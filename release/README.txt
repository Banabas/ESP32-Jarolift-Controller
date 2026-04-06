ESP32-Jarolift-Controller v1.10.0-beta
======================================

Supported chips
---------------
  esp32   - ESP32-WROOM, ESP32-WROVER, ESP32-MINI
  esp32s2 - ESP32-S2
  esp32s3 - ESP32-S3
  esp32c3 - ESP32-C3

Files in this release
---------------------

  ESP32-Jarolift-Controller_v1.10.0-beta_esp32_flash.bin
    -> First-time installation for ESP32
    -> esptool.py --chip esp32 --baud 460800 write_flash 0x0 ESP32-Jarolift-Controller_v1.10.0-beta_esp32_flash.bin

  ESP32-Jarolift-Controller_v1.10.0-beta_esp32_ota.bin
    -> OTA update for ESP32 via WebUI -> Tools -> OTA Update

  ESP32-Jarolift-Controller_v1.10.0-beta_esp32s2_flash.bin
    -> First-time installation for ESP32S2
    -> esptool.py --chip esp32s2 --baud 460800 write_flash 0x0 ESP32-Jarolift-Controller_v1.10.0-beta_esp32s2_flash.bin

  ESP32-Jarolift-Controller_v1.10.0-beta_esp32s2_ota.bin
    -> OTA update for ESP32S2 via WebUI -> Tools -> OTA Update

  ESP32-Jarolift-Controller_v1.10.0-beta_esp32s3_flash.bin
    -> First-time installation for ESP32S3
    -> esptool.py --chip esp32s3 --baud 460800 write_flash 0x0 ESP32-Jarolift-Controller_v1.10.0-beta_esp32s3_flash.bin

  ESP32-Jarolift-Controller_v1.10.0-beta_esp32s3_ota.bin
    -> OTA update for ESP32S3 via WebUI -> Tools -> OTA Update

  ESP32-Jarolift-Controller_v1.10.0-beta_esp32c3_flash.bin
    -> First-time installation for ESP32C3
    -> esptool.py --chip esp32c3 --baud 460800 write_flash 0x0 ESP32-Jarolift-Controller_v1.10.0-beta_esp32c3_flash.bin

  ESP32-Jarolift-Controller_v1.10.0-beta_esp32c3_ota.bin
    -> OTA update for ESP32C3 via WebUI -> Tools -> OTA Update

Position control feature
------------------------
This build adds time-based position control (0-100%) for Jarolift TDEF shutters.
Calibration required for each channel (Service page -> Travel Time Calibration).

Source code
-----------
https://github.com/Banabas/ESP32-Jarolift-Controller
