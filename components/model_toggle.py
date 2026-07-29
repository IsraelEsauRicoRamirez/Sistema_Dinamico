import customtkinter as ctk
from utils.theme import COLORS, FONTS


class ModelToggle(ctk.CTkFrame):
    MODELOS = ["Modelo Exponencial", "Modelo Logístico"]

    def __init__(self, parent, on_change=None, **kwargs):
        super().__init__(parent,
                         fg_color=COLORS["bg"],
                         corner_radius=22,
                         border_width=1,
                         border_color=COLORS["border"],
                         **kwargs)
        self.on_change = on_change
        self._active   = self.MODELOS[0]
        self._btns     = {}
        self._build()

    def _build(self):
        self.grid_columnconfigure((0,1), weight=1)
        for i, modelo in enumerate(self.MODELOS):
            active = (i == 0)
            btn = ctk.CTkButton(
                self, text=modelo,
                font=("Arial", 13, "bold") if active else FONTS["label"],
                height=40, corner_radius=18,
                fg_color=COLORS["green"] if active else "transparent",
                hover_color=COLORS["green_dark"] if active else COLORS["border"],
                text_color="#FFFFFF" if active else COLORS["text_sub"],
                command=lambda m=modelo: self._select(m))
            btn.grid(row=0, column=i, padx=4, pady=4, sticky="ew")
            self._btns[modelo] = btn

    def _select(self, modelo):
        if modelo == self._active:
            return
        
        # Desactivar el botón previo
        prev = self._btns[self._active]
        prev.configure(fg_color="transparent",
                       text_color=COLORS["text_sub"],
                       hover_color=COLORS["border"],
                       font=FONTS["label"])
        
        # Activar el nuevo botón
        self._active = modelo
        curr = self._btns[modelo]
        curr.configure(fg_color=COLORS["green"],
                       text_color="#FFFFFF",
                       hover_color=COLORS["green_dark"],
                       font=("Arial", 13, "bold"))
        
        # Disparar el evento
        if self.on_change:
            self.on_change(modelo)

    def get(self):
        return self._active