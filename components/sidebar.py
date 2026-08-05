import customtkinter as ctk
from utils.theme import COLORS, FONTS, SIZES


class Sidebar(ctk.CTkFrame):
    # Íconos: ∫ (integral) para el simulador, 👤 perfil, 📊 historial
    NAV_ITEMS = [
        ("∫",  "simulador",  "Simulador"),
        ("👤", "perfil",     "Mi Perfil"),
        ("📊", "historial",  "Historial"),
    ]

    def __init__(self, parent, on_navigate=None, **kwargs):
        super().__init__(parent,
                         width=SIZES["sidebar_w"],
                         fg_color=COLORS["card"],
                         corner_radius=0,
                         **kwargs)
        self.grid_propagate(False)
        self.on_navigate = on_navigate
        self._expanded   = False
        self._active     = "simulador"
        self._nav_btns   = {}
        self._build()

    def _build(self):
        self.grid_rowconfigure(10, weight=1)
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkFrame(self, width=1, fg_color=COLORS["border"]).grid(
            row=0, column=1, rowspan=20, sticky="ns")

        self._ham = ctk.CTkButton(
            self, text="☰", font=("Arial", 20),
            width=46, height=46,
            fg_color="transparent", hover_color=COLORS["bg"],
            text_color=COLORS["text_main"], corner_radius=10,
            command=self._toggle)
        self._ham.grid(row=0, column=0, padx=13, pady=(16,6), sticky="w")

        ctk.CTkFrame(self, height=1, fg_color=COLORS["border"]).grid(
            row=1, column=0, sticky="ew", padx=13, pady=(0,10))

        for idx, (icon, key, label) in enumerate(self.NAV_ITEMS):
            active = (key == self._active)
            frame = ctk.CTkFrame(self, fg_color="transparent")
            frame.grid(row=2+idx, column=0, sticky="ew", padx=10, pady=3)
            frame.grid_columnconfigure(1, weight=1)

            # El ícono ∫ del simulador necesita una fuente serif para verse bien
            icon_font = ("Georgia", 26, "bold") if icon == "∫" else ("Arial", 21)
            btn = ctk.CTkButton(
                frame, text=icon, font=icon_font,
                width=46, height=46,
                fg_color=COLORS["green_subtle"] if active else "transparent",
                hover_color=COLORS["green_subtle"],
                text_color=COLORS["green"] if active else COLORS["text_sub"],
                corner_radius=10,
                command=lambda k=key: self._on_nav(k))
            btn.grid(row=0, column=0)

            lbl = ctk.CTkLabel(frame, text=label,
                               font=FONTS["label"],
                               text_color=COLORS["green"] if active else COLORS["text_sub"],
                               anchor="w")
            # Los labels arrancan OCULTOS — solo se muestran al expandir con ☰
            # (NO llamar a lbl.grid() aquí)
            self._nav_btns[key] = (frame, btn, lbl)

        self._settings_frame = ctk.CTkFrame(self, fg_color="transparent")
        self._settings_frame.grid(row=11, column=0, sticky="ew",
                                   padx=10, pady=(0,18))
        self._settings_frame.grid_columnconfigure(1, weight=1)

        self._settings_btn = ctk.CTkButton(
            self._settings_frame, text="⚙", font=("Arial", 21),
            width=46, height=46,
            fg_color="transparent", hover_color=COLORS["green_subtle"],
            text_color=COLORS["text_sub"], corner_radius=10,
            command=lambda: self._on_nav("configuracion"))
        self._settings_btn.grid(row=0, column=0)

        self._settings_lbl = ctk.CTkLabel(
            self._settings_frame, text="Configuración",
            font=FONTS["label"],
            text_color=COLORS["text_sub"], anchor="w")

    def _toggle(self):
        self._expanded = not self._expanded
        new_w = SIZES["sidebar_w_exp"] if self._expanded else SIZES["sidebar_w"]
        self.configure(width=new_w)
        for key, (frame, btn, lbl) in self._nav_btns.items():
            if self._expanded:
                lbl.grid(row=0, column=1, sticky="w", padx=(8,0))
            else:
                lbl.grid_forget()
        if self._expanded:
            self._settings_lbl.grid(row=0, column=1, sticky="w", padx=(8,0))
        else:
            self._settings_lbl.grid_forget()

    def _on_nav(self, key):
        prev = self._active
        if prev in self._nav_btns:
            _, pb, pl = self._nav_btns[prev]
            pb.configure(fg_color="transparent", text_color=COLORS["text_sub"])
            pl.configure(text_color=COLORS["text_sub"])
        elif prev == "configuracion":
            self._settings_btn.configure(fg_color="transparent",
                                          text_color=COLORS["text_sub"])
        
        self._active = key
        
        if key in self._nav_btns:
            _, nb, nl = self._nav_btns[key]
            nb.configure(fg_color=COLORS["green_subtle"],
                          text_color=COLORS["green"])
            nl.configure(text_color=COLORS["green"])
        elif key == "configuracion":
            self._settings_btn.configure(fg_color=COLORS["green_subtle"],
                                          text_color=COLORS["green"])
        
        if self.on_navigate:
            self.on_navigate(key)