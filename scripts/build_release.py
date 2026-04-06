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


def write_flash_instructions(release_path, version):
    """Create a README.txt with flashing instructions for this release."""
    readme = os.path.join(release_path, "README.txt")
    mcus = ["esp32", "esp32s2", "esp32s3", "esp32c3"]
    file_list = ""
    for m in mcus:
        file_list += f"""
  {PROJECT_NAME}_{version}_{m}_flash.bin
    -> First-time installation for {m.upper()}
    -> esptool.py --chip {m} --baud 460800 write_flash 0x0 {PROJECT_NAME}_{version}_{m}_flash.bin

  {PROJECT_NAME}_{version}_{m}_ota.bin
    -> OTA update for {m.upper()} via WebUI -> Tools -> OTA Update
"""
    content = f"""{PROJECT_NAME} {version}
{'=' * (len(PROJECT_NAME) + len(version) + 1)}

Supported chips
---------------
  esp32   - ESP32-WROOM, ESP32-WROVER, ESP32-MINI
  esp32s2 - ESP32-S2
  esp32s3 - ESP32-S3
  esp32c3 - ESP32-C3

Files in this release
---------------------
{file_list}
Position control feature
------------------------
This build adds time-based position control (0-100%) for Jarolift TDEF shutters.
Calibration required for each channel (Service page -> Travel Time Calibration).

Source code
-----------
https://github.com/Banabas/ESP32-Jarolift-Controller
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

    if pioenv == "esp32":
        write_flash_instructions(release_path, version)

    print(f"\n[build_release] Release files written to: {release_path}")
    print(f"  {flash_name}  (full flash image)")
    print(f"  {ota_name}    (OTA update)")
    print(f"  README.txt")


env.AddPostAction(APP_BIN, merge_bin)
