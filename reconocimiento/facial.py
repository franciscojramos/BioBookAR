import cv2
import face_recognition
import numpy as np

def capturar_y_codificar_rostro():
    """
    Captura un rostro con la webcam y devuelve su encoding facial.
    Retorna None si no se detecta exactamente un rostro.
    """
    video = cv2.VideoCapture(0)
    encoding_resultado = None

    print("Iniciando cámara... Presiona 'q' para capturar.")

    while True:
        ret, frame = video.read()
        if not ret:
            print("Error accediendo a la cámara.")
            break

        # Mostrar imagen con instrucciones
        cv2.putText(frame, "Presiona 'q' para capturar rostro", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Captura de rostro", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):# Presionar 'q' para capturar
            # Tomar imagen actual y cerrar
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            caras = face_recognition.face_locations(rgb_frame)
            if len(caras) == 1:
                encoding = face_recognition.face_encodings(rgb_frame, caras)[0]
                encoding_resultado = encoding
                print("Rostro capturado correctamente.")
            else:
                print("Error: se necesita exactamente una cara (detectadas: {})".format(len(caras)))
            break

    video.release()
    cv2.destroyAllWindows() # Cerrar ventana de captura
    return encoding_resultado

def comparar_encoding_con_base(encoding_nuevo, lista_encodings_guardados, tolerancia=0.5):
    """
    Compara un encoding nuevo con una lista de encodings guardados.
    Devuelve el ID del usuario si hay coincidencia, o None si no hay match.
    """
    for usuario_id, encoding_guardado in lista_encodings_guardados:
        matches = face_recognition.compare_faces([encoding_guardado], encoding_nuevo, tolerance=tolerancia)
        if matches[0]:
            return usuario_id
    return None
