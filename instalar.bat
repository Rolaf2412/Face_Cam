@echo off
setlocal
cd /d "%~dp0"

echo ==========================================
echo  Instalador - Reconocimiento facial
echo ==========================================
echo.

where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] No se encontro Python. Instalalo desde https://www.python.org/downloads/
    echo         y marca la casilla "Add Python to PATH" durante la instalacion.
    goto :fin
)

where git >nul 2>&1
if errorlevel 1 (
    echo [ERROR] No se encontro Git. Instalalo desde https://git-scm.com/downloads
    echo         Se necesita para descargar los modelos de face_recognition.
    goto :fin
)

if not exist ".venv\Scripts\activate.bat" (
    echo [1/5] Creando entorno virtual .venv ...
    python -m venv .venv
    if errorlevel 1 goto :error
) else (
    echo [1/5] El entorno virtual .venv ya existe, se reutiliza.
)

call ".venv\Scripts\activate.bat"

echo [2/5] Actualizando pip ...
python -m pip install --upgrade pip
if errorlevel 1 goto :error

echo [3/5] Instalando dlib-bin (version precompilada, sin Visual Studio) ...
pip install dlib-bin
if errorlevel 1 goto :error

echo [4/5] Instalando face_recognition (sin dependencias, para no compilar dlib) ...
pip install face_recognition --no-deps
if errorlevel 1 goto :error

echo [5/5] Instalando el resto de librerias ...
pip install -r requirements.txt
if errorlevel 1 goto :error

if not exist "caras_conocidas" mkdir "caras_conocidas"

echo.
echo ==========================================
echo  Instalacion terminada.
echo ==========================================
echo  1. Agrega una foto por persona en la carpeta "caras_conocidas"
echo     (de frente, buena luz, una sola cara). Ejemplo: Juan.jpg
echo  2. Abre esta carpeta en CMD y ejecuta:
echo        .venv\Scripts\activate.bat
echo        python reconocimiento_facial.py
echo  3. Presiona la tecla q en la ventana de la camara para salir.
echo ==========================================
goto :fin

:error
echo.
echo [ERROR] Algo fallo en la instalacion. Copia el mensaje de arriba
echo         y buscalo o pegalo al abrir un issue en el repositorio.

:fin
echo.
pause
endlocal
