# views/dashboard_view.py
import tkinter as tk
import customtkinter as ctk

from utils.theme import COLORS, FONTS, SIZES
from components.sidebar import Sidebar
from components.model_toggle import ModelToggle
from components.simulation_panel import SimulationPanel
from components.profile_panel import ProfilePanel
from components.history_panel import HistoryPanel
from components.settings_panel import SettingsPanel

# matplotlib integrado en tkinter
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ── Logo pequeño ──────────────────────────────────────────────────────────────
def draw_logo_small(parent, size=28, bg=None):
    bg = bg or COLORS["card"]
    scale = size / 100
    c = tk.Canvas(parent, width=size, height=size, highlightthickness=0, bg=bg)
    c.create_rectangle(0, 0, size, size, fill="#F4F4F5", outline="")
    def sc(v): return int(v * scale)
    c.create_line(sc(25),sc(75),sc(50),sc(45),sc(75),sc(45),
                  fill="#22c55e",width=max(2,int(5*scale)),capstyle="round",joinstyle="round")
    c.create_line(sc(25),sc(75),sc(60),sc(75),sc(75),sc(45),
                  fill="#d4d4d8",width=max(1,int(4*scale)),capstyle="round",joinstyle="round")
    c.create_line(sc(50),sc(45),sc(60),sc(75),fill="#e4e4e7",width=1)
    def oval(cx,cy,r,fill):
        cx,cy,r=sc(cx),sc(cy),max(2,int(r*scale))
        c.create_oval(cx-r,cy-r,cx+r,cy+r,fill=fill,outline="")
    oval(25,75,7,"#18181b"); oval(50,45,6,"#71717a"); oval(60,75,5,"#a1a1aa")
    oval(75,45,9,"#22c55e"); oval(75,45,3,"#ffffff")
    return c


# ══════════════════════════════════════════════════════════════════════════════
class SimulatorSection(ctk.CTkFrame):
    """Sección simulador: panel izquierdo + gráfica matplotlib + tabla."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=COLORS["bg"], corner_radius=0, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self._mpl_canvas   = None   # FigureCanvasTkAgg
        self._table_rows   = []     # widgets de la tabla
        self._modelo_label = "Modelo Exponencial"
        self._build()

    # ─────────────────────────────────────────────────────────────────────────
    def _build(self):
        # Panel izquierdo
        self.sim_panel = SimulationPanel(self, on_result=self._on_result)
        self.sim_panel.grid(row=0, column=0, sticky="nsew")

        # Panel derecho
        right = ctk.CTkFrame(self, fg_color=COLORS["bg"], corner_radius=0)
        right.grid(row=0, column=1, sticky="nsew")
        right.grid_rowconfigure(0, weight=3)
        right.grid_rowconfigure(1, weight=2)
        right.grid_columnconfigure(0, weight=1)

        # ── Card gráfica ──────────────────────────────────
        self._chart_card = ctk.CTkFrame(right, fg_color=COLORS["card"],
                                         corner_radius=16,
                                         border_width=1, border_color=COLORS["border"])
        self._chart_card.grid(row=0, column=0, sticky="nsew", padx=16, pady=(16,8))
        self._chart_card.grid_rowconfigure(1, weight=1)
        self._chart_card.grid_columnconfigure(0, weight=1)

        # Header gráfica
        ch = ctk.CTkFrame(self._chart_card, fg_color="transparent")
        ch.grid(row=0, column=0, sticky="ew", padx=20, pady=(14, 0))

        ctk.CTkFrame(ch, width=3, height=20,
                     fg_color=COLORS["green"], corner_radius=2).pack(side="left", padx=(0,10))

        self._chart_title = ctk.CTkLabel(ch, text="Gráfica Dinámica",
                                          font=FONTS["title"],
                                          text_color=COLORS["text_main"])
        self._chart_title.pack(side="left")

        # Área matplotlib
        self._chart_area = ctk.CTkFrame(self._chart_card,
                                         fg_color="#FFFFFF",
                                         corner_radius=10)
        self._chart_area.grid(row=1, column=0, sticky="nsew", padx=14, pady=(8,14))
        self._chart_area.grid_rowconfigure(0, weight=1)
        self._chart_area.grid_columnconfigure(0, weight=1)

        # Placeholder inicial
        self._placeholder = ctk.CTkLabel(
            self._chart_area,
            text="📈\n\nConfigura los parámetros y\npulsa  ▶ Ejecutar Simulación",
            font=FONTS["subtitle"],
            text_color=COLORS["text_hint"],
            justify="center")
        self._placeholder.place(relx=.5, rely=.5, anchor="center")

        # ── Card tabla ────────────────────────────────────
        table_card = ctk.CTkFrame(right, fg_color=COLORS["card"],
                                   corner_radius=16,
                                   border_width=1, border_color=COLORS["border"])
        table_card.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0,16))
        table_card.grid_rowconfigure(2, weight=1)
        table_card.grid_columnconfigure(0, weight=1)

        # Header tabla
        th = ctk.CTkFrame(table_card, fg_color="transparent")
        th.grid(row=0, column=0, sticky="ew", padx=20, pady=(14,0))
        th.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(th, text="Datos Obtenidos",
                     font=FONTS["title"],
                     text_color=COLORS["text_main"],
                     anchor="w").grid(row=0, column=0, sticky="w")

        self._csv_btn = ctk.CTkButton(th, text="⬇  Descargar CSV",
                                       font=FONTS["caption"],
                                       height=32, corner_radius=8,
                                       fg_color="transparent",
                                       border_width=1, border_color=COLORS["border"],
                                       hover_color=COLORS["bg"],
                                       text_color=COLORS["green_dark"],
                                       state="disabled",
                                       command=self._exportar_csv)
        self._csv_btn.grid(row=0, column=1, sticky="e")

        # Cabecera columnas
        cols = ctk.CTkFrame(table_card, fg_color=COLORS["surface"], corner_radius=6)
        cols.grid(row=1, column=0, sticky="ew", padx=16, pady=(10,0))
        cols.grid_columnconfigure((0,1), weight=1)
        for i, col in enumerate(["TIEMPO (T)", "POBLACIÓN (P)"]):
            ctk.CTkLabel(cols, text=col,
                         font=("Arial", 9, "bold"),
                         text_color=COLORS["text_hint"],
                         anchor="w").grid(row=0, column=i, padx=18, pady=7, sticky="w")

        # Cuerpo scrollable
        self._table_body = ctk.CTkScrollableFrame(
            table_card, fg_color="transparent",
            scrollbar_button_color=COLORS["border"])
        self._table_body.grid(row=2, column=0, sticky="nsew", padx=16, pady=(0,12))
        self._table_body.grid_columnconfigure((0,1), weight=1)

        self._no_data_lbl = ctk.CTkLabel(self._table_body,
                                          text="Sin datos. Ejecuta una simulación.",
                                          font=FONTS["subtitle"],
                                          text_color=COLORS["text_hint"])
        self._no_data_lbl.grid(row=0, column=0, columnspan=2, pady=18)

        # Guardar para exportar
        self._last_t = []
        self._last_p = []

    # ─────────────────────────────────────────────────────────────────────────
    def _on_result(self, modelo, t_vals, p_vals):
        """Recibe resultados del SimulationPanel y actualiza gráfica + tabla."""
        self._modelo_label = modelo
        self._last_t = t_vals
        self._last_p = p_vals

        self._update_chart(modelo, t_vals, p_vals)
        self._update_table(t_vals, p_vals)
        self._csv_btn.configure(state="normal")

    # ─────────────────────────────────────────────────────────────────────────
    def _update_chart(self, modelo, t_vals, p_vals):
        """Dibuja la curva con matplotlib embebido en CTk."""
        # Quitar placeholder
        self._placeholder.place_forget()

        # Destruir canvas anterior si existe
        if self._mpl_canvas:
            self._mpl_canvas.get_tk_widget().destroy()
            self._mpl_canvas = None

        fig = Figure(figsize=(6, 3.2), dpi=96, facecolor="#FFFFFF")
        ax  = fig.add_subplot(111)
        ax.set_facecolor("#F8FAFC")

        # Línea principal
        ax.plot(t_vals, p_vals,
                color="#22C55E", linewidth=2.5, zorder=3)
        ax.fill_between(t_vals, p_vals,
                         alpha=0.12, color="#22C55E")

        # Línea K si es logístico
        if modelo == "Modelo Logístico" and p_vals:
            k_approx = max(p_vals)
            ax.axhline(k_approx, color="#94A3B8", linewidth=1,
                       linestyle="--", label=f"K ≈ {k_approx:,.0f}")
            ax.legend(fontsize=8, framealpha=0.8)

        ax.set_xlabel("Tiempo (t)", fontsize=9, color="#64748B")
        ax.set_ylabel("Población P(t)", fontsize=9, color="#64748B")
        ax.tick_params(colors="#94A3B8", labelsize=8)
        for spine in ax.spines.values():
            spine.set_edgecolor("#E2E8F0")
        ax.grid(True, color="#E2E8F0", linewidth=0.7, zorder=0)
        fig.tight_layout(pad=1.4)

        self._mpl_canvas = FigureCanvasTkAgg(fig, master=self._chart_area)
        self._mpl_canvas.draw()
        self._mpl_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    # ─────────────────────────────────────────────────────────────────────────
    def _update_table(self, t_vals, p_vals):
        """Llena la tabla con t y P(t)."""
        # Limpiar filas anteriores
        for w in self._table_rows:
            w.destroy()
        self._table_rows.clear()
        self._no_data_lbl.grid_forget()

        for i, (t, p) in enumerate(zip(t_vals, p_vals)):
            bg = COLORS["card"] if i % 2 == 0 else COLORS["surface"]
            row_f = ctk.CTkFrame(self._table_body, fg_color=bg, corner_radius=0)
            row_f.grid(row=i, column=0, columnspan=2, sticky="ew")
            row_f.grid_columnconfigure((0,1), weight=1)

            ctk.CTkLabel(row_f, text=str(t),
                         font=FONTS["subtitle"],
                         text_color=COLORS["text_sub"],
                         anchor="w").grid(row=0, column=0, padx=18, pady=5, sticky="w")
            ctk.CTkLabel(row_f, text=f"{p:,.2f}",
                         font=("Arial", 12, "bold"),
                         text_color=COLORS["text_main"],
                         anchor="w").grid(row=0, column=1, padx=18, pady=5, sticky="w")

            self._table_rows.append(row_f)

    # ─────────────────────────────────────────────────────────────────────────
    def _exportar_csv(self):
        import csv, tkinter.filedialog as fd
        path = fd.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
            initialfile=f"sdcp_{self._modelo_label.replace(' ','_').lower()}.csv")
        if not path:
            return
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Tiempo (t)", "Población P(t)"])
            for t, p in zip(self._last_t, self._last_p):
                writer.writerow([t, f"{p:.4f}"])

    def cambiar_modelo(self, modelo):
        self.sim_panel.cambiar_modelo(modelo)


# ══════════════════════════════════════════════════════════════════════════════
class DashboardView(ctk.CTkFrame):
    """Vista principal SDCP. Navegación interna por secciones."""

    def __init__(self, parent, user_data=None, **kwargs):
        super().__init__(parent, fg_color=COLORS["bg"], corner_radius=0, **kwargs)
        self.user_data = user_data or {
            "nombre": "Juan Pérez", "rol": "Alumno",
            "matricula": "A01234567", "correo": "juan@ejemplo.com"}
        self._sections = {}
        self._build()

    def _build(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Sidebar
        self.sidebar = Sidebar(self, on_navigate=self._navigate)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")

        # Header
        self._build_header()

        # Contenedor de secciones
        content = ctk.CTkFrame(self, fg_color=COLORS["bg"], corner_radius=0)
        content.grid(row=1, column=1, sticky="nsew")
        content.grid_rowconfigure(0, weight=1)
        content.grid_columnconfigure(0, weight=1)

        # Crear secciones apiladas
        self._sim_sec  = SimulatorSection(content)
        self._sim_sec.grid(row=0, column=0, sticky="nsew")

        self._prof_sec = ProfilePanel(content, user_data=self.user_data)
        self._prof_sec.grid(row=0, column=0, sticky="nsew")

        self._hist_sec = HistoryPanel(content)
        self._hist_sec.grid(row=0, column=0, sticky="nsew")

        self._sett_sec = SettingsPanel(content)
        self._sett_sec.grid(row=0, column=0, sticky="nsew")

        self._sections = {
            "simulador":     self._sim_sec,
            "perfil":        self._prof_sec,
            "historial":     self._hist_sec,
            "configuracion": self._sett_sec,
        }

        self._navigate("simulador")

    # ─────────────────────────────────────────────────────────────────────────
    def _build_header(self):
        header = ctk.CTkFrame(self, height=64, fg_color=COLORS["card"],
                               corner_radius=0)
        header.grid(row=0, column=1, sticky="ew")
        header.grid_propagate(False)
        header.grid_columnconfigure(1, weight=1)

        # Título
        tf = ctk.CTkFrame(header, fg_color="transparent")
        tf.grid(row=0, column=0, padx=20, sticky="w")
        logo = draw_logo_small(tf, size=28, bg=COLORS["card"])
        logo.pack(side="left", padx=(0,8))
        self._header_title = ctk.CTkLabel(tf, text="Simulador Poblacional",
                                           font=FONTS["title"],
                                           text_color=COLORS["text_main"])
        self._header_title.pack(side="left")

        # Toggle modelos
        self._toggle_wrap = ctk.CTkFrame(header, fg_color="transparent")
        self._toggle_wrap.grid(row=0, column=1)
        from components.model_toggle import ModelToggle
        self.toggle = ModelToggle(self._toggle_wrap,
                                   on_change=self._on_modelo_change)
        self.toggle.pack()

        # Perfil
        pf = ctk.CTkFrame(header, fg_color="transparent")
        pf.grid(row=0, column=2, padx=20, sticky="e")
        info_col = ctk.CTkFrame(pf, fg_color="transparent")
        info_col.pack(side="left", padx=(0,10))
        ctk.CTkLabel(info_col, text=self.user_data["nombre"],
                     font=FONTS["label"],
                     text_color=COLORS["text_main"],
                     anchor="e").pack(anchor="e")
        ctk.CTkLabel(info_col,
                     text=f"  {self.user_data['rol']}  ",
                     font=FONTS["small"],
                     text_color=COLORS["green_dark"],
                     fg_color=COLORS["green_glow"],
                     corner_radius=6).pack(anchor="e")
        ctk.CTkLabel(pf,
                     text=self.user_data["nombre"][0].upper(),
                     font=("Arial", 15, "bold"),
                     width=40, height=40,
                     fg_color=COLORS["green"],
                     text_color="#FFFFFF",
                     corner_radius=20).pack(side="left")

        # Línea bajo header
        ctk.CTkFrame(self, height=1, fg_color=COLORS["border"]).grid(
            row=0, column=1, sticky="sew")

    # ─────────────────────────────────────────────────────────────────────────
    def _navigate(self, key):
        titles = {
            "simulador":     "Simulador Poblacional",
            "perfil":        "Mi Perfil",
            "historial":     "Historial de Simulaciones",
            "configuracion": "Configuración",
        }
        self._header_title.configure(text=titles.get(key, "SDCP"))

        if key == "simulador":
            self._toggle_wrap.grid()
        else:
            self._toggle_wrap.grid_remove()

        if key in self._sections:
            self._sections[key].tkraise()

    def _on_modelo_change(self, modelo):
        self._sim_sec.cambiar_modelo(modelo)