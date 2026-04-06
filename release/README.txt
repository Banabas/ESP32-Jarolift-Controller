ESP32-Jarolift-Controller v1.10.0-beta
======================================

Files in this release
---------------------
ESP32-Jarolift-Controller_v1.10.0-beta_esp32_flash.bin
  Complete flash image – use this for first-time installation.
  Flash with esptool.py or the ESP32 Flash Download Tool.

  esptool.py command:
    esptool.py --chip esp32 --baud 460800 write_flash 0x0 ESP32-Jarolift-Controller_v1.10.0-beta_esp32_flash.bin

ESP32-Jarolift-Controller_v1.10.0-beta_esp32_ota.bin
  OTA update image – use this for over-the-air updates via the web interface.
  Upload through: WebUI -> Tools -> OTA Update

Position control feature
------------------------
This build adds time-based position control (0-100%) for Jarolift TDEF shutters.
Calibration is required for each channel (Service page -> Travel Time Calibration).

Source code
-----------
https://github.com/dewenni/ESP32-Jarolift-Controller
