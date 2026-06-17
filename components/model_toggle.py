# components/model_toggle.py
import customtkinter as ctk
from utils.theme import COLORS, FONTS


class ModelToggle(ctk.CTkFrame):
    """
    Toggle pill que alterna entre 'Modelo Exponencial' y 'Modelo Logístico'.
    Llama a on_change(modelo: str) cuando cambia.
    """

    MODELOS = ["Modelo Exponencial", "Modelo Logístico"]

    def __init__(self, parent, on_change=None, **kwargs):
        super().__init__(
            parent,
            fg_color=COLORS["bg"],
            corner_radius=20,
            border_width=1,
            border_color=COLORS["border"],
            **kwargs,
        )
        self.on_change = on_change
        self._active = self.MODELOS[0]
        self._btns = {}
        self._build()

    def _build(self):
        for i, modelo in enumerate(self.MODELOS):
            btn = ctk.CTkButton(
                self,
                text=modelo,
                font=FONTS["label"],
                height=36,
                corner_radius=16,
                fg_color=COLORS["green"] if i == 0 else "transparent",
                hover_color=COLORS["green_dark"] if i == 0 else COLORS["border"],
                text_color="#FFFFFF" if i == 0 else COLORS["text_sub"],
                command=lambda m=modelo: self._select(m),
            )
            btn.grid(row=0, column=i, padx=4, pady=4)
            self._btns[modelo] = btn

    def _select(self, modelo):
        if modelo == self._active:
            return
        # Desactivar anterior
        prev = self._btns[self._active]
        prev.configure(
            fg_color="transparent",
            text_color=COLORS["text_sub"],
            hover_color=COLORS["border"],
        )
        # Activar nuevo
        self._active = modelo
        curr = self._btns[modelo]
        curr.configure(
            fg_color=COLORS["green"],
            text_color="#FFFFFF",
            hover_color=COLORS["green_dark"],
        )
        if self.on_change:
            self.on_change(modelo)

    def get(self):
        return self._active