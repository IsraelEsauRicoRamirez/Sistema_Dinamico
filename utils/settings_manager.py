import json
import os
import sys

if getattr(sys, 'frozen', False):
    ruta_base = os.path.dirname(sys.executable)
else:
    ruta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

CONFIG_FILE = os.path.join(ruta_base, "config.json")

DEFAULT_SETTINGS = {
    "tema_app": True,
    "modo_oscuro": False,
    "tamano_fuente": "Normal",
    "precision": "Alta",
    "auto_guardar": True,
    "animacion_grafica": True,
    "alertas": True,
    "correo_csv": False,
    "idioma": "Español",
    "formato_num": "1,000.00"
}

def load_settings():
    if not os.path.exists(CONFIG_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()
    
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            loaded_settings = json.load(f)
            settings = DEFAULT_SETTINGS.copy()
            settings.update(loaded_settings)
            return settings
            
    except (json.JSONDecodeError, OSError):
        return DEFAULT_SETTINGS.copy()

def save_settings(settings_dict):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(settings_dict, f, indent=4)