ESP32-Jarolift-Controller v1.10.3-beta
======================================

Unterstuetzte Chips
-------------------
  esp32   - ESP32-WROOM, ESP32-WROVER, ESP32-MINI
  esp32s2 - ESP32-S2
  esp32s3 - ESP32-S3

Dateien in diesem Release
--------------------------

  ESP32-Jarolift-Controller_v1.10.3-beta_esp32_flash.bin
    -> Erstmaliges Flashen fuer ESP32
    -> esptool.py --chip esp32 --baud 460800 write_flash 0x0 ESP32-Jarolift-Controller_v1.10.3-beta_esp32_flash.bin

  ESP32-Jarolift-Controller_v1.10.3-beta_esp32_ota.bin
    -> OTA-Update fuer ESP32 via WebUI -> Tools -> OTA Update

  ESP32-Jarolift-Controller_v1.10.3-beta_esp32s2_flash.bin
    -> Erstmaliges Flashen fuer ESP32S2
    -> esptool.py --chip esp32s2 --baud 460800 write_flash 0x0 ESP32-Jarolift-Controller_v1.10.3-beta_esp32s2_flash.bin

  ESP32-Jarolift-Controller_v1.10.3-beta_esp32s2_ota.bin
    -> OTA-Update fuer ESP32S2 via WebUI -> Tools -> OTA Update

  ESP32-Jarolift-Controller_v1.10.3-beta_esp32s3_flash.bin
    -> Erstmaliges Flashen fuer ESP32S3
    -> esptool.py --chip esp32s3 --baud 460800 write_flash 0x0 ESP32-Jarolift-Controller_v1.10.3-beta_esp32s3_flash.bin

  ESP32-Jarolift-Controller_v1.10.3-beta_esp32s3_ota.bin
    -> OTA-Update fuer ESP32S3 via WebUI -> Tools -> OTA Update

Positionssteuerung
------------------
Dieser Build enthaelt zeitbasierte Positionssteuerung (0-100%) fuer Jarolift TDEF Rolllaeden.
Kalibrierung erforderlich pro Kanal (Service-Seite -> Laufzeit-Kalibrierung).

Quellcode
---------
https://github.com/Banabas/ESP32-Jarolift-Controller
