@echo off
echo =============================================
echo  ESP32 Jarolift Controller - Build & Flash
echo =============================================
echo.

REM PlatformIO muss installiert sein (VSCode + PlatformIO Extension)
REM oder: pip install platformio

where pio >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo FEHLER: 'pio' nicht gefunden.
    echo Bitte PlatformIO installieren:
    echo   pip install platformio
    echo   oder VSCode + PlatformIO Extension
    pause
    exit /b 1
)

echo [1/2] Kompiliere und flashe ESP32...
echo       (USB-Kabel einstecken und COM-Port weiter unten eintragen)
echo.

REM === COM-Port anpassen! ===
set UPLOAD_PORT=COM3

cd /d "%~dp0"
pio run --environment esp32 --target upload --upload-port %UPLOAD_PORT%

if %ERRORLEVEL% == 0 (
    echo.
    echo Fertig! ESP32 wurde erfolgreich geflasht.
) else (
    echo.
    echo FEHLER beim Flashen. COM-Port korrekt? Aktuell: %UPLOAD_PORT%
    echo Verfuegbare Ports: 
    mode | findstr "COM"
)
pause
