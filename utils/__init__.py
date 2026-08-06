# Dentro de utils/__init__.py
import os
import sys

def resolver_ruta(ruta_relativa):
    """Devuelve la ruta absoluta, ya sea en desarrollo o como ejecutable de PyInstaller"""
    try:
        ruta_base = sys._MEIPASS
    except Exception:
        ruta_base = os.path.abspath(".")
    return os.path.join(ruta_base, ruta_relativa)