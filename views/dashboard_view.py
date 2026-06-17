# views/dashboard_view.py
import customtkinter as ctk
from utils.theme import COLORS, FONTS
from components.sidebar import Sidebar
from components.model_toggle import ModelToggle
from components.simulation_panel import SimulationPanel


class DashboardView(ctk.CTkFrame):
    """
    Vista principal del simulador.
    Recibe user_data = {"nombre": str, "rol": str} para mostrar en el header.
    """

    def __init__(self, parent, user_data=None, **kwargs):
        super().__init__(parent, fg_color=COLORS["bg"], corner_radius=0, **kwargs)
        self.user_data = user_data or {"nombre": "Juan Pérez", "rol": "Estudiante"}
        self._build()

    # ──────────────────────────────────────────────────────────────────────────
    def _build(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # ── Sidebar ────────────────────────────────────────
        self.sidebar = Sidebar(self)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")

        # ── Header ─────────────────────────────────────────
        self._build_header()

        # ── Área principal ─────────────────────────────────
        main = ctk.CTkFrame(self, fg_color=COLORS["bg"], corner_radius=0)
        main.grid(row=1, column=1, sticky="nsew", padx=0, pady=0)
        main.grid_rowconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=1)

        # Panel izquierdo de parámetros
        self.sim_panel = SimulationPanel(
            main,
            on_ejecutar=self._on_ejecutar,
        )
        self.sim_panel.grid(row=0, column=0, sticky="nsew")

        # Separador vertical
        ctk.CTkFrame(main, width=1, fg_color=COLORS["border"]).grid(
            row=0, column=1, sticky="ns"
        )

        # Panel derecho: gráfica + tabla (placeholder)
        self._build_right_panel(main)

    # ──────────────────────────────────────────────────────────────────────────
    def _build_header(self):
        header = ctk.CTkFrame(
            self,
            height=68,
            fg_color=COLORS["card"],
            corner_radius=0,
        )
        header.grid(row=0, column=1, sticky="ew")
        header.grid_propagate(False)
        header.grid_columnconfigure(1, weight=1)

        # Título
        ctk.CTkLabel(
            header,
            text="Simulador Poblacional",
            font=FONTS["title"],
            text_color=COLORS["text_main"],
        ).grid(row=0, column=0, padx=24, pady=0, sticky="w")

        # Toggle de modelos (centro)
        self.toggle = ModelToggle(
            header,
            on_change=self._on_modelo_change,
        )
        self.toggle.grid(row=0, column=1, padx=0, pady=0)

        # Perfil de usuario (derecha)
        profile = ctk.CTkFrame(header, fg_color="transparent")
        profile.grid(row=0, column=2, padx=24, pady=0, sticky="e")

        ctk.CTkLabel(
            profile,
            text=self.user_data["nombre"],
            font=FONTS["label"],
            text_color=COLORS["text_main"],
            anchor="e",
        ).grid(row=0, column=0, sticky="e")

        ctk.CTkLabel(
            profile,
            text=self.user_data["rol"],
            font=FONTS["subtitle"],
            text_color=COLORS["text_sub"],
            anchor="e",
        ).grid(row=1, column=0, sticky="e")

        # Avatar (círculo con inicial)
        avatar = ctk.CTkLabel(
            profile,
            text=self.user_data["nombre"][0].upper(),
            font=("Arial", 16, "bold"),
            width=42,
            height=42,
            fg_color=COLORS["green"],
            text_color="#FFFFFF",
            corner_radius=21,
        )
        avatar.grid(row=0, column=1, rowspan=2, padx=(12, 0))

        # Separador horizontal bajo el header
        ctk.CTkFrame(self, height=1, fg_color=COLORS["border"]).grid(
            row=0, column=1, sticky="sew"
        )

    # ──────────────────────────────────────────────────────────────────────────
    def _build_right_panel(self, parent):
        right = ctk.CTkFrame(parent, fg_color=COLORS["bg"], corner_radius=0)
        right.grid(row=0, column=2, sticky="nsew", padx=0, pady=0)
        right.grid_rowconfigure(0, weight=3)
        right.grid_rowconfigure(1, weight=2)
        right.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(2, weight=1)

        # ── Gráfica placeholder ────────────────────────────
        self._chart_frame = ctk.CTkFrame(
            right,
            fg_color=COLORS["card"],
            corner_radius=16,
        )
        self._chart_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=(20, 10))
        self._chart_frame.grid_rowconfigure(1, weight=1)
        self._chart_frame.grid_columnconfigure(0, weight=1)

        # Header de la gráfica
        chart_hdr = ctk.CTkFrame(self._chart_frame, fg_color="transparent")
        chart_hdr.grid(row=0, column=0, sticky="w", padx=20, pady=(16, 0))

        ctk.CTkFrame(
            chart_hdr, width=4, height=22,
            fg_color=COLORS["green"], corner_radius=2,
        ).pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            chart_hdr,
            text="Gráfica Dinámica",
            font=FONTS["title"],
            text_color=COLORS["text_main"],
        ).pack(side="left")

        # Área donde irá matplotlib (canvas placeholder)
        self.chart_area = ctk.CTkFrame(
            self._chart_frame,
            fg_color=COLORS["bg"],
            corner_radius=10,
        )
        self.chart_area.grid(row=1, column=0, sticky="nsew", padx=16, pady=(12, 16))

        self._chart_placeholder = ctk.CTkLabel(
            self.chart_area,
            text="Configura los parámetros y\npulsa 'Ejecutar Simulación'",
            font=FONTS["subtitle"],
            text_color=COLORS["text_sub"],
        )
        self._chart_placeholder.place(relx=.5, rely=.5, anchor="center")

        # ── Tabla de datos placeholder ─────────────────────
        self._table_frame = ctk.CTkFrame(
            right,
            fg_color=COLORS["card"],
            corner_radius=16,
        )
        self._table_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self._table_frame.grid_rowconfigure(1, weight=1)
        self._table_frame.grid_columnconfigure(0, weight=1)

        # Header tabla
        tbl_hdr = ctk.CTkFrame(self._table_frame, fg_color="transparent")
        tbl_hdr.grid(row=0, column=0, sticky="ew", padx=20, pady=(16, 0))
        tbl_hdr.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            tbl_hdr,
            text="Datos Obtenidos",
            font=FONTS["title"],
            text_color=COLORS["text_main"],
            anchor="w",
        ).grid(row=0, column=0, sticky="w")

        # Botón CSV
        ctk.CTkButton(
            tbl_hdr,
            text="⬇  Descargar CSV",
            font=FONTS["label"],
            height=34,
            corner_radius=10,
            fg_color="transparent",
            border_width=1,
            border_color=COLORS["border"],
            hover_color=COLORS["bg"],
            text_color=COLORS["green_dark"],
        ).grid(row=0, column=1, sticky="e")

        # Cabecera de la tabla
        cols_frame = ctk.CTkFrame(
            self._table_frame, fg_color=COLORS["bg"], corner_radius=8
        )
        cols_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(12, 0))
        cols_frame.grid_columnconfigure((0, 1), weight=1)

        for i, col in enumerate(["TIEMPO (T)", "POBLACIÓN (P)"]):
            ctk.CTkLabel(
                cols_frame,
                text=col,
                font=("Arial", 10, "bold"),
                text_color=COLORS["text_sub"],
                anchor="w",
            ).grid(row=0, column=i, padx=20, pady=8, sticky="w")

        # Cuerpo de la tabla (scrollable)
        self._table_body = ctk.CTkScrollableFrame(
            self._table_frame,
            fg_color="transparent",
            scrollbar_button_color=COLORS["border"],
        )
        self._table_body.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 16))
        self._table_body.grid_columnconfigure((0, 1), weight=1)

        self._table_placeholder = ctk.CTkLabel(
            self._table_body,
            text="Sin datos aún.",
            font=FONTS["subtitle"],
            text_color=COLORS["text_sub"],
        )
        self._table_placeholder.grid(row=0, column=0, columnspan=2, pady=20)

    # ──────────────────────────────────────────────────────────────────────────
    def _on_modelo_change(self, modelo):
        """El toggle cambió de modelo → actualizar el panel de parámetros."""
        self.sim_panel.cambiar_modelo(modelo)

    def _on_ejecutar(self, modelo, valores):
        """
        Se llamará cuando el usuario pulse 'Ejecutar Simulación'.
        Por ahora solo imprime — aquí conectarás la lógica de simulación.
        """
        print(f"[Dashboard] Ejecutar: {modelo}")
        print(f"[Dashboard] Valores: {valores}")