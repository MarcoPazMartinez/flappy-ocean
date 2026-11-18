@echo off
rem Genera dist\FlappyDiver.exe en una PC con Windows y Python 3.10 o superior.
rem Uso: doble clic o ejecutar construir_exe.bat desde la carpeta del repo.

python -m venv .venv-exe
if errorlevel 1 goto error
call .venv-exe\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt pyinstaller
if errorlevel 1 goto error

pyinstaller --noconfirm --clean FlappyDiver.spec
if errorlevel 1 goto error

echo.
echo Probando el ejecutable (--verificar)...
set SDL_VIDEODRIVER=dummy
set SDL_AUDIODRIVER=dummy
dist\FlappyDiver.exe --verificar
if errorlevel 1 goto error

echo.
echo LISTO: dist\FlappyDiver.exe
echo El ranking se guarda en la carpeta database junto al .exe.
pause
exit /b 0

:error
echo.
echo ERROR: no se pudo generar el ejecutable. Revisa los mensajes de arriba.
pause
exit /b 1
