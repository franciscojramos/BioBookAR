import cv2
import os
import sys
import numpy as np
from pathlib import Path

# Añadir ruta base del proyecto para importar módulos internos
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# Importar lógica de base de datos
from base_datos.db import marcar_tema_como_visto

# Obtener usuario_id desde argumentos
usuario_id = int(sys.argv[1]) if len(sys.argv) > 1 else 0

# Paths a recursos
IMG_DIR = BASE_DIR / "recursos" / "imagenes"
VID_DIR = BASE_DIR / "recursos" / "videos"

# Inicializar ORB para detección de imagen
orb = cv2.ORB_create()
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Inicializar ARUCO
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
aruco_params = cv2.aruco.DetectorParameters()
aruco_detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

# Inicializar reproductores de video por ID
video_caps = {i: cv2.VideoCapture(str(VID_DIR / f"tema{i}.mp4")) for i in range(1, 9)}

# Iniciar cámara
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, _ = aruco_detector.detectMarkers(gray)

    if ids is not None:
        for i, marker_corners in enumerate(corners):
            id_ = ids[i][0]
            if 1 <= id_ <= 8 and id_ in video_caps:
                # Leer siguiente frame del video
                cap_video = video_caps[id_]
                ret_video, frame_video = cap_video.read()

                if not ret_video:
                    cap_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    ret_video, frame_video = cap_video.read()

                if not ret_video:
                    continue

                # Redimensionar video al tamaño del marcador
                pts_dst = np.array(marker_corners[0], dtype="float32")
                h, w = frame_video.shape[:2]
                pts_src = np.array([[0, 0], [w, 0], [w, h], [0, h]], dtype="float32")

                matrix, _ = cv2.findHomography(pts_src, pts_dst)
                warped = cv2.warpPerspective(frame_video, matrix, (frame.shape[1], frame.shape[0]))

                # Crear máscara y combinar con el frame de cámara
                mask = np.zeros_like(frame, dtype=np.uint8)
                cv2.fillConvexPoly(mask, pts_dst.astype(int), (255, 255, 255))
                mask_inv = cv2.bitwise_not(mask)
                frame = cv2.bitwise_and(frame, mask_inv)
                frame = cv2.add(frame, warped)

                # Marcar como visto en base de datos
                marcar_tema_como_visto(usuario_id, id_)

    cv2.imshow("Camara RA", frame)
    if cv2.waitKey(1) & 0xFF in [27, ord('q')]:
        break

cap.release()
for cap_video in video_caps.values():
    cap_video.release()
cv2.destroyAllWindows()
