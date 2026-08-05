# views/dashboard_view.py
import tkinter as tk
import customtkinter as ctk
import math
import numpy as np
import matplotlib
import matplotlib.ticker

from utils.theme import COLORS, FONTS, SIZES
from components.sidebar import Sidebar
from components.model_toggle import ModelToggle
from components.simulation_panel import SimulationPanel

matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def _draw_logo_small(parent, size=28, bg=None):
    bg = bg or COLORS["card"]
    if isinstance(bg, tuple):
        bg = bg[1] if ctk.get_appearance_mode() == "Dark" else bg[0]
    scale = size / 100
    c = tk.Canvas(parent, width=size, height=size,
                  highlightthickness=0, bg=bg)
    c.create_rectangle(0, 0, size, size, fill="#F4F4F5", outline="")
    def sc(v): return int(v * scale)
    c.create_line(sc(25),sc(75),sc(50),sc(45),sc(75),sc(45),
                  fill="#22c55e", width=max(2, int(5*scale)),
                  capstyle="round", joinstyle="round")
    c.create_line(sc(25),sc(75),sc(60),sc(75),sc(75),sc(45),
                  fill="#d4d4d8", width=max(1, int(4*scale)),
                  capstyle="round", joinstyle="round")
    c.create_line(sc(50),sc(45),sc(60),sc(75), fill="#e4e4e7", width=1)
    def oval(cx, cy, r, fill):
        cx,cy,r = sc(cx), sc(cy), max(2, int(r*scale))
        c.create_oval(cx-r,cy-r,cx+r,cy+r, fill=fill, outline="")
    oval(25,75,7,"#18181b"); oval(50,45,6,"#71717a")
    oval(60,75,5,"#a1a1aa"); oval(75,45,9,"#22c55e"); oval(75,45,3,"#ffffff")
    return c


class SimulatorSection(ctk.CTkFrame):
    """
    Sección del simulador: panel de parámetros a la izquierda,
    gráfica + tabla a la derecha.
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=COLORS["bg"],
                         corner_radius=0, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self._mpl_canvas  = None
        self._table_rows  = []
        self._last_anios  = []
        self._last_p      = []
        self._last_modelo = ""
        self._build()

    def _build(self):
        # Panel izquierdo de parámetros
        self.sim_panel = SimulationPanel(self, on_result=self._on_result)
        self.sim_panel.grid(row=0, column=0, sticky="nsew")

        # Panel derecho
        right = ctk.CTkFrame(self, fg_color=COLORS["bg"], corner_radius=0)
        right.grid(row=0, column=1, sticky="nsew")
        right.grid_rowconfigure(0, weight=0)   # tarjeta de resultado: tamaño fijo
        right.grid_rowconfigure(1, weight=3)   # gráfica: mayor espacio
        right.grid_rowconfigure(2, weight=2)   # tabla
        right.grid_columnconfigure(0, weight=1)

        # ── Tarjeta de resultado / solución ──────────────────────────────────
        self._sol_card = ctk.CTkFrame(right,
                                      fg_color=COLORS["green_subtle"],
                                      corner_radius=12,
                                      border_width=1, border_color=COLORS["green"])
        self._sol_card.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 4))
        self._sol_card.grid_columnconfigure(0, weight=1)

        sol_hdr = ctk.CTkFrame(self._sol_card, fg_color="transparent")
        sol_hdr.grid(row=0, column=0, sticky="w", padx=14, pady=(10, 2))
        ctk.CTkLabel(sol_hdr, text="✓",
                     font=("Arial", 12, "bold"),
                     text_color="#FFFFFF",
                     fg_color=COLORS["green"],
                     width=22, height=22,
                     corner_radius=11).pack(side="left", padx=(0, 8))
        ctk.CTkLabel(sol_hdr,
                     text="Resultado de la simulación",
                     font=("Arial", 13, "bold"),
                     text_color=COLORS["green_dark"]).pack(side="left")

        self._sol_lbl = ctk.CTkLabel(
            self._sol_card,
            text="Ejecuta una simulación para ver el resultado.",
            font=("Arial", 13, "italic"),
            text_color=COLORS["text_sub"],
            wraplength=620, justify="left", anchor="w")
        self._sol_lbl.grid(row=1, column=0, sticky="w", padx=14, pady=(2, 10))

        # ── Gráfica ───────────────────────────────────────────────────────────
        chart_card = ctk.CTkFrame(right, fg_color=COLORS["card"],
                                  corner_radius=16,
                                  border_width=1, border_color=COLORS["border"])
        chart_card.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 8))
        chart_card.grid_rowconfigure(1, weight=1)
        chart_card.grid_columnconfigure(0, weight=1)

        ch = ctk.CTkFrame(chart_card, fg_color="transparent")
        ch.grid(row=0, column=0, sticky="ew", padx=18, pady=(14, 0))
        ctk.CTkFrame(ch, width=3, height=20,
                     fg_color=COLORS["green"],
                     corner_radius=2).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(ch, text="Gráfica Dinámica",
                     font=FONTS["title"],
                     text_color=COLORS["text_main"]).pack(side="left")

        self._chart_area = ctk.CTkFrame(chart_card, fg_color="#FFFFFF",
                                        corner_radius=10)
        self._chart_area.grid(row=1, column=0, sticky="nsew", padx=14, pady=(8, 14))
        self._chart_area.grid_rowconfigure(0, weight=1)
        self._chart_area.grid_columnconfigure(0, weight=1)

        # Placeholder: ícono grande de gráfica + instrucción
        ph_frame = ctk.CTkFrame(self._chart_area, fg_color="transparent")
        ph_frame.place(relx=.5, rely=.5, anchor="center")
        ctk.CTkLabel(ph_frame,
                     text="∫",
                     font=("Georgia", 64, "bold"),
                     text_color="#22C55E").pack()
        ctk.CTkLabel(ph_frame,
                     text="P(t) = P₀ · eʳᵗ",
                     font=("Arial", 15, "italic"),
                     text_color=COLORS["text_hint"]).pack(pady=(4, 0))
        ctk.CTkLabel(ph_frame,
                     text="Configura los parámetros y pulsa  ▶ Ejecutar Simulación",
                     font=FONTS["caption"],
                     text_color=COLORS["text_hint"],
                     justify="center").pack(pady=(8, 0))
        self._placeholder = ph_frame

        # ── Tabla de datos ────────────────────────────────────────────────────
        table_card = ctk.CTkFrame(right, fg_color=COLORS["card"],
                                  corner_radius=16,
                                  border_width=1, border_color=COLORS["border"])
        table_card.grid(row=2, column=0, sticky="nsew", padx=16, pady=(0, 16))
        table_card.grid_rowconfigure(2, weight=1)
        table_card.grid_columnconfigure(0, weight=1)

        th = ctk.CTkFrame(table_card, fg_color="transparent")
        th.grid(row=0, column=0, sticky="ew", padx=18, pady=(14, 0))
        th.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(th, text="Datos Obtenidos",
                     font=FONTS["title"],
                     text_color=COLORS["text_main"],
                     anchor="w").grid(row=0, column=0, sticky="w")

        self._csv_btn = ctk.CTkButton(
            th, text="⬇ Descargar CSV",
            font=FONTS["caption"],
            height=34, corner_radius=8,
            fg_color="transparent",
            border_width=1, border_color=COLORS["border"],
            hover_color=COLORS["bg"],
            text_color=COLORS["green_dark"],
            state="disabled",
            command=self._exportar_csv)
        self._csv_btn.grid(row=0, column=1, sticky="e")

        cols = ctk.CTkFrame(table_card, fg_color=COLORS["surface"], corner_radius=6)
        cols.grid(row=1, column=0, sticky="ew", padx=16, pady=(10, 0))
        cols.grid_columnconfigure((0, 1, 2), weight=1)
        for i, col in enumerate(["AÑO", "TIEMPO (t)", "POBLACIÓN  P(t)"]):
            ctk.CTkLabel(cols, text=col,
                         font=("Arial", 10, "bold"),
                         text_color=COLORS["text_hint"],
                         anchor="w").grid(row=0, column=i,
                                          padx=18, pady=8, sticky="w")

        self._table_body = ctk.CTkScrollableFrame(
            table_card, fg_color="transparent",
            scrollbar_button_color=COLORS["border"])
        self._table_body.grid(row=2, column=0, sticky="nsew", padx=16, pady=(0, 12))
        self._table_body.grid_columnconfigure((0, 1, 2), weight=1)

        self._no_data_lbl = ctk.CTkLabel(
            self._table_body,
            text="Sin datos. Ejecuta una simulación.",
            font=FONTS["subtitle"],
            text_color=COLORS["text_hint"])
        self._no_data_lbl.grid(row=0, column=0, columnspan=3, pady=18)

    # ── Callbacks ─────────────────────────────────────────────────────────────
    def _on_result(self, modelo, anios, p_vals, params):
        """Recibe años reales (ej. 1975, 1980, …, 2025) y poblaciones."""
        self._last_anios  = anios
        self._last_p      = p_vals
        self._last_modelo = modelo

        anio0   = params.get("anio0", anios[0])
        t_vals  = [a - anio0 for a in anios]   # tiempo relativo para la gráfica

        sol_str = params.get("sol_str", "")
        if sol_str:
            self._sol_lbl.configure(
                text=sol_str,
                text_color=COLORS["green_dark"],
                font=("Arial", 15, "bold"))

        self._update_chart(modelo, anios, t_vals, p_vals, params.get("K"))
        self._update_table(anios, t_vals, p_vals)
        self._csv_btn.configure(state="normal")

    def _update_chart(self, modelo, anios, t_vals, p_vals, k=None):
        self._placeholder.place_forget()
        if self._mpl_canvas:
            self._mpl_canvas.get_tk_widget().destroy()
            self._mpl_canvas = None

        fig = Figure(figsize=(6, 3.2), dpi=100, facecolor="#FFFFFF")
        ax  = fig.add_subplot(111)
        ax.set_facecolor("#F8FAFC")

        # Línea principal + relleno + puntos
        ax.plot(anios, p_vals, color="#22C55E", linewidth=2.5, zorder=4)
        ax.fill_between(anios, p_vals, alpha=0.10, color="#22C55E", zorder=2)
        ax.scatter(anios, p_vals, color="#16A34A", s=28, zorder=5, linewidths=0)

        # Línea K para logístico
        if k is not None:
            ax.axhline(k, color="#94A3B8", linewidth=1.4,
                       linestyle="--", label=f"K = {k:,.0f}", zorder=3)
            ax.legend(fontsize=11, framealpha=0.9)

        # Etiquetas en el punto final
        ax.annotate(f"{p_vals[-1]:,.0f}",
                    xy=(anios[-1], p_vals[-1]),
                    xytext=(-10, 10),
                    textcoords="offset points",
                    fontsize=11, color="#16A34A", fontweight="bold",
                    ha="right")

        # Formateo de ejes
        ax.xaxis.set_major_locator(
            matplotlib.ticker.MultipleLocator(5))
        ax.xaxis.set_major_formatter(
            matplotlib.ticker.FuncFormatter(lambda v, _: str(int(v))))
        ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(nbins=8))
        ax.yaxis.set_major_formatter(
            matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))

        ax.set_xlabel("Año", fontsize=12, color="#475569", labelpad=8)
        ax.set_ylabel("Población P(t)", fontsize=12, color="#475569", labelpad=8)
        ax.tick_params(colors="#64748B", labelsize=10, length=4)
        for sp in ax.spines.values():
            sp.set_edgecolor("#E2E8F0")
        ax.grid(True, color="#E2E8F0", linewidth=0.8, linestyle="--", zorder=0)
        ax.set_xlim(left=anios[0] - 1, right=anios[-1] + 1)
        fig.tight_layout(pad=1.6)

        self._mpl_canvas = FigureCanvasTkAgg(fig, master=self._chart_area)
        self._mpl_canvas.draw()
        self._mpl_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        # Tooltip interactivo al mover el mouse
        annot = ax.annotate(
            "", xy=(0, 0), xytext=(12, 12),
            textcoords="offset points",
            bbox=dict(boxstyle="round,pad=0.5",
                      fc="#0F172A", ec="#22C55E", lw=1.2, alpha=0.92),
            arrowprops=dict(arrowstyle="->", color="#22C55E", lw=1),
            fontsize=11, color="#FFFFFF", zorder=10)
        annot.set_visible(False)

        a_arr = np.array(anios)
        p_arr = np.array(p_vals)

        def _on_move(event):
            if event.inaxes != ax:
                annot.set_visible(False)
                self._mpl_canvas.draw_idle()
                return
            x = event.xdata
            if x is None:
                return
            idx = int(np.argmin(np.abs(a_arr - x)))
            tx, ty = a_arr[idx], p_arr[idx]
            annot.xy = (tx, ty)
            annot.set_text(f"Año {int(tx)}\nP = {ty:,.0f}")
            annot.set_visible(True)
            self._mpl_canvas.draw_idle()

        fig.canvas.mpl_connect("motion_notify_event", _on_move)

    def _update_table(self, anios, t_vals, p_vals):
        for w in self._table_rows:
            w.destroy()
        self._table_rows.clear()
        self._no_data_lbl.grid_forget()

        for i, (anio, t, p) in enumerate(zip(anios, t_vals, p_vals)):
            bg = COLORS["card"] if i % 2 == 0 else COLORS["surface"]
            row_f = ctk.CTkFrame(self._table_body, fg_color=bg, corner_radius=0)
            row_f.grid(row=i, column=0, columnspan=3, sticky="ew")
            row_f.grid_columnconfigure((0, 1, 2), weight=1)

            # Año
            ctk.CTkLabel(row_f,
                         text=str(anio),
                         font=("Arial", 13, "bold"),
                         text_color=COLORS["text_main"],
                         anchor="w").grid(row=0, column=0,
                                          padx=18, pady=6, sticky="w")
            # t relativo
            ctk.CTkLabel(row_f,
                         text=str(t),
                         font=FONTS["subtitle"],
                         text_color=COLORS["text_sub"],
                         anchor="w").grid(row=0, column=1,
                                          padx=18, pady=6, sticky="w")
            # P(t)
            ctk.CTkLabel(row_f,
                         text=f"{p:,.0f}",
                         font=("Arial", 13, "bold"),
                         text_color=COLORS["green_dark"],
                         anchor="w").grid(row=0, column=2,
                                          padx=18, pady=6, sticky="w")
            self._table_rows.append(row_f)

    def _exportar_csv(self):
        import csv
        import tkinter.filedialog as fd
        name = self._last_modelo.replace(" ", "_").lower()
        path = fd.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
            initialfile=f"sdcp_{name}.csv")
        if not path:
            return
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Año", "Tiempo (t)", "Población P(t)"])
            for anio, p in zip(self._last_anios, self._last_p):
                anio0 = self._last_anios[0]
                writer.writerow([anio, anio - anio0, f"{p:.2f}"])

    def cambiar_modelo(self, modelo):
        self.sim_panel.cambiar_modelo(modelo)


# ── Vista principal del Dashboard ────────────────────────────────────────────
class DashboardView(ctk.CTkFrame):
    def __init__(self, parent, user_data=None, on_show_intro=None, **kwargs):
        super().__init__(parent, fg_color=COLORS["bg"],
                         corner_radius=0, **kwargs)
        self.user_data     = user_data or {
            "nombre": "Juan Pérez", "rol": "Alumno",
            "matricula": "A01234567", "correo": "juan@ejemplo.com"}
        self.on_show_intro = on_show_intro
        self._sections     = {}
        self._build()

    def _build(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar = Sidebar(self, on_navigate=self._navigate)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")

        self._build_header()

        content = ctk.CTkFrame(self, fg_color=COLORS["bg"], corner_radius=0)
        content.grid(row=1, column=1, sticky="nsew")
        content.grid_rowconfigure(0, weight=1)
        content.grid_columnconfigure(0, weight=1)

        self._sim_sec = SimulatorSection(content)
        self._sim_sec.grid(row=0, column=0, sticky="nsew")

        from components.profile_panel import ProfilePanel
        from components.history_panel import HistoryPanel
        from components.settings_panel import SettingsPanel

        self._prof_sec = ProfilePanel(content, user_data=self.user_data)
        self._prof_sec.grid(row=0, column=0, sticky="nsew")

        self._hist_sec = HistoryPanel(content)
        self._hist_sec.grid(row=0, column=0, sticky="nsew")

        self._sett_sec = SettingsPanel(content,
                                       user_data=self.user_data,
                                       on_logout=self.on_show_intro)
        self._sett_sec.grid(row=0, column=0, sticky="nsew")

        self._sections = {
            "simulador":     self._sim_sec,
            "perfil":        self._prof_sec,
            "historial":     self._hist_sec,
            "configuracion": self._sett_sec,
        }
        self._navigate("simulador")

    def _build_header(self):
        header = ctk.CTkFrame(self, height=64, fg_color=COLORS["card"],
                              corner_radius=0)
        header.grid(row=0, column=1, sticky="ew")
        header.grid_propagate(False)
        header.grid_columnconfigure(1, weight=1)

        tf = ctk.CTkFrame(header, fg_color="transparent")
        tf.grid(row=0, column=0, padx=20, sticky="w")
        logo = _draw_logo_small(tf, size=28)
        logo.pack(side="left", padx=(0, 8))
        self._header_title = ctk.CTkLabel(
            tf, text="Simulador Poblacional",
            font=FONTS["title"],
            text_color=COLORS["text_main"])
        self._header_title.pack(side="left")

        self._toggle_wrap = ctk.CTkFrame(header, fg_color="transparent")
        self._toggle_wrap.grid(row=0, column=1)
        self.toggle = ModelToggle(self._toggle_wrap,
                                  on_change=self._on_modelo_change)
        self.toggle.pack()

        pf = ctk.CTkFrame(header, fg_color="transparent")
        pf.grid(row=0, column=2, padx=20, sticky="e")

        if self.on_show_intro:
            ctk.CTkButton(pf, text="ℹ Introducción",
                          font=FONTS["caption"],
                          height=32, corner_radius=8,
                          fg_color="transparent",
                          border_width=1, border_color=COLORS["border"],
                          hover_color=COLORS["bg"],
                          text_color=COLORS["text_sub"],
                          command=self.on_show_intro).pack(side="left",
                                                           padx=(0, 12))

        nombre  = self.user_data.get("nombre", "")
        inicial = nombre[0].upper() if nombre else "U"

        info_col = ctk.CTkFrame(pf, fg_color="transparent")
        info_col.pack(side="left", padx=(0, 10))
        ctk.CTkLabel(info_col,
                     text=nombre or "Usuario",
                     font=FONTS["label"],
                     text_color=COLORS["text_main"],
                     anchor="e").pack(anchor="e")
        ctk.CTkLabel(info_col,
                     text=f"  {self.user_data.get('rol', 'Invitado')}  ",
                     font=FONTS["small"],
                     text_color=COLORS["green_dark"],
                     fg_color=COLORS["green_glow"],
                     corner_radius=6).pack(anchor="e")

        ctk.CTkLabel(pf,
                     text=inicial,
                     font=("Arial", 15, "bold"),
                     width=40, height=40,
                     fg_color=COLORS["green"],
                     text_color="#FFFFFF",
                     corner_radius=20).pack(side="left")

        ctk.CTkFrame(self, height=1, fg_color=COLORS["border"]).grid(
            row=0, column=1, sticky="sew")

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
