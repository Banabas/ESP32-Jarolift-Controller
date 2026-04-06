# Positionssteuerung – Flash-Anleitung

## Was ist neu?

- **Schieberegler** in der WebUI pro Rollladen (0–100%)
- **MQTT-Positionsbefehl**: Payload `0`–`100` auf `/cmd/shutter/N`
- **Kalibrierung** der Laufzeit einmalig nötig
- **Letzter Positionswert** wird nach Neustart wiederhergestellt

---

## Schritt 1: Voraussetzungen

**PlatformIO installieren** (einmalig):

```bash
pip install platformio
```

Oder: [VSCode](https://code.visualstudio.com) + PlatformIO Extension installieren.

---

## Schritt 2: Flashen

### Windows

1. `FLASH_WINDOWS.bat` öffnen
2. `COM-Port` anpassen (Geräte-Manager → Anschlüsse)
3. Doppelklick auf `FLASH_WINDOWS.bat`

### Mac / Linux

```bash
bash FLASH_MAC_LINUX.sh
```

Der Port wird automatisch erkannt.

### Manuell

```bash
pio run --environment esp32 --target upload --upload-port /dev/ttyUSB0
```

Für andere Chips: `esp32s2`, `esp32s3`, `esp32c3`

---

## Schritt 3: Kalibrierung (einmalig pro Rollladen)

Da Jarolift-Motoren **keinen Positionsstatus zurücksenden**, muss die
Laufzeit einmalig gemessen werden:

1. Rollladen vollständig **öffnen** (bis Anschlag)
2. In der WebUI: Kanal → `DOWN`-Button gedrückt halten und gleichzeitig
   den Schieberegler auf einen Testwert ziehen  
   *(oder direkt per MQTT: `/cmd/shutter/1` → `calib_start`)*
3. Rollladen vollständig **schließen** lassen
4. Wenn unten: `/cmd/shutter/1` → `calib_finish` senden  
   → Laufzeit wird in `config.json` gespeichert

**Einfacherer Weg über WebUI** (nach nächstem Update):
Einstellungen → Kanal N → ⚙ Kalibrieren

---

## MQTT-Protokoll (neu)

```
# Zielposition setzen (0 = offen, 100 = geschlossen)
Topic:   <prefix>/cmd/shutter/1
Payload: 50

# Aktuelle Position (Status)
Topic:   <prefix>/status/shutter/1
Payload: 50
```

Alle bisherigen Befehle (UP, DOWN, STOP, SHADE) funktionieren weiterhin.

---

## Home Assistant

In der HA MQTT Discovery wird die `position_topic` automatisch gesetzt.
Für den Schieberegler in HA zusätzlich in der HA-Konfiguration ergänzen:

```yaml
cover:
  - platform: mqtt
    name: "Wohnzimmer"
    command_topic: "jarolift/cmd/shutter/1"
    position_topic: "jarolift/status/shutter/1"
    set_position_topic: "jarolift/cmd/shutter/1"
    position_open: 0
    position_closed: 100
```
