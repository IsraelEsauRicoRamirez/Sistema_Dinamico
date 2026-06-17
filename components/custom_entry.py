# components/custom_entry.py
import customtkinter as ctk
from utils.theme import COLORS, FONTS, SIZES


class CustomEntry(ctk.CTkFrame):
    """
    Campo de entrada reutilizable con label y borde de focus.
    Uso:
        entry = CustomEntry(parent, label="Correo", placeholder="usuario@ejemplo.com")
        valor = entry.get()
    """

    def __init__(self, parent, label="", placeholder="", show="", **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)

        self._show = show

        # Label
        self.label = ctk.CTkLabel(
            self,
            text=label,
            font=FONTS["label"],
            text_color=COLORS["text_main"],
            anchor="w",
        )
        self.label.pack(fill="x", pady=(0, 5))

        # Input
        self.entry = ctk.CTkEntry(
            self,
            placeholder_text=placeholder,
            show=show,
            font=FONTS["input"],
            height=SIZES["input_height"],
            corner_radius=SIZES["corner_radius"],
            fg_color=COLORS["input_bg"],
            border_color=COLORS["border"],
            border_width=1,
            text_color=COLORS["text_main"],
            placeholder_text_color=COLORS["text_sub"],
        )
        self.entry.pack(fill="x")

        # Focus effects
        self.entry.bind("<FocusIn>",  self._on_focus)
        self.entry.bind("<FocusOut>", self._on_blur)

    def _on_focus(self, _event):
        self.entry.configure(border_color=COLORS["border_focus"], border_width=2)

    def _on_blur(self, _event):
        self.entry.configure(border_color=COLORS["border"], border_width=1)

    def get(self):
        return self.entry.get()

    def clear(self):
        self.entry.delete(0, "end")