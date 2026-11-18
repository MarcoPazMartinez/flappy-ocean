# Generar y usar FlappyDiver.exe

## Opción 1: automática (GitHub Actions)

1. En GitHub, pestaña **Actions** → **Generar FlappyDiver.exe** → **Run workflow**.
2. Cuando termina (unos 3 a 5 minutos), entrá a la ejecución y bajá el archivo **FlappyDiver-windows** de *Artifacts*. Es un zip con `FlappyDiver.exe`.
3. Si se crea un tag `v*` (por ejemplo `v1.0`), el `.exe` también queda adjunto al Release.

El flujo prueba el `.exe` antes de publicarlo: corre `FlappyDiver.exe --verificar` (imágenes, sonidos, partida simulada y base de datos) y comprueba que el juego arranca.

## Opción 2: en una PC con Windows

Con Python 3.10 o superior instalado, hacer doble clic en `construir_exe.bat`. El resultado queda en `dist\FlappyDiver.exe`.

## Usarlo en la expo

- Copiá `FlappyDiver.exe` a una carpeta propia (por ejemplo `C:\Expo\`). No necesita Python ni instalación.
- **El ranking se guarda en `database\ranking.db`, al lado del `.exe`.** Se crea solo la primera vez.
- Para **reiniciar el ranking** antes de la expo, borrá la carpeta `database` que está junto al `.exe`.
- Si la carpeta no permite escribir (por ejemplo `C:\Program Files`), el ranking se guarda en `C:\Users\<usuario>\FlappyDiver`.
- Para comprobar que todo está bien, desde una terminal: `FlappyDiver.exe --verificar`. Crea `verificacion.txt` con el detalle.

## Avisos conocidos

- **Windows SmartScreen / antivirus:** como el `.exe` no está firmado, puede aparecer "Windows protegió su PC". Se resuelve con **Más información → Ejecutar de todas formas**. Conviene probarlo en la PC de la expo con anticipación.
- El primer arranque puede tardar unos segundos, porque el `.exe` se descomprime en una carpeta temporal.
