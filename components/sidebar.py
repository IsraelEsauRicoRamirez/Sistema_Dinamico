# components/sidebar.py
import customtkinter as ctk
from utils.theme import COLORS


class Sidebar(ctk.CTkFrame):
    """
    Barra lateral izquierda con botón hamburguesa y íconos de navegación.
    """

    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            width=72,
            fg_color=COLORS["card"],
            corner_radius=0,
            **kwargs,
        )
        self.grid_propagate(False)
        self._active_btn = None
        self._build()

    def _build(self):
        self.grid_rowconfigure(10, weight=1)  # empuja settings al fondo

        # ── Botón hamburguesa ──────────────────────────────
        self._hamburger = ctk.CTkButton(
            self,
            text="☰",
            font=("Arial", 20),
            width=48,
            height=48,
            fg_color="transparent",
            hover_color=COLORS["bg"],
            text_color=COLORS["text_main"],
            corner_radius=12,
        )
        self._hamburger.grid(row=0, column=0, padx=12, pady=(16, 8))

        # Separador
        ctk.CTkFrame(self, height=1, fg_color=COLORS["border"]).grid(
            row=1, column=0, sticky="ew", padx=12, pady=(0, 8)
        )

        # ── Íconos de navegación ───────────────────────────
        nav_items = [
            ("⊞", "Dashboard", 2),   # cuadrícula
            ("👤", "Perfil",    3),   # usuario
        ]

        self._nav_btns = {}
        for icon, name, row in nav_items:
            btn = ctk.CTkButton(
                self,
                text=icon,
                font=("Arial", 22),
                width=48,
                height=48,
                fg_color=COLORS["green"] if name == "Dashboard" else "transparent",
                hover_color=COLORS["green_glow"] if name != "Dashboard" else COLORS["green_dark"],
                text_color="#FFFFFF" if name == "Dashboard" else COLORS["text_sub"],
                corner_radius=12,
                command=lambda n=name: self._on_nav(n),
            )
            btn.grid(row=row, column=0, padx=12, pady=4)
            self._nav_btns[name] = btn

        self._active_btn = self._nav_btns["Dashboard"]

        # ── Settings al fondo ──────────────────────────────
        ctk.CTkButton(
            self,
            text="⚙",
            font=("Arial", 22),
            width=48,
            height=48,
            fg_color="transparent",
            hover_color=COLORS["bg"],
            text_color=COLORS["text_sub"],
            corner_radius=12,
        ).grid(row=11, column=0, padx=12, pady=(0, 16))

    def _on_nav(self, name):
        # Desactivar el anterior
        if self._active_btn:
            self._active_btn.configure(
                fg_color="transparent",
                text_color=COLORS["text_sub"],
                hover_color=COLORS["bg"],
            )
        # Activar el nuevo
        btn = self._nav_btns[name]
        btn.configure(
            fg_color=COLORS["green"],
            text_color="#FFFFFF",
            hover_color=COLORS["green_dark"],
        )
        self._active_btn = btn