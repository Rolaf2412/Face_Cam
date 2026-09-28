"""
Reconocimiento facial en tiempo real con Python.

Requisitos (instalar antes de ejecutar):
    pip install face_recognition opencv-python numpy

Nota: face_recognition depende de dlib, que puede requerir CMake y un
compilador de C++ instalado en el sistema. En Windows suele ser más
fácil instalar dlib con:
    pip install dlib-bin
o usando conda:
    conda install -c conda-forge dlib

Uso:
    1. Crea una carpeta "caras_conocidas" junto a este script.
    2. Dentro, agrega una foto por persona, nombrada como quieras
       que aparezca el texto, por ejemplo: "Juan.jpg", "Maria.png".
    3. Ejecuta: python reconocimiento_facial.py
    4. Presiona 'q' para salir.
"""

import os
import cv2
import face_recognition
import numpy as np

CARPETA_CARAS_CONOCIDAS = "caras_conocidas"
TOLERANCIA = 0.6          # Menor = más estricto. 0.6 es el valor típico.
ESCALA_REDUCCION = 0.25   # Reduce resolución para procesar más rápido


def cargar_caras_conocidas(carpeta):
    """Carga las imágenes de la carpeta y calcula sus encodings faciales."""
    encodings_conocidos = []
    nombres_conocidos = []

    if not os.path.isdir(carpeta):
        os.makedirs(carpeta, exist_ok=True)
        print(f"Se creó la carpeta '{carpeta}'. Agrega fotos ahí y vuelve a ejecutar.")
        return encodings_conocidos, nombres_conocidos

    for archivo in os.listdir(carpeta):
        ruta = os.path.join(carpeta, archivo)
        nombre, ext = os.path.splitext(archivo)

        if ext.lower() not in (".jpg", ".jpeg", ".png"):
            continue

        imagen = face_recognition.load_image_file(ruta)
        encodings = face_recognition.face_encodings(imagen)

        if len(encodings) == 0:
            print(f"⚠ No se detectó ninguna cara en '{archivo}', se omite.")
            continue

        encodings_conocidos.append(encodings[0])
        nombres_conocidos.append(nombre)
        print(f"✔ Cara cargada: {nombre}")

    return encodings_conocidos, nombres_conocidos


def reconocer_en_video(encodings_conocidos, nombres_conocidos):
    """Abre la cámara y reconoce caras en tiempo real."""
    video = cv2.VideoCapture(0)

    if not video.isOpened():
        print("No se pudo acceder a la cámara.")
        return

    print("Presiona 'q' para salir.")

    while True:
        ret, frame = video.read()
        if not ret:
            break

        # Reducir el frame para acelerar el procesamiento
        frame_pequeno = cv2.resize(frame, (0, 0), fx=ESCALA_REDUCCION, fy=ESCALA_REDUCCION)
        frame_rgb = cv2.cvtColor(frame_pequeno, cv2.COLOR_BGR2RGB)

        ubicaciones = face_recognition.face_locations(frame_rgb)
        encodings_frame = face_recognition.face_encodings(frame_rgb, ubicaciones)

        for (top, right, bottom, left), encoding in zip(ubicaciones, encodings_frame):
            nombre = "Desconocido"

            if encodings_conocidos:
                distancias = face_recognition.face_distance(encodings_conocidos, encoding)
                mejor_indice = np.argmin(distancias)

                if distancias[mejor_indice] < TOLERANCIA:
                    nombre = nombres_conocidos[mejor_indice]

            # Reescalar coordenadas al tamaño original del frame
            factor = int(1 / ESCALA_REDUCCION)
            top, right, bottom, left = top * factor, right * factor, bottom * factor, left * factor

            color = (0, 255, 0) if nombre != "Desconocido" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(frame, (left, bottom - 25), (right, bottom), color, cv2.FILLED)
            cv2.putText(frame, nombre, (left + 6, bottom - 6),
                        cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)

        cv2.imshow("Reconocimiento facial - presiona 'q' para salir", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video.release()
    cv2.destroyAllWindows()


def main():
    encodings_conocidos, nombres_conocidos = cargar_caras_conocidas(CARPETA_CARAS_CONOCIDAS)
    reconocer_en_video(encodings_conocidos, nombres_conocidos)


if __name__ == "__main__":
    main()
