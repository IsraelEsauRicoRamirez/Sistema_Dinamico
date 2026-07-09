import math
import customtkinter as ctk
from utils.theme import COLORS, FONTS, SIZES
from components.custom_entry import CustomEntry


def _safe_float(val, default=0.0):
    try:
        return float(str(val).strip())
    except Exception:
        return default


MODELOS_INFO = {
    "Modelo Exponencial": {
        "titulo":  "Crecimiento sin restricciones ambientales",
        "eq_diff": "dP/dt = r · P",
        "eq_sol":  "P(t) = P₀ · e^(r·t)",
        "desc":    "La población crece proporcionalmente a su tamaño actual. No tiene límite superior.",
        "params": [
            (
                "Población Inicial (P₀)",
                "100",
                "individuos",
                "Número de individuos al inicio de la simulación (cuando t = 0).",
            ),
            (
                "Tasa de Crecimiento (r)",
                "0.1",
                "1/t",
                "Si r > 0 la población crece. Si r < 0 la población decrece.",
            ),
            (
                "Tiempo (t)",
                "50",
                "pasos",
                "Número de pasos a graficar: t = 0, 1, 2 ... hasta este valor.",
            ),
        ],
    },
    "Modelo Logístico": {
        "titulo":  "Crecimiento con capacidad de carga ambiental",
        "eq_diff": "dP/dt = r · P · (1 - P/K)",
        "eq_sol":  "P(t) = K / (1 + A · e^(-r·t))  ,  A = (K-P₀)/P₀",
        "desc":    "La población crece hasta el límite K impuesto por los recursos del ambiente.",
        "params": [
            (
                "Población Inicial (P₀)",
                "100",
                "individuos",
                "Número de individuos al inicio de la simulación (cuando t = 0).",
            ),
            (
                "Tasa de Crecimiento (r)",
                "0.1",
                "1/t",
                "Velocidad intrínseca de crecimiento per cápita.",
            ),
            (
                "Capacidad de Carga (K)",
                "1000",
                "individuos",
                "Número máximo de individuos que el ambiente puede sostener.",
            ),
            (
                "Tiempo (t)",
                "50",
                "pasos",
                "Número de pasos a graficar: t = 0, 1, 2 ... hasta este valor.",
            ),
        ],
    },
}

VARIABLES_INFO = {
    "Modelo Exponencial": [
        ("P(t)", "Población en el tiempo t",  "Variable dependiente: número de individuos en t"),
        ("P₀",  "Población inicial",           "Valor de P cuando t = 0 (condición inicial)"),
        ("r",   "Tasa de crecimiento",         "r > 0 crece  |  r < 0 decrece  |  r = 0 constante"),
        ("t",   "Tiempo",                      "Variable independiente. Va de 0 hasta el valor ingresado"),
        ("e",   "Número de Euler",             "Constante ≈ 2.71828, base del crecimiento continuo"),
        ("dP/dt","Tasa de cambio de P",        "Derivada: velocidad con que cambia la población"),
    ],
    "Modelo Logístico": [
        ("P(t)", "Población en el tiempo t",  "Variable dependiente: número de individuos en t"),
        ("P₀",  "Población inicial",           "Valor de P cuando t = 0 (condición inicial)"),
        ("r",   "Tasa de crecimiento",         "Velocidad intrínseca de crecimiento per cápita"),
        ("K",   "Capacidad de carga",          "Límite máximo que el ambiente puede sostener"),
        ("A",   "Constante auxiliar",          "A = (K - P₀) / P₀"),
        ("e",   "Número de Euler",             "Constante ≈ 2.71828"),
    ],
}


class _Collapsible(ctk.CTkFrame):
    def __init__(self, parent, title, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self._open = False
        self._btn = ctk.CTkButton(
            self, text=f"  ▸  {title}",
            font=("Arial", 15, "bold"),
            height=44, corner_radius=10,
            fg_color=COLORS["surface"],
            hover_color=COLORS["green_glow"],
            text_color=COLORS["text_sub"],
            border_width=1, border_color=COLORS["border"],
            anchor="w",
            command=self._toggle,
        )
        self._btn.grid(row=0, column=0, sticky="ew")
        self._body = ctk.CTkFrame(
            self, fg_color=COLORS["surface"],
            corner_radius=10,
            border_width=1, border_color=COLORS["border"],
        )
        self._body.grid_columnconfigure(0, weight=1)

    def _toggle(self):
        self._open = not self._open
        if self._open:
            self._body.grid(row=1, column=0, sticky="ew", pady=(4, 0))
            self._btn.configure(
                text=self._btn.cget("text").replace("▸", "▾"))
        else:
            self._body.grid_forget()
            self._btn.configure(
                text=self._btn.cget("text").replace("▾", "▸"))

    @property
    def body(self):
        return self._body


class SimulationPanel(ctk.CTkFrame):
    def __init__(self, parent, on_result=None, **kwargs):
        super().__init__(parent, width=420,
                         fg_color=COLORS["card"], corner_radius=0, **kwargs)
        self.grid_propagate(False)
        self.on_result      = on_result
        self._entries       = {}
        self._r_entries     = {}
        self._r_calculated  = None
        self._r_lbl         = None
        self._status_lbl    = None
        self._modelo_actual = "Modelo Exponencial"
        self._build()

    def _build(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkFrame(self, width=1, fg_color=COLORS["border"]).grid(
            row=0, column=1, rowspan=3, sticky="ns")

        self._scroll = ctk.CTkScrollableFrame(
            self, fg_color="transparent",
            scrollbar_button_color=COLORS["border"])
        self._scroll.grid(row=0, column=0, sticky="nsew")
        self._scroll.grid_columnconfigure(0, weight=1)

        self._render_modelo(self._modelo_actual)

        self._status_frame = ctk.CTkFrame(
            self, fg_color=COLORS["green_subtle"], corner_radius=0)
        self._status_frame.grid(row=1, column=0, sticky="ew")
        self._status_frame.grid_columnconfigure(0, weight=1)
        self._status_lbl = ctk.CTkLabel(
            self._status_frame, text="",
            font=("Arial", 13, "normal"),
            text_color=COLORS["text_hint"],
            anchor="w", wraplength=380, justify="left")
        self._status_lbl.grid(row=0, column=0, sticky="ew", padx=14, pady=7)

        btn_wrap = ctk.CTkFrame(self, fg_color=COLORS["card"])
        btn_wrap.grid(row=2, column=0, sticky="ew", padx=14, pady=(8, 14))
        btn_wrap.grid_columnconfigure(0, weight=1)
        ctk.CTkFrame(btn_wrap, height=1,
                     fg_color=COLORS["border"]).grid(
            row=0, column=0, sticky="ew", pady=(0, 8))
        ctk.CTkButton(
            btn_wrap, text="▶  Ejecutar Simulación",
            font=("Arial", 16, "bold"),
            height=52,
            corner_radius=SIZES["corner_radius"],
            fg_color=COLORS["green"],
            hover_color=COLORS["green_hover"],
            text_color="#FFFFFF",
            command=self._ejecutar,
        ).grid(row=1, column=0, sticky="ew")

    def _render_modelo(self, modelo):
        for w in self._scroll.winfo_children():
            w.destroy()
        self._entries.clear()
        self._r_entries.clear()
        self._r_calculated = None
        self._r_lbl = None

        info  = MODELOS_INFO[modelo]
        vars_ = VARIABLES_INFO[modelo]

        card = ctk.CTkFrame(self._scroll, fg_color=COLORS["surface"],
                             corner_radius=14,
                             border_width=1, border_color=COLORS["border"])
        card.grid(row=0, column=0, sticky="ew", padx=14, pady=(16, 0))
        card.grid_columnconfigure(0, weight=1)

        hdr = ctk.CTkFrame(card, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=14, pady=(14, 6))
        ctk.CTkLabel(hdr, text=" ƒ ",
                     font=("Arial", 16, "bold"),
                     text_color="#FFFFFF",
                     fg_color=COLORS["green"],
                     corner_radius=6).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(hdr, text=info["titulo"],
                     font=("Arial", 15, "bold"),
                     text_color=COLORS["text_main"],
                     wraplength=270, justify="left").pack(side="left")

        ctk.CTkLabel(card, text=info["desc"],
                     font=("Arial", 14, "normal"),
                     text_color=COLORS["text_sub"],
                     anchor="w", wraplength=370,
                     justify="left").grid(
            row=1, column=0, sticky="w", padx=14, pady=(0, 10))

        ctk.CTkLabel(card, text="Ecuación diferencial:",
                     font=("Arial", 13, "bold"),
                     text_color=COLORS["text_hint"],
                     anchor="w").grid(row=2, column=0, sticky="w", padx=14)

        fbox1 = ctk.CTkFrame(card, fg_color=COLORS["card"],
                              corner_radius=8,
                              border_width=1, border_color=COLORS["border"])
        fbox1.grid(row=3, column=0, sticky="ew", padx=14, pady=(4, 8))
        ctk.CTkLabel(fbox1, text=info["eq_diff"],
                     font=("Arial", 17, "italic"),
                     text_color=COLORS["text_main"]).pack(padx=14, pady=10)

        ctk.CTkLabel(card, text="Solución analítica:",
                     font=("Arial", 13, "bold"),
                     text_color=COLORS["text_hint"],
                     anchor="w").grid(row=4, column=0, sticky="w", padx=14)

        fbox2 = ctk.CTkFrame(card, fg_color=COLORS["green_subtle"],
                              corner_radius=8,
                              border_width=1, border_color=COLORS["green"])
        fbox2.grid(row=5, column=0, sticky="ew", padx=14, pady=(4, 8))
        ctk.CTkLabel(fbox2, text=info["eq_sol"],
                     font=("Arial", 15, "bold"),
                     text_color=COLORS["green_dark"],
                     wraplength=360, justify="center").pack(padx=14, pady=10)

        sec_vars = _Collapsible(card, "Glosario de variables")
        sec_vars.grid(row=6, column=0, sticky="ew", padx=14, pady=(0, 14))
        for sym, name, desc in vars_:
            row_f = ctk.CTkFrame(sec_vars.body, fg_color="transparent")
            row_f.pack(fill="x", padx=12, pady=5)
            ctk.CTkLabel(row_f, text=sym,
                         font=("Arial", 16, "bold"),
                         text_color=COLORS["green"],
                         width=46, anchor="w").pack(side="left")
            col = ctk.CTkFrame(row_f, fg_color="transparent")
            col.pack(side="left", fill="x", expand=True)
            ctk.CTkLabel(col, text=name,
                         font=("Arial", 14, "bold"),
                         text_color=COLORS["text_main"],
                         anchor="w").pack(anchor="w")
            ctk.CTkLabel(col, text=desc,
                         font=("Arial", 13, "normal"),
                         text_color=COLORS["text_sub"],
                         anchor="w", wraplength=260,
                         justify="left").pack(anchor="w")

        ctk.CTkLabel(self._scroll,
                     text="PARÁMETROS DE SIMULACIÓN",
                     font=("Arial", 13, "bold"),
                     text_color=COLORS["text_hint"],
                     anchor="w").grid(
            row=1, column=0, sticky="w", padx=18, pady=(18, 6))

        for idx, (label, default, unit, tip) in enumerate(info["params"]):
            e = CustomEntry(
                self._scroll,
                label=label,
                placeholder=default,
                unit=unit if unit else "",
                tooltip=tip,
            )
            e.insert(0, default)
            e.grid(row=2 + idx, column=0, sticky="ew",
                   padx=14, pady=(0, 12))
            self._entries[label] = e

        next_row = 2 + len(info["params"])

        sec_r = _Collapsible(self._scroll,
                              "Calcular Tasa de Crecimiento (r)")
        sec_r.grid(row=next_row, column=0, sticky="ew",
                   padx=14, pady=(4, 14))
        self._build_calc_r(sec_r.body)

    def _build_calc_r(self, body):
        body.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            body,
            text="Si conoces la población en dos momentos distintos,\n"
                 "puedes calcular r con esta fórmula:",
            font=("Arial", 13, "normal"),
            text_color=COLORS["text_sub"],
            justify="left", anchor="w").pack(fill="x", padx=14, pady=(12, 6))

        ctk.CTkLabel(body, text="r  =  ln(Pf / P₀)  /  t",
                     font=("Arial", 16, "italic"),
                     text_color=COLORS["text_main"],
                     fg_color=COLORS["card"],
                     corner_radius=8).pack(fill="x", padx=14, pady=(0, 12))

        r_fields = [
            ("r_p0", "P₀  — Población inicial",
             "individuos", "100",
             "Individuos al inicio del período de observación real."),
            ("r_pf", "Pf  — Población final",
             "individuos", "200",
             "Individuos al final del período de observación real."),
            ("r_t",  "t  — Tiempo transcurrido",
             "pasos", "10",
             "Número de pasos entre los dos conteos (tf - t₀)."),
        ]
        for key, lbl, unit, dflt, tip in r_fields:
            e = CustomEntry(body, label=lbl, placeholder=dflt,
                            unit=unit, tooltip=tip)
            e.insert(0, dflt)
            e.pack(fill="x", padx=14, pady=(0, 8))
            self._r_entries[key] = e

        self._r_lbl = ctk.CTkLabel(
            body, text="r  =  —",
            font=("Arial", 17, "bold"),
            text_color=COLORS["green"],
            fg_color=COLORS["green_glow"],
            corner_radius=8)
        self._r_lbl.pack(fill="x", padx=14, pady=(4, 8))

        ctk.CTkButton(body, text="Calcular r",
                      font=("Arial", 15, "bold"),
                      height=44, corner_radius=10,
                      fg_color=COLORS["green"],
                      hover_color=COLORS["green_hover"],
                      text_color="#FFFFFF",
                      command=self._calcular_r).pack(
            fill="x", padx=14, pady=(0, 6))

        ctk.CTkButton(body,
                      text="↑ Usar este r en los parámetros",
                      font=("Arial", 14, "normal"),
                      height=38, corner_radius=8,
                      fg_color="transparent",
                      border_width=1, border_color=COLORS["border"],
                      hover_color=COLORS["green_glow"],
                      text_color=COLORS["green_dark"],
                      command=self._usar_r).pack(
            fill="x", padx=14, pady=(0, 14))

    def _calcular_r(self):
        try:
            p0 = _safe_float(self._r_entries["r_p0"].get())
            pf = _safe_float(self._r_entries["r_pf"].get())
            t  = _safe_float(self._r_entries["r_t"].get())

            if p0 <= 0 or pf <= 0:
                self._r_lbl.configure(
                    text="⚠  P₀ y Pf deben ser > 0",
                    text_color=COLORS["error"])
                return
            if t <= 0:
                self._r_lbl.configure(
                    text="⚠  t debe ser > 0",
                    text_color=COLORS["error"])
                return

            r = math.log(pf / p0) / t
            self._r_calculated = r
            self._r_lbl.configure(
                text=f"r  =  {r:.8f}",
                text_color=COLORS["green"])
        except Exception as ex:
            self._r_lbl.configure(
                text=f"Error: {ex}", text_color=COLORS["error"])

    def _usar_r(self):
        if self._r_calculated is None:
            if self._r_lbl:
                self._r_lbl.configure(
                    text="⚠  Primero pulsa 'Calcular r'",
                    text_color=COLORS["error"])
            return
        key = "Tasa de Crecimiento (r)"
        if key in self._entries:
            self._entries[key].entry.delete(0, "end")
            self._entries[key].entry.insert(
                0, f"{self._r_calculated:.8f}")
            if self._r_lbl:
                self._r_lbl.configure(
                    text=f"✓  r = {self._r_calculated:.8f}  copiado",
                    text_color=COLORS["green"])

    def cambiar_modelo(self, modelo):
        if modelo != self._modelo_actual:
            self._modelo_actual = modelo
            self._render_modelo(modelo)
            if self._status_lbl:
                self._status_lbl.configure(text="")

    def _ejecutar(self):
        modelo = self._modelo_actual

        def read(label, default):
            e = self._entries.get(label)
            if e is None:
                return default
            raw = e.entry.get().strip()
            return _safe_float(raw, default) if raw else default

        try:
            p0 = read("Población Inicial (P₀)", 100.0)
            r  = read("Tasa de Crecimiento (r)", 0.1)
            n  = int(read("Tiempo (t)", 50.0))

            if p0 <= 0:
                self._set_status("⚠  P₀ debe ser > 0", error=True)
                return
            if n <= 0:
                self._set_status("⚠  Tiempo debe ser > 0", error=True)
                return

            # t va de 0 hasta n en pasos enteros — solo para graficar
            t_vals = list(range(n + 1))

            if modelo == "Modelo Exponencial":
                # Fórmula exacta: P(t) = P₀ · e^(r·t)
                p_vals = [p0 * math.exp(r * t) for t in t_vals]
                sol_str = f"P(t) = {p0:g} · e^({r:.6g} · t)"
                self._set_status(
                    f"✓  P₀={p0:g}  r={r:.6g}  t=[0,{n}]"
                    f"  →  P({n}) = {p_vals[-1]:,.4f}")

            else:
                k = read("Capacidad de Carga (K)", 1000.0)
                if k <= 0:
                    self._set_status("⚠  K debe ser > 0", error=True)
                    return

                # Integración numérica RK4
                p  = p0
                p_vals = [p]
                dt = 1.0
                for _ in range(n):
                    def f(pp, _r=r, _k=k):
                        return _r * pp * (1.0 - pp / _k)
                    k1 = f(p)
                    k2 = f(p + 0.5 * dt * k1)
                    k3 = f(p + 0.5 * dt * k2)
                    k4 = f(p + dt * k3)
                    p  = max(0.0,
                             p + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4))
                    p_vals.append(p)

                A = (k - p0) / p0 if p0 > 0 else 0
                sol_str = (f"P(t) = {k:g} / "
                           f"(1 + {A:.4g}·e^(-{r:.6g}·t))")
                self._set_status(
                    f"✓  P₀={p0:g}  r={r:.6g}  K={k:g}  t=[0,{n}]"
                    f"  →  P({n}) = {p_vals[-1]:,.4f}")

            params = {"P₀": p0, "r": r, "n": n, "sol_str": sol_str}
            if modelo == "Modelo Logístico":
                params["K"] = k

            if self.on_result:
                self.on_result(modelo, t_vals, p_vals, params)

        except Exception as ex:
            self._set_status(f"Error: {ex}", error=True)
            import traceback; traceback.print_exc()

    def _set_status(self, msg, error=False):
        if self._status_lbl:
            color = COLORS["error"] if error else COLORS["text_hint"]
            self._status_lbl.configure(text=msg, text_color=color)

    def get_valores(self):
        return {k: v.entry.get().strip()
                for k, v in self._entries.items()}