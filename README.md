# Reconocimiento facial en tiempo real con Python

Detecta y reconoce rostros usando la cámara, con `face_recognition` y OpenCV.

## Requisitos

- Python 3.12 (probado en Windows)
- Una cámara (webcam o celular con Iriun Webcam)
- Git

## Instalación (Windows)

```bash
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
cd TU_REPOSITORIO

python -m venv .venv
.venv\Scripts\activate

pip install dlib-bin
pip install face_recognition --no-deps
pip install -r requirements.txt
```

> `face_recognition` se instala con `--no-deps` para evitar que pip intente
> compilar `dlib` (que exige Visual Studio C++). En su lugar se usa `dlib-bin`,
> que ya viene compilado.

## Uso

1. Ejecuta el programa una vez para que cree la carpeta `caras_conocidas/`:
   ```bash
   python reconocimiento_facial.py
   ```
2. Dentro de `caras_conocidas/`, agrega una foto por persona (de frente, buena
   luz, una sola cara), nombrada como quieres que aparezca: `Juan.jpg`.
3. Ejecuta de nuevo el programa. Se abrirá la cámara y mostrará un recuadro
   verde con el nombre, o rojo con "Desconocido".
4. Presiona `q` para salir.

## Configuración

- `TOLERANCIA` (en el script): menor valor = más estricto. Por defecto `0.6`.
- Si abre una cámara equivocada, cambia `cv2.VideoCapture(0)` por `1` o `2`.

## Privacidad

La carpeta `caras_conocidas/` está en `.gitignore` a propósito: no subas fotos
de personas a un repositorio sin su consentimiento.
