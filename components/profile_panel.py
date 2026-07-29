import customtkinter as ctk
from utils.theme import COLORS, FONTS, SIZES
from components.custom_entry import CustomEntry


class ProfilePanel(ctk.CTkFrame):
    """Panel de perfil de usuario — sección del dashboard."""

    def __init__(self, parent, user_data=None, **kwargs):
        super().__init__(parent, fg_color=COLORS["bg"], corner_radius=0, **kwargs)
        base = user_data or {}
        self.user_data = {
            "nombre":    base.get("nombre",    "Juan Pérez"),
            "rol":       base.get("rol",       "Alumno"),
            "matricula": base.get("matricula", "A01234567"),
            "correo":    base.get("correo",    "juan@ejemplo.com"),
        }
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self._build()

    def _build(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent",
                                        scrollbar_button_color=COLORS["border"])
        scroll.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        scroll.grid_columnconfigure(0, weight=1)

        # Título de sección
        hdr = ctk.CTkFrame(scroll, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="w", padx=28, pady=(24, 0))
        ctk.CTkLabel(hdr, text="Mi Perfil",
                     font=FONTS["display"],
                     text_color=COLORS["text_main"]).pack(side="left")

        # ── Card avatar + nombre ───────────────────────────
        hero = ctk.CTkFrame(scroll, fg_color=COLORS["card"],
                            corner_radius=18,
                            border_width=1, border_color=COLORS["border"])
        hero.grid(row=1, column=0, sticky="ew", padx=28, pady=(18, 0))
        hero.grid_columnconfigure(1, weight=1)

        # Avatar grande (con validación de seguridad por si el nombre está vacío)
        nombre_actual = self.user_data.get("nombre", "Usuario")
        initial = nombre_actual[0].upper() if nombre_actual else "U"
        
        ctk.CTkLabel(hero, text=initial,
                     font=("Arial", 36, "bold"),
                     width=88, height=88,
                     fg_color=COLORS["green"],
                     text_color="#FFFFFF",
                     corner_radius=44).grid(row=0, column=0, rowspan=2,
                                            padx=28, pady=28)

        ctk.CTkLabel(hero, text=nombre_actual,
                     font=("Arial", 20, "bold"),
                     text_color=COLORS["text_main"],
                     anchor="w").grid(row=0, column=1, sticky="sw", pady=(28,2))

        # Badge rol
        ctk.CTkLabel(hero,
                     text=f"  {self.user_data['rol']}  ",
                     font=FONTS["small"],
                     text_color=COLORS["green_dark"],
                     fg_color=COLORS["green_glow"],
                     corner_radius=8).grid(row=1, column=1, sticky="nw", pady=(0,28))

        # ── Card datos editables ───────────────────────────
        data_card = ctk.CTkFrame(scroll, fg_color=COLORS["card"],
                                 corner_radius=18,
                                 border_width=1, border_color=COLORS["border"])
        data_card.grid(row=2, column=0, sticky="ew", padx=28, pady=(16, 0))
        data_card.grid_columnconfigure((0,1), weight=1)

        ctk.CTkLabel(data_card, text="Información de la cuenta",
                     font=FONTS["label"],
                     text_color=COLORS["text_sub"],
                     anchor="w").grid(row=0, column=0, columnspan=2,
                                      padx=24, pady=(18,10), sticky="w")

        # Campos en dos columnas
        fields = [
            ("Nombre completo", self.user_data["nombre"], 1, 0),
            ("Matrícula / ID",  self.user_data["matricula"], 1, 1),
            ("Correo electrónico", self.user_data["correo"], 2, 0),
            ("Rol",             self.user_data["rol"], 2, 1),
        ]

        for label, val, row, col in fields:
            e = CustomEntry(data_card, label=label, placeholder=val)
            if val: # Validación para no intentar insertar un NoneType
                e.insert(0, val)
            e.grid(row=row, column=col, sticky="ew",
                   padx=(24 if col==0 else 8, 8 if col==0 else 24),
                   pady=(0, 16))

        # Botón guardar
        ctk.CTkButton(data_card, text="Guardar cambios",
                      font=FONTS["button"],
                      height=SIZES["button_height"],
                      corner_radius=SIZES["corner_radius"],
                      fg_color=COLORS["green"],
                      hover_color=COLORS["green_hover"],
                      text_color="#FFFFFF"
                      ).grid(row=3, column=0, columnspan=2,
                             padx=24, pady=(0, 24), sticky="ew")

        # ── Card cambio de contraseña ──────────────────────
        pw_card = ctk.CTkFrame(scroll, fg_color=COLORS["card"],
                               corner_radius=18,
                               border_width=1, border_color=COLORS["border"])
        pw_card.grid(row=3, column=0, sticky="ew", padx=28, pady=(16, 28))
        pw_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(pw_card, text="Cambiar contraseña",
                     font=FONTS["label"],
                     text_color=COLORS["text_sub"],
                     anchor="w").grid(row=0, column=0, padx=24, pady=(18,10), sticky="w")

        for i, lbl in enumerate(["Contraseña actual", "Nueva contraseña", "Confirmar contraseña"]):
            CustomEntry(pw_card, label=lbl,
                        placeholder="••••••••", show="•").grid(
                row=i+1, column=0, sticky="ew", padx=24, pady=(0,12))

        ctk.CTkButton(pw_card, text="Actualizar contraseña",
                      font=FONTS["button"],
                      height=SIZES["button_height"],
                      corner_radius=SIZES["corner_radius"],
                      fg_color=COLORS["green"],
                      hover_color=COLORS["green_hover"],
                      text_color="#FFFFFF"
                      ).grid(row=4, column=0, padx=24, pady=(0,24), sticky="ew")