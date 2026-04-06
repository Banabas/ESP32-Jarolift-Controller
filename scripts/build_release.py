Import("env")
import os
import re
import shutil
import subprocess

pioenv    = env.get("PIOENV")
APP_BIN   = "$BUILD_DIR/${PROGNAME}.bin"
MERGED_BIN = "$BUILD_DIR/${PROGNAME}_merged.bin"
RELEASE_PATH = "$PROJECT_DIR/release"
BOARD_CONFIG = env.BoardConfig()

PROJECT_NAME = "ESP32-Jarolift-Controller"


def extract_version():
    config_path = env.subst("$PROJECT_DIR/include/config.h")
    with open(config_path, "r") as f:
        m = re.search(r'#define VERSION\s+"([^"]+)"', f.read())
        return m.group(1) if m else "unknown"


def write_flash_instructions(release_path, version, mcu):
    """Create a README.txt with flashing instructions for this release."""
    readme = os.path.join(release_path, "README.txt")
    content = f"""{PROJECT_NAME} {version}
{'=' * (len(PROJECT_NAME) + len(version) + 1)}

Files in this release
---------------------
{PROJECT_NAME}_{version}_{mcu}_flash.bin
  Complete flash image – use this for first-time installation.
  Flash with esptool.py or the ESP32 Flash Download Tool.

  esptool.py command:
    esptool.py --chip {mcu} --baud 460800 write_flash 0x0 {PROJECT_NAME}_{version}_{mcu}_flash.bin

{PROJECT_NAME}_{version}_{mcu}_ota.bin
  OTA update image – use this for over-the-air updates via the web interface.
  Upload through: WebUI -> Tools -> OTA Update

Position control feature
------------------------
This build adds time-based position control (0-100%) for Jarolift TDEF shutters.
Calibration is required for each channel (Service page -> Travel Time Calibration).

Source code
-----------
https://github.com/dewenni/ESP32-Jarolift-Controller
"""
    with open(readme, "w") as f:
        f.write(content)


def merge_bin(source, target, env):
    flash_images = env.Flatten(env.get("FLASH_EXTRA_IMAGES", [])) + ["$ESP32_APP_OFFSET", APP_BIN]

    merged_bin_path  = env.subst(MERGED_BIN)
    pythonexe        = env.subst("$PYTHONEXE")
    objcopy          = env.subst("$OBJCOPY")
    flash_images_sub = [env.subst(x) for x in flash_images]
    mcu              = BOARD_CONFIG.get("build.mcu", "esp32")
    flash_size       = BOARD_CONFIG.get("upload.flash_size", "4MB")

    cmd = [
        pythonexe, objcopy,
        "--chip", mcu,
        "merge_bin",
        "--flash_size", flash_size,
        "-o", merged_bin_path,
    ] + flash_images_sub

    ret = subprocess.call(cmd)
    if ret != 0:
        print(f"[build_release] merge_bin failed (exit {ret})")
        return

    release_path = env.subst(RELEASE_PATH)
    # Clear release folder only on first env (esp32)
    if pioenv == "esp32":
        if os.path.exists(release_path):
            shutil.rmtree(release_path)
        os.makedirs(release_path)
    else:
        os.makedirs(release_path, exist_ok=True)

    version = extract_version()

    # Clean version string for filenames (remove leading 'v' if present)
    ver_clean = version.lstrip("v")

    flash_name = f"{PROJECT_NAME}_{version}_{mcu}_flash.bin"
    ota_name   = f"{PROJECT_NAME}_{version}_{mcu}_ota.bin"

    flash_dest = os.path.join(release_path, flash_name)
    ota_dest   = os.path.join(release_path, ota_name)

    shutil.copyfile(merged_bin_path,       flash_dest)
    shutil.copyfile(env.subst(APP_BIN),    ota_dest)

    write_flash_instructions(release_path, version, mcu)

    print(f"\n[build_release] Release files written to: {release_path}")
    print(f"  {flash_name}  (full flash image)")
    print(f"  {ota_name}    (OTA update)")
    print(f"  README.txt")


env.AddPostAction(APP_BIN, merge_bin)
