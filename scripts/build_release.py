Import("env")
import os
import re
import shutil
import subprocess

pioenv = env.get("PIOENV")
OTA_NAME = f"{pioenv}_jarolift_ota"         # prefix for ota release image
INSTALL_NAME = f"{pioenv}_jarolift_flash"   # prefix for merged flash image     

APP_BIN = "$BUILD_DIR/${PROGNAME}.bin"
MERGED_BIN = "$BUILD_DIR/${PROGNAME}_merged.bin"
RELEASE_PATH = "$PROJECT_DIR/release"
BOARD_CONFIG = env.BoardConfig()


# extract program version from /include/config.h
def extract_version():
    config_path = env.subst("$PROJECT_DIR/include/config.h")
    with open(config_path, "r") as file:
        content = file.read()
        match = re.search(r'#define VERSION\s+"(.+)"', content)
        if match:
            return match.group(1)
        else:
            return None

def merge_bin(source, target, env):
    flash_images = env.Flatten(env.get("FLASH_EXTRA_IMAGES", [])) + ["$ESP32_APP_OFFSET", APP_BIN]

    # Pfade substituieren (löst Variablen auf)
    merged_bin_path = env.subst(MERGED_BIN)
    pythonexe       = env.subst("$PYTHONEXE")
    objcopy         = env.subst("$OBJCOPY")

    # flash_images: abwechselnd Adresse (hex) und Dateipfad
    flash_images_subst = [env.subst(x) for x in flash_images]

    # Befehl als Liste aufbauen – subprocess kümmert sich um Quoting
    cmd = [
        pythonexe, objcopy,
        "--chip", BOARD_CONFIG.get("build.mcu", "esp32"),
        "merge_bin",
        "--flash_size", BOARD_CONFIG.get("upload.flash_size", "4MB"),
        "-o", merged_bin_path,
    ] + flash_images_subst

    ret = subprocess.call(cmd)
    if ret != 0:
        print(f"[build_release] merge_bin fehlgeschlagen (exit {ret})")
        return

    release_path = env.subst(RELEASE_PATH)
    if env.get("PIOENV") == "esp32":
        if os.path.exists(release_path):
            shutil.rmtree(release_path)
        os.makedirs(release_path)
    else:
        if not os.path.exists(release_path):
            os.makedirs(release_path)

    version = extract_version()
    merged_file    = os.path.join(release_path, f"{INSTALL_NAME}_{version}.bin")
    ota_update_file = os.path.join(release_path, f"{OTA_NAME}_{version}.bin")
    shutil.copyfile(merged_bin_path, merged_file)
    shutil.copyfile(env.subst(APP_BIN), ota_update_file)


# Add a post action that runs esptoolpy to merge available flash images
env.AddPostAction(APP_BIN, merge_bin)
