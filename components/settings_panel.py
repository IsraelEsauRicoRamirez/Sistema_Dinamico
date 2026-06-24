# components/settings_panel.py
import customtkinter as ctk
from utils.theme import COLORS, FONTS, SIZES


class SettingsPanel(ctk.CTkFrame):
    """Panel de configuración — sección del dashboard."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=COLORS["bg"], corner_radius=0, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self._build()

    def _build(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent",
                                         scrollbar_button_color=COLORS["border"])
        scroll.grid(row=0, column=0, sticky="nsew")
        scroll.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(scroll, text="Configuración",
                     font=FONTS["display"],
                     text_color=COLORS["text_main"],
                     anchor="w").grid(row=0, column=0, sticky="w",
                                       padx=28, pady=(24, 18))

        sections = [
            ("🎨  Apariencia", [
                ("Tema de la aplicación", "switch", True),
                ("Modo oscuro", "switch", False),
                ("Tamaño de fuente", "option", ["Normal","Grande","Pequeño"]),
            ]),
            ("📊  Simulación", [
                ("Precisión de cálculo", "option", ["Alta","Media","Baja"]),
                ("Guardar resultados automáticamente", "switch", True),
                ("Mostrar animación de gráfica", "switch", True),
            ]),
            ("🔔  Notificaciones", [
                ("Alertas de simulación completada", "switch", True),
                ("Correo al exportar CSV", "switch", False),
            ]),
            ("🌐  Idioma y región", [
                ("Idioma", "option", ["Español","English","Português"]),
                ("Formato de números", "option", ["1,000.00","1.000,00"]),
            ]),
        ]

        for sec_idx, (sec_title, items) in enumerate(sections):
            # Card de sección
            card = ctk.CTkFrame(scroll, fg_color=COLORS["card"],
                                 corner_radius=18,
                                 border_width=1, border_color=COLORS["border"])
            card.grid(row=sec_idx+1, column=0, sticky="ew",
                      padx=28, pady=(0, 14))
            card.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(card, text=sec_title,
                         font=FONTS["label"],
                         text_color=COLORS["text_sub"],
                         anchor="w").grid(row=0, column=0, sticky="w",
                                           padx=22, pady=(16,8))

            for item_idx, (label, kind, value) in enumerate(items):
                is_last = (item_idx == len(items) - 1)
                row_f = ctk.CTkFrame(card, fg_color="transparent")
                row_f.grid(row=item_idx+1, column=0, sticky="ew",
                           padx=22, pady=(0, 14 if is_last else 0))
                row_f.grid_columnconfigure(0, weight=1)

                ctk.CTkLabel(row_f, text=label,
                             font=FONTS["subtitle"],
                             text_color=COLORS["text_main"],
                             anchor="w").grid(row=0, column=0, sticky="w", pady=8)

                if kind == "switch":
                    sw = ctk.CTkSwitch(row_f, text="",
                                        onvalue=True, offvalue=False,
                                        progress_color=COLORS["green"],
                                        button_color=COLORS["card"],
                                        button_hover_color=COLORS["green_glow"])
                    if value:
                        sw.select()
                    sw.grid(row=0, column=1, sticky="e")

                elif kind == "option":
                    ctk.CTkOptionMenu(row_f,
                                       values=value,
                                       font=FONTS["subtitle"],
                                       height=36,
                                       corner_radius=10,
                                       fg_color=COLORS["input_bg"],
                                       button_color=COLORS["green"],
                                       button_hover_color=COLORS["green_hover"],
                                       dropdown_fg_color=COLORS["card"],
                                       text_color=COLORS["text_main"],
                                       ).grid(row=0, column=1, sticky="e")

                # Separador entre items (no el último)
                if not is_last:
                    ctk.CTkFrame(card, height=1,
                                 fg_color=COLORS["border"]).grid(
                        row=item_idx+2, column=0, sticky="ew", padx=22)

        # Zona peligrosa
        danger = ctk.CTkFrame(scroll, fg_color=COLORS["card"],
                               corner_radius=18,
                               border_width=1, border_color="#FECACA")
        danger.grid(row=len(sections)+1, column=0, sticky="ew",
                    padx=28, pady=(0, 28))
        danger.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(danger, text="⚠️  Zona peligrosa",
                     font=FONTS["label"],
                     text_color="#EF4444",
                     anchor="w").grid(row=0, column=0, sticky="w",
                                       padx=22, pady=(16,8))

        row_d = ctk.CTkFrame(danger, fg_color="transparent")
        row_d.grid(row=1, column=0, sticky="ew", padx=22, pady=(0,18))
        row_d.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(row_d,
                     text="Eliminar cuenta permanentemente. Esta acción no se puede deshacer.",
                     font=FONTS["subtitle"],
                     text_color=COLORS["text_sub"],
                     anchor="w").grid(row=0, column=0, sticky="w")

        ctk.CTkButton(row_d, text="Eliminar cuenta",
                      font=FONTS["label"],
                      height=36, corner_radius=10,
                      fg_color="transparent",
                      border_width=1, border_color="#EF4444",
                      hover_color="#FEF2F2",
                      text_color="#EF4444",
                      ).grid(row=0, column=1, sticky="e", padx=(16,0))