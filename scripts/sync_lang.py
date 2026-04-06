# Pre-Build Skript: Synchronisiert lang.js mit lib.js
# EspWebUI 0.0.7 prüft strenger und erwartet alle data-i18n Keys in lang.js.
# Keys die in lib.js (lib_translations) stehen werden hier automatisch ergänzt.
Import("env")
import re, os

project_dir = env.subst("$PROJECT_DIR")
lang_path = os.path.join(project_dir, "web", "js", "lang.js")
lib_path  = os.path.join(project_dir, "web", "output", "lib.js")
html_dir  = os.path.join(project_dir, "web", "html")

with open(lang_path, encoding="utf-8") as f:
    lang_content = f.read()
lang_keys = set(re.findall(r'^\s{2}(\w+):', lang_content, re.MULTILINE))

with open(lib_path, encoding="utf-8") as f:
    lib_content = f.read()
lib_keys_entries = {}
for m in re.finditer(r'\s{2}(\w+):\s*\{\s*de:\s*"([^"]*)"[^}]*en:\s*"([^"]*)"[^}]*\}', lib_content):
    lib_keys_entries[m.group(1)] = (m.group(2), m.group(3))

html_keys = set()
for fname in os.listdir(html_dir):
    if fname.endswith('.html'):
        with open(os.path.join(html_dir, fname), encoding="utf-8") as f:
            content = f.read()
        for match in re.findall(r'data-i18n="([^"]+)"', content):
            key = re.split(r'\+\+|\$| ', match)[0]
            if key:
                html_keys.add(key)

missing = sorted(html_keys - lang_keys)
added = []

if missing:
    # Schließendes }; entfernen
    base = lang_content.rstrip()
    if base.endswith("};"):
        base = base[:-2].rstrip()
    elif base.endswith("}"):
        base = base[:-1].rstrip()

    for key in missing:
        if key in lib_keys_entries:
            de, en = lib_keys_entries[key]
            base += f'\n  {key}: {{\n    de: "{de}",\n    en: "{en}",\n  }},'
            added.append(key)

    base += "\n};\n"
    with open(lang_path, "w", encoding="utf-8") as f:
        f.write(base)

if added:
    print(f"[sync_lang] {len(added)} Keys aus lib.js ergänzt.")
else:
    print("[sync_lang] lang.js vollständig – nichts zu tun.")
