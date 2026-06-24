# components/simulation_panel.py
import math
import customtkinter as ctk
from utils.theme import COLORS, FONTS, SIZES
from components.custom_entry import CustomEntry


# ── Variables de cada modelo ──────────────────────────────────────────────────
VARIABLES_INFO = {
    "Modelo Exponencial": [
        ("P₀", "Población inicial", "Número de individuos en el tiempo t=0"),
        ("r",  "Tasa de crecimiento", "Velocidad de crecimiento per cápita (puede ser negativa)"),
        ("t",  "Tiempo", "Número de pasos de tiempo a simular"),
        ("P(t)","Población en t", "Resultado: P₀ · e^(r·t)"),
    ],
    "Modelo Logístico": [
        ("P₀", "Población inicial", "Número de individuos en el tiempo t=0"),
        ("r",  "Tasa de crecimiento", "Velocidad intrínseca de crecimiento"),
        ("K",  "Capacidad de carga", "Máximo de individuos que el ambiente puede sostener"),
        ("t",  "Tiempo", "Número de pasos de tiempo a simular"),
        ("P(t)","Población en t", "Resultado: curva sigmoidea que se acerca a K"),
    ],
}

MODELOS_INFO = {
    "Modelo Exponencial": {
        "titulo":      "Crecimiento poblacional sin restricciones ambientales",
        "formula":     "dP/dt = r · P",
        "params": [
            ("Población Inicial (P₀)", "100"),
            ("Tasa de Crecimiento (r)", "0.1"),
            ("Tiempo (t)",              "50"),
        ],
    },
    "Modelo Logístico": {
        "titulo":      "Crecimiento poblacional con capacidad de carga",
        "formula":     "dP/dt = r · P(1 - P/K)",
        "params": [
            ("Población Inicial (P₀)", "100"),
            ("Tasa de Crecimiento (r)", "0.1"),
            ("Capacidad de Carga (K)", "1000"),
            ("Tiempo (t)",              "50"),
        ],
    },
}


class CollapsibleSection(ctk.CTkFrame):
    """Sección con header clicable que muestra/oculta su contenido."""

    def __init__(self, parent, title, icon="▸", **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self._open = False

        # Header botón
        self._hdr = ctk.CTkButton(
            self, text=f"  {icon}  {title}",
            font=("Arial", 11, "bold"),
            height=36, corner_radius=10,
            fg_color=COLORS["surface"],
            hover_color=COLORS["green_glow"],
            text_color=COLORS["text_sub"],
            border_width=1, border_color=COLORS["border"],
            anchor="w",
            command=self._toggle,
        )
        self._hdr.grid(row=0, column=0, sticky="ew")

        # Contenedor del contenido (oculto por defecto)
        self._body = ctk.CTkFrame(self,
                                   fg_color=COLORS["surface"],
                                   corner_radius=10,
                                   border_width=1,
                                   border_color=COLORS["border"])
        self._body.grid_columnconfigure(0, weight=1)

    def _toggle(self):
        self._open = not self._open
        if self._open:
            self._body.grid(row=1, column=0, sticky="ew", pady=(4, 0))
            self._hdr.configure(text=self._hdr.cget("text").replace("▸", "▾"))
        else:
            self._body.grid_forget()
            self._hdr.configure(text=self._hdr.cget("text").replace("▾", "▸"))

    @property
    def body(self):
        return self._body


class SimulationPanel(ctk.CTkFrame):
    """
    Panel izquierdo del simulador.
    Expone on_result(modelo, t_vals, p_vals) para actualizar gráfica y tabla.
    """

    def __init__(self, parent, on_result=None, **kwargs):
        super().__init__(parent, width=310,
                          fg_color=COLORS["card"],
                          corner_radius=0, **kwargs)
        self.grid_propagate(False)
        self.on_result    = on_result   # callback con datos calculados
        self._entries     = {}
        self._modelo_actual = "Modelo Exponencial"
        self._build()

    # ─────────────────────────────────────────────────────────────────────────
    def _build(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Borde derecho
        ctk.CTkFrame(self, width=1, fg_color=COLORS["border"]).grid(
            row=0, column=1, rowspan=2, sticky="ns")

        # Scroll principal
        self._scroll = ctk.CTkScrollableFrame(
            self, fg_color="transparent",
            scrollbar_button_color=COLORS["border"])
        self._scroll.grid(row=0, column=0, sticky="nsew")
        self._scroll.grid_columnconfigure(0, weight=1)

        self._render_modelo(self._modelo_actual)

        # Botón fijo al fondo + Panel de Estado
        btn_wrap = ctk.CTkFrame(self, fg_color=COLORS["card"])
        btn_wrap.grid(row=1, column=0, sticky="ew", padx=16, pady=(6, 14))
        btn_wrap.grid_columnconfigure(0, weight=1)

        ctk.CTkFrame(btn_wrap, height=1,
                     fg_color=COLORS["border"]).grid(row=0, column=0,
                                                     sticky="ew", pady=(0, 6))
        
        # 🛑 MODIFICACIÓN: Panel de Estado / Alertas visible
        self._lbl_estado = ctk.CTkLabel(
            btn_wrap, text="", 
            font=("Arial", 11, "bold"),
            text_color=COLORS["text_sub"],
            justify="center",
            wraplength=260
        )
        self._lbl_estado.grid(row=1, column=0, sticky="ew", pady=(0, 8))

        self._btn = ctk.CTkButton(
            btn_wrap, text="▶  Ejecutar Simulación",
            font=FONTS["button"],
            height=SIZES["button_height"],
            corner_radius=SIZES["corner_radius"],
            fg_color=COLORS["green"],
            hover_color=COLORS["green_hover"],
            text_color="#FFFFFF",
            command=self._ejecutar)
        self._btn.grid(row=2, column=0, sticky="ew")

    # ─────────────────────────────────────────────────────────────────────────
    def _render_modelo(self, modelo):
        for w in self._scroll.winfo_children():
            w.destroy()
        self._entries.clear()

        info  = MODELOS_INFO[modelo]
        vars_ = VARIABLES_INFO[modelo]

        # ── 1. Tarjeta principal ───────────────────────────
        card = ctk.CTkFrame(self._scroll,
                             fg_color=COLORS["surface"],
                             corner_radius=14,
                             border_width=1, border_color=COLORS["border"])
        card.grid(row=0, column=0, sticky="ew", padx=14, pady=(18, 0))
        card.grid_columnconfigure(0, weight=1)

        # Badge + título
        hdr = ctk.CTkFrame(card, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=14, pady=(14, 6))

        ctk.CTkLabel(hdr, text=" ƒ ",
                     font=("Arial", 13, "bold"),
                     text_color="#FFFFFF",
                     fg_color=COLORS["green"],
                     corner_radius=6).pack(side="left", padx=(0, 8))

        ctk.CTkLabel(hdr, text=info["titulo"],
                     font=("Arial", 11, "bold"),
                     text_color=COLORS["text_main"],
                     wraplength=200,
                     justify="left").pack(side="left")

        # Fórmula
        fbox = ctk.CTkFrame(card, fg_color=COLORS["card"],
                             corner_radius=8,
                             border_width=1, border_color=COLORS["border"])
        fbox.grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 10))

        ctk.CTkLabel(fbox, text=info["formula"],
                     font=("Arial", 15, "italic"),
                     text_color=COLORS["text_main"]).pack(padx=16, pady=10)

        # ── 2. Acordeón: qué significa cada variable ───────
        sec_vars = CollapsibleSection(card,
                                       title="¿Qué significa cada variable?",
                                       icon="▸")
        sec_vars.grid(row=2, column=0, sticky="ew", padx=14, pady=(0, 14))
        sec_vars.grid_columnconfigure(0, weight=1)

        for sym, name, desc in vars_:
            vrow = ctk.CTkFrame(sec_vars.body, fg_color="transparent")
            vrow.pack(fill="x", padx=12, pady=5)

            ctk.CTkLabel(vrow, text=sym,
                         font=("Arial", 12, "bold"),
                         text_color=COLORS["green"],
                         width=32, anchor="w").pack(side="left")

            txt = ctk.CTkFrame(vrow, fg_color="transparent")
            txt.pack(side="left", fill="x", expand=True)

            ctk.CTkLabel(txt, text=name,
                         font=("Arial", 10, "bold"),
                         text_color=COLORS["text_main"],
                         anchor="w").pack(anchor="w")
            ctk.CTkLabel(txt, text=desc,
                         font=("Arial", 9, "normal"),
                         text_color=COLORS["text_sub"],
                         anchor="w",
                         wraplength=190,
                         justify="left").pack(anchor="w")

        # ── 3. Parámetros iniciales ────────────────────────
        ctk.CTkLabel(self._scroll, text="PARÁMETROS INICIALES",
                     font=("Arial", 9, "bold"),
                     text_color=COLORS["text_hint"],
                     anchor="w").grid(row=1, column=0,
                                       sticky="w", padx=20, pady=(14, 4))

        for idx, (label, default) in enumerate(info["params"]):
            e = CustomEntry(self._scroll, label=label, placeholder=default)
            e.insert(0, default)
            e.grid(row=2+idx, column=0, sticky="ew", padx=14, pady=(0, 10))
            self._entries[label] = e

        next_row = 2 + len(info["params"])

        # ── 4. Acordeón: Calcular tasa de crecimiento r ───
        sec_r = CollapsibleSection(self._scroll,
                                    title="Calcular Tasa de Crecimiento (r)",
                                    icon="▸")
        sec_r.grid(row=next_row, column=0, sticky="ew",
                    padx=14, pady=(4, 14))
        sec_r.grid_columnconfigure(0, weight=1)
        self._build_calc_r(sec_r.body, modelo)

    # ─────────────────────────────────────────────────────────────────────────
    def _build_calc_r(self, body, modelo):
        """Calculadora de r. Fórmula: r = ln(Pf/P0) / t"""
        body.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(body,
                     text="Calcula r a partir de datos conocidos:",
                     font=("Arial", 9, "normal"),
                     text_color=COLORS["text_sub"],
                     anchor="w").pack(fill="x", padx=12, pady=(10, 6))

        # Fórmula de r
        ctk.CTkLabel(body, text="r  =  ln(Pf / P₀) / t",
                     font=("Arial", 12, "italic"),
                     text_color=COLORS["text_main"],
                     fg_color=COLORS["card"],
                     corner_radius=8).pack(fill="x", padx=12, pady=(0, 10))

        # Campos
        fields_r = [
            ("P₀  (población inicial)",  "100"),
            ("Pf  (población final)",    "200"),
            ("t   (tiempo transcurrido)","10"),
        ]
        self._r_entries = {}
        for lbl, dflt in fields_r:
            e = CustomEntry(body, label=lbl, placeholder=dflt)
            e.insert(0, dflt)
            e.pack(fill="x", padx=12, pady=(0, 8))
            self._r_entries[lbl] = e

        # Resultado
        self._r_result = ctk.CTkLabel(body, text="r = —",
                                       font=("Arial", 13, "bold"),
                                       text_color=COLORS["green"],
                                       fg_color=COLORS["green_glow"],
                                       corner_radius=8)
        self._r_result.pack(fill="x", padx=12, pady=(0, 6))

        # Botón calcular
        ctk.CTkButton(body, text="Calcular r",
                      font=FONTS["label"],
                      height=36, corner_radius=10,
                      fg_color=COLORS["green"],
                      hover_color=COLORS["green_hover"],
                      text_color="#FFFFFF",
                      command=self._calcular_r).pack(fill="x",
                                                     padx=12, pady=(0, 12))

        # Botón "usar este r"
        self._usar_r_btn = ctk.CTkButton(
            body, text="↑ Usar este r en parámetros",
            font=("Arial", 10, "normal"),
            height=30, corner_radius=8,
            fg_color="transparent",
            border_width=1, border_color=COLORS["border"],
            hover_color=COLORS["green_glow"],
            text_color=COLORS["green_dark"],
            command=self._usar_r)
        self._usar_r_btn.pack(fill="x", padx=12, pady=(0, 12))
        self._r_calculated = None

    def _calcular_r(self):
        try:
            # Validación simple local para la subcalculadora
            p0 = float(self._r_entries["P₀  (población inicial)"].get().strip())
            pf = float(self._r_entries["Pf  (población final)"].get().strip())
            t  = float(self._r_entries["t   (tiempo transcurrido)"].get().strip())

            if p0 <= 0 or pf <= 0 or t <= 0:
                self._r_result.configure(text="Error: valores deben ser > 0")
                return
            r = math.log(pf / p0) / t
            self._r_calculated = r
            self._r_result.configure(text=f"r  =  {r:.6f}")
        except Exception:
            self._r_result.configure(text="Error: Formato numérico inválido")

    def _usar_r(self):
        """
        🛠️ MODIFICACIÓN: Inyecta de forma robusta la tasa y fuerza a la UI 
        a procesar el cambio en los hilos del sistema operativo.
        """
        if self._r_calculated is None:
            return
        key = "Tasa de Crecimiento (r)"
        if key in self._entries:
            # Si agregaste el método set_value en CustomEntry, lo usamos.
            if hasattr(self._entries[key], 'set_value'):
                self._entries[key].set_value(f"{self._r_calculated:.6f}")
            else:
                self._entries[key].clear()
                self._entries[key].insert(0, f"{self._r_calculated:.6f}")
                self._entries[key].update_idletasks() # Asegura refresco inmediato en Tkinter
            
            # Avisamos en el panel de control inferior que fue exitosa la copia
            self._lbl_estado.configure(
                text=f" Tasa r = {self._r_calculated:.6f} inyectada",
                text_color=COLORS["green_dark"]
            )

    # ─────────────────────────────────────────────────────────────────────────
    def cambiar_modelo(self, modelo):
        if modelo != self._modelo_actual:
            self._modelo_actual = modelo
            self._render_modelo(modelo)
            if hasattr(self, '_lbl_estado'):
                self._lbl_estado.configure(text="")

    # ─────────────────────────────────────────────────────────────────────────
    def _ejecutar(self):
        """
        🛠️ MODIFICACIÓN: Lectura estricta y robusta de parámetros. 
        Maneja errores visuales en tiempo real y erradica el fallo silencioso de r=0.1
        """
        modelo = self._modelo_actual
        # Obtenemos los valores limpios eliminando espacios accidentales
        vals = {k: v.get().strip() for k, v in self._entries.items()}

        try:
            # 1. Validar que no haya cajas vacías
            for campo, valor in vals.items():
                if not valor:
                    raise ValueError(f"El campo '{campo}' está vacío.")

            # 2. Conversiones estrictas y captura de fallos de escritura
            try:
                p0 = float(vals.get("Población Inicial (P₀)"))
                if p0 < 0: raise ValueError()
            except ValueError:
                raise ValueError("P₀ (Población Inicial) debe ser un número ≥ 0.")

            try:
                r = float(vals.get("Tasa de Crecimiento (r)"))
            except ValueError:
                raise ValueError("r (Tasa de Crecimiento) debe ser un número decimal válido.")

            try:
                t = int(float(vals.get("Tiempo (t)")))
                if t <= 0: raise ValueError()
            except ValueError:
                raise ValueError("t (Tiempo) debe ser un número entero mayor a 0.")

            # 3. Matemáticas de la Simulación
            t_vals = list(range(t + 1))

            if modelo == "Modelo Exponencial":
                p_vals = [p0 * math.exp(r * ti) for ti in t_vals]

            else:  # Logístico
                try:
                    k = float(vals.get("Capacidad de Carga (K)"))
                    if k <= 0: raise ValueError()
                except ValueError:
                    raise ValueError("K (Capacidad de Carga) debe ser un número válido mayor a 0.")

                # Integración numérica Euler
                dt = 1.0
                p  = p0
                p_vals = [p]
                for _ in range(t):
                    dp = r * p * (1 - p / k) * dt
                    p  = max(0, p + dp)
                    p_vals.append(p)

            # 4. Si todo el proceso matemático es exitoso, actualizamos estado
            self._lbl_estado.configure(
                text=f"✅ Simulación exitosa\n(Parámetros validados, r = {r:.6f})",
                text_color=COLORS["green_dark"]
            )

            if self.on_result:
                self.on_result(modelo, t_vals, p_vals)

        except ValueError as ex:
            # Captura errores controlados por nosotros (campos vacíos, letras, negativos)
            self._lbl_estado.configure(
                text=f"❌ Error:\n{str(ex)}",
                text_color="#ef4444"  # Color Rojo de alerta
            )
        except Exception as ex:
            # Captura cualquier otro imprevisto matemático raro (ej: overflow numérico)
            self._lbl_estado.configure(
                text=f"💥 Error crítico matemático: {str(ex)}",
                text_color="#ef4444"
            )
            print(f"[SimPanel] Error al ejecutar: {ex}")

    def get_valores(self):
        return {k: v.get() for k, v in self._entries.items()}