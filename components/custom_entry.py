import customtkinter as ctk
from utils.theme import COLORS, FONTS, SIZES


class CustomEntry(ctk.CTkFrame):
    def __init__(self, parent, label="", placeholder="", show="",
                 unit="", tooltip="", **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self._show = show
        self.grid_columnconfigure(0, weight=1)

        if label:
            lbl_frame = ctk.CTkFrame(self, fg_color="transparent")
            lbl_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
            lbl_frame.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(
                lbl_frame, text=label,
                font=FONTS["label"],
                text_color=COLORS["text_main"],
                anchor="w",
            ).grid(row=0, column=0, sticky="w")

            if unit:
                ctk.CTkLabel(
                    lbl_frame,
                    text=unit,
                    font=("Arial", 11, "normal"),
                    text_color=COLORS["green_dark"],
                    fg_color=COLORS["green_glow"],
                    corner_radius=6,
                ).grid(row=0, column=1, sticky="e", padx=(6, 0))

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
            placeholder_text_color=COLORS["text_hint"],
        )
        self.entry.grid(row=1, column=0, sticky="ew")

        if tooltip:
            tip = ctk.CTkLabel(
                self, text=f"ⓘ  {tooltip}",
                font=("Arial", 10, "normal"),
                text_color=COLORS["text_hint"],
                anchor="w",
                wraplength=260,
                justify="left",
            )
            tip.grid(row=2, column=0, sticky="w", pady=(3, 0))

        self.entry.bind("<FocusIn>",  self._on_focus)
        self.entry.bind("<FocusOut>", self._on_blur)

    def _on_focus(self, _):
        self.entry.configure(border_color=COLORS["border_focus"],
                             border_width=2, fg_color=COLORS["card"])

    def _on_blur(self, _):
        self.entry.configure(border_color=COLORS["border"],
                             border_width=1, fg_color=COLORS["input_bg"])

    def get(self):
        return self.entry.get()

    def clear(self):
        self.entry.delete(0, "end")

    def insert(self, index, value):
        self.entry.insert(index, value)