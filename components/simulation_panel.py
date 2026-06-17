# components/simulation_panel.py
import customtkinter as ctk
from utils.theme import COLORS, FONTS, SIZES
from components.custom_entry import CustomEntry


class SimulationPanel(ctk.CTkFrame):
    """
    Panel izquierdo del dashboard.
    Muestra la fórmula, los parámetros y el botón de ejecución.
    Cambia su contenido según el modelo activo.
    """

    # Datos por modelo
    MODELOS_INFO = {
        "Modelo Exponencial": {
            "formula":     "dP/dt = r · P",
            "descripcion": "Crecimiento proporcional al tamaño\nactual sin restricciones ambientales.",
            "params": [
                ("Población Inicial (P₀)", "100"),
                ("Tasa de Crecimiento (r)", "0.1"),
                ("Tiempo (t)",             "50"),
            ],
        },
        "Modelo Logístico": {
            "formula":     "dP/dt = r · P(1 - P/K)",
            "descripcion": "Crecimiento limitado por la\ncapacidad de carga (K) del ecosistema.",
            "params": [
                ("Población Inicial (P₀)", "100"),
                ("Tasa de Crecimiento (r)", "0.1"),
                ("Capacidad de Carga (K)", "1000"),
                ("Tiempo (t)",             "50"),
            ],
        },
    }

    def __init__(self, parent, on_ejecutar=None, **kwargs):
        super().__init__(
            parent,
            width=310,
            fg_color=COLORS["bg"],
            corner_radius=0,
            **kwargs,
        )
        self.grid_propagate(False)
        self.on_ejecutar = on_ejecutar
        self._entries = {}
        self._modelo_actual = "Modelo Exponencial"
        self._build()

    # ──────────────────────────────────────────────────────────────────────────
    def _build(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Contenedor scrollable interno
        self._inner = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["text_sub"],
        )
        self._inner.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self._inner.grid_columnconfigure(0, weight=1)

        self._render_modelo(self._modelo_actual)

        # ── Botón Ejecutar (siempre visible al fondo) ──────
        btn_frame = ctk.CTkFrame(self, fg_color=COLORS["bg"])
        btn_frame.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 16))
        btn_frame.grid_columnconfigure(0, weight=1)

        self._btn_ejecutar = ctk.CTkButton(
            btn_frame,
            text="Ejecutar Simulación",
            font=FONTS["button"],
            height=SIZES["button_height"],
            corner_radius=SIZES["corner_radius"],
            fg_color=COLORS["green"],
            hover_color=COLORS["green_hover"],
            text_color="#FFFFFF",
            command=self._ejecutar,
        )
        self._btn_ejecutar.grid(row=0, column=0, sticky="ew")

    # ──────────────────────────────────────────────────────────────────────────
    def _render_modelo(self, modelo):
        """Limpia y reconstruye el panel según el modelo."""
        for widget in self._inner.winfo_children():
            widget.destroy()
        self._entries.clear()

        info = self.MODELOS_INFO[modelo]

        # ── Tarjeta de fórmula ─────────────────────────────
        formula_card = ctk.CTkFrame(
            self._inner,
            fg_color=COLORS["card"],
            corner_radius=16,
        )
        formula_card.grid(row=0, column=0, sticky="ew", padx=16, pady=(20, 0))
        formula_card.grid_columnconfigure(0, weight=1)

        # Header de la tarjeta
        hdr = ctk.CTkFrame(formula_card, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="w", padx=16, pady=(14, 4))

        ctk.CTkLabel(
            hdr,
            text="ƒ",
            font=("Arial", 18, "bold"),
            text_color=COLORS["green"],
            width=28,
            height=28,
            fg_color=COLORS["green_glow"],
            corner_radius=8,
        ).pack(side="left", padx=(0, 8))

        ctk.CTkLabel(
            hdr,
            text="Derivación Matemática",
            font=FONTS["label"],
            text_color=COLORS["text_main"],
        ).pack(side="left")

        # Fórmula
        formula_bg = ctk.CTkFrame(
            formula_card,
            fg_color=COLORS["bg"],
            corner_radius=10,
        )
        formula_bg.grid(row=1, column=0, sticky="ew", padx=16, pady=(4, 8))

        ctk.CTkLabel(
            formula_bg,
            text=info["formula"],
            font=("Arial", 15, "italic"),
            text_color=COLORS["text_main"],
        ).pack(padx=16, pady=10)

        # Descripción
        ctk.CTkLabel(
            formula_card,
            text=info["descripcion"],
            font=FONTS["subtitle"],
            text_color=COLORS["text_sub"],
            justify="center",
            wraplength=240,
        ).grid(row=2, column=0, padx=16, pady=(0, 14))

        # ── Separador "PARÁMETROS INICIALES" ──────────────
        ctk.CTkLabel(
            self._inner,
            text="PARÁMETROS INICIALES",
            font=("Arial", 10, "bold"),
            text_color=COLORS["text_sub"],
            anchor="w",
        ).grid(row=1, column=0, sticky="w", padx=16, pady=(20, 6))

        # ── Campos de parámetros ───────────────────────────
        for idx, (label, default) in enumerate(info["params"]):
            entry = CustomEntry(
                self._inner,
                label=label,
                placeholder=default,
            )
            entry.entry.insert(0, default)
            entry.grid(row=2 + idx, column=0, sticky="ew", padx=16, pady=(0, 12))
            self._entries[label] = entry

    # ──────────────────────────────────────────────────────────────────────────
    def cambiar_modelo(self, modelo):
        """Llamado desde el toggle para cambiar el modelo."""
        if modelo != self._modelo_actual:
            self._modelo_actual = modelo
            self._render_modelo(modelo)

    def _ejecutar(self):
        if self.on_ejecutar:
            valores = {k: v.get() for k, v in self._entries.items()}
            self.on_ejecutar(self._modelo_actual, valores)

    def get_valores(self):
        return {k: v.get() for k, v in self._entries.items()}