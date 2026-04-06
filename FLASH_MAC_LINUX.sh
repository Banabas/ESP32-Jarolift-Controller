#!/bin/bash
echo "============================================="
echo " ESP32 Jarolift Controller - Build & Flash"
echo "============================================="
echo ""

# PlatformIO prüfen
if ! command -v pio &> /dev/null; then
    echo "FEHLER: 'pio' nicht gefunden."
    echo "Installation: pip install platformio"
    exit 1
fi

# USB-Port automatisch erkennen
PORT=$(ls /dev/tty.usbserial* /dev/ttyUSB* /dev/ttyACM* 2>/dev/null | head -1)

if [ -z "$PORT" ]; then
    echo "FEHLER: Kein USB-Seriell-Port gefunden."
    echo "ESP32 einstecken und nochmal versuchen."
    echo "Verfügbare Ports:"
    ls /dev/tty* | grep -E "usb|USB|ACM" 2>/dev/null
    exit 1
fi

echo "[1/2] Gefundener Port: $PORT"
echo "[2/2] Kompiliere und flashe ESP32..."
echo ""

cd "$(dirname "$0")"
pio run --environment esp32 --target upload --upload-port "$PORT"

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Fertig! ESP32 wurde erfolgreich geflasht."
    echo ""
    echo "Nächste Schritte:"
    echo "  1. Verbinde mit WLAN 'ESP32_Jarolift' (Setup-Mode)"
    echo "  2. Öffne http://192.168.4.1"
    echo "  3. WLAN konfigurieren"
    echo "  4. Rollläden kalibrieren (Einstellungen → Kanal → ⚙)"
else
    echo ""
    echo "FEHLER beim Flashen. Port korrekt? Aktuell: $PORT"
fi
