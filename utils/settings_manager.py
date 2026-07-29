import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "..", "config.json")

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
    """Carga las configuraciones; si no existen, crea el archivo con las predeterminadas."""
    if not os.path.exists(CONFIG_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()
    
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            loaded_settings = json.load(f)
            
            # Combinamos las configuraciones por defecto con las cargadas.
            # Así, si en el futuro agregas nuevas opciones, no habrá errores por claves faltantes.
            settings = DEFAULT_SETTINGS.copy()
            settings.update(loaded_settings)
            return settings
            
    except (json.JSONDecodeError, OSError):
        # Capturamos específicamente errores de formato JSON o de lectura del sistema operativo
        return DEFAULT_SETTINGS.copy()

def save_settings(settings_dict):
    """Guarda las configuraciones en el archivo JSON."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(settings_dict, f, indent=4)