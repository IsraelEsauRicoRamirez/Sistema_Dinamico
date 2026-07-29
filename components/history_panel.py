import customtkinter as ctk
from utils.theme import COLORS, FONTS

# Datos de ejemplo para el historial
SAMPLE_HISTORY = [
    {"modelo": "Modelo Exponencial", "fecha": "23 Jun 2026  10:42", "p0": "100", "r": "0.1", "t": "50", "resultado": "14,841"},
    {"modelo": "Modelo Logístico",   "fecha": "23 Jun 2026  09:15", "p0": "100", "r": "0.3", "t": "30", "resultado": "873"},
    {"modelo": "Modelo Exponencial", "fecha": "22 Jun 2026  18:03", "p0": "500", "r": "0.05","t": "100","resultado": "7,389"},
    {"modelo": "Modelo Logístico",   "fecha": "22 Jun 2026  14:50", "p0": "200", "r": "0.2", "t": "50", "resultado": "980"},
    {"modelo": "Modelo Exponencial", "fecha": "21 Jun 2026  11:27", "p0": "50",  "r": "0.15","t": "40", "resultado": "1,001"},
]

class HistoryPanel(ctk.CTkFrame):
    """Panel de historial de simulaciones — sección del dashboard."""

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

        # Encabezado
        hdr = ctk.CTkFrame(scroll, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=28, pady=(24, 0))
        hdr.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(hdr, text="Historial de Simulaciones",
                     font=FONTS["display"],
                     text_color=COLORS["text_main"],
                     anchor="w").grid(row=0, column=0, sticky="w")

        ctk.CTkButton(hdr, text="⬇ Exportar todo",
                      font=FONTS["caption"],
                      height=34, corner_radius=10,
                      fg_color="transparent",
                      border_width=1, border_color=COLORS["border"],
                      hover_color=COLORS["bg"],
                      text_color=COLORS["green_dark"],
                      ).grid(row=0, column=1, sticky="e")

        # Stat cards
        stats = ctk.CTkFrame(scroll, fg_color="transparent")
        stats.grid(row=1, column=0, sticky="ew", padx=28, pady=(18, 0))
        stats.grid_columnconfigure((0,1,2), weight=1)

        stat_data = [
            ("5", "Simulaciones totales", "📊"),
            ("2", "Modelos distintos",    "🔢"),
            ("23 Jun", "Última ejecución","📅"),
        ]
        
        for i, (val, lbl, icon) in enumerate(stat_data):
            card = ctk.CTkFrame(stats, fg_color=COLORS["card"],
                                corner_radius=14,
                                border_width=1, border_color=COLORS["border"])
            card.grid(row=0, column=i, sticky="ew",
                      padx=(0,10) if i<2 else 0)
            card.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(card, text=icon, font=("Arial", 22)).grid(
                row=0, column=0, pady=(16,4))
            ctk.CTkLabel(card, text=val,
                         font=("Arial", 24, "bold"),
                         text_color=COLORS["text_main"]).grid(row=1, column=0)
            ctk.CTkLabel(card, text=lbl,
                         font=FONTS["caption"],
                         text_color=COLORS["text_sub"]).grid(row=2, column=0, pady=(2,14))

        # Tabla de historial
        table_card = ctk.CTkFrame(scroll, fg_color=COLORS["card"],
                                  corner_radius=18,
                                  border_width=1, border_color=COLORS["border"])
        table_card.grid(row=2, column=0, sticky="ew", padx=28, pady=(18, 28))
        table_card.grid_columnconfigure(0, weight=1)

        # Header tabla
        cols_hdr = ctk.CTkFrame(table_card, fg_color=COLORS["surface"],
                                corner_radius=10)
        cols_hdr.grid(row=0, column=0, sticky="ew", padx=16, pady=(16,0))
        cols_hdr.grid_columnconfigure((0,1,2,3,4), weight=1)

        for i, col in enumerate(["MODELO","FECHA","P₀","r","RESULTADO"]):
            ctk.CTkLabel(cols_hdr, text=col,
                         font=("Arial", 9, "bold"),
                         text_color=COLORS["text_hint"],
                         anchor="w").grid(row=0, column=i, padx=14, pady=8, sticky="w")

        # Filas
        for idx, entry in enumerate(SAMPLE_HISTORY):
            row_bg = COLORS["card"] if idx % 2 == 0 else COLORS["surface"]
            row_f = ctk.CTkFrame(table_card, fg_color=row_bg, corner_radius=0)
            row_f.grid(row=idx+1, column=0, sticky="ew", padx=16, pady=0)
            row_f.grid_columnconfigure((0,1,2,3,4), weight=1)

            # Badge de modelo con color
            badge_color = COLORS["green_glow"] if "Expo" in entry["modelo"] else "#EFF6FF"
            badge_text_color = COLORS["green_dark"] if "Expo" in entry["modelo"] else "#3B82F6"

            badge = ctk.CTkLabel(row_f,
                                 text=f"  {entry['modelo']}  ",
                                 font=("Arial", 10, "bold"),
                                 text_color=badge_text_color,
                                 fg_color=badge_color,
                                 corner_radius=8)
            badge.grid(row=0, column=0, padx=14, pady=10, sticky="w")

            for col, key in [(1,"fecha"),(2,"p0"),(3,"r"),(4,"resultado")]:
                ctk.CTkLabel(row_f, text=entry[key],
                             font=FONTS["subtitle"],
                             text_color=COLORS["text_main"] if col==4 else COLORS["text_sub"],
                             anchor="w").grid(row=0, column=col, padx=14, sticky="w")

        # Separador final redondeado
        ctk.CTkFrame(table_card, height=1,
                     fg_color=COLORS["border"]).grid(
            row=len(SAMPLE_HISTORY)+1, column=0, sticky="ew", padx=16, pady=(0,14))