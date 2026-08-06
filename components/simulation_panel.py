import math
import os
import sys
import customtkinter as ctk
from PIL import Image
from utils.theme import COLORS, FONTS, SIZES
from components.custom_entry import CustomEntry

def resolver_ruta_asset(ruta_relativa):
    if getattr(sys, 'frozen', False):
        ruta_base = sys._MEIPASS
    else:
        ruta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(ruta_base, ruta_relativa)

def _safe_float(val, default=0.0):
    try:
        return float(str(val).strip().replace(",", ""))
    except Exception:
        return default

def _safe_int(val, default=0):
    try:
        return int(float(str(val).strip()))
    except Exception:
        return default

MODELOS_INFO = {
    "Modelo Exponencial": {
        "titulo":   "Crecimiento sin restricciones ambientales",
        "eq_sol":   "P(t)  =  P₀ · e^(r · t)",
        "desc":     "La población crece proporcionalmente a su tamaño.\nNo existe límite superior.",
        "img_file": "ecuacion_exponencial.png",
        "variables": [
            ("P(t)",  "Población en el tiempo t",    "Número de individuos en un año dado"),
            ("P₀",   "Población inicial",            "Individuos al inicio (t = 0)"),
            ("r",    "Tasa de crecimiento",          "r > 0 crece  |  r < 0 decrece  |  calculada automáticamente"),
            ("t",    "Tiempo transcurrido",          "Diferencia en años desde el año inicial"),
            ("e",    "Número de Euler",              "≈ 2.71828 — base del crecimiento continuo"),
        ],
        "extra_params": [],
    },
    "Modelo Logístico": {
        "titulo":   "Crecimiento con capacidad de carga",
        "eq_sol":   "P(t)  =  K / (1 + A · e^(−r·t))     A = (K−P₀)/P₀",
        "desc":     "La población crece hasta el límite K impuesto\npor los recursos disponibles.",
        "img_file": "ecuacion_logistica.png",
        "variables": [
            ("P(t)",  "Población en el tiempo t",    "Número de individuos en un año dado"),
            ("P₀",   "Población inicial",            "Individuos al inicio (t = 0)"),
            ("r",    "Tasa de crecimiento",          "Velocidad intrínseca per cápita — calculada automáticamente"),
            ("K",    "Capacidad de carga",           "Límite máximo que el ambiente puede sostener"),
            ("A",    "Constante auxiliar",           "A = (K − P₀) / P₀"),
            ("e",    "Número de Euler",              "≈ 2.71828"),
        ],
        "extra_params": [
            ("Capacidad de Carga (K)", "10000", "individuos",
             "Número máximo de individuos que el ecosistema puede sostener."),
        ],
    },
}

class _Collapsible(ctk.CTkFrame):
    def __init__(self, parent, title, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self._open = False

        self._btn = ctk.CTkButton(
            self, text=f"  ▸  {title}",
            font=("Arial", 13, "bold"),
            height=40, corner_radius=10,
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
            self._btn.configure(text=self._btn.cget("text").replace("▸", "▾"))
        else:
            self._body.grid_forget()
            self._btn.configure(text=self._btn.cget("text").replace("▾", "▸"))

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
            font=("Arial", 12),
            text_color=COLORS["text_hint"],
            anchor="w", wraplength=390, justify="left")
        self._status_lbl.grid(row=0, column=0, sticky="ew", padx=14, pady=6)

        btn_wrap = ctk.CTkFrame(self, fg_color=COLORS["card"])
        btn_wrap.grid(row=2, column=0, sticky="ew", padx=14, pady=(8, 14))
        btn_wrap.grid_columnconfigure(0, weight=1)
        ctk.CTkFrame(btn_wrap, height=1,
                     fg_color=COLORS["border"]).grid(row=0, column=0,
                                                     sticky="ew", pady=(0, 8))
        ctk.CTkButton(
            btn_wrap, text="▶  Ejecutar Simulación",
            font=("Arial", 16, "bold"),
            height=52, corner_radius=SIZES["corner_radius"],
            fg_color=COLORS["green"],
            hover_color=COLORS["green_hover"],
            text_color="#FFFFFF",
            command=self._ejecutar,
        ).grid(row=1, column=0, sticky="ew")

    def _render_modelo(self, modelo):
        for w in self._scroll.winfo_children():
            w.destroy()
        self._entries.clear()
        self._r_calculated = None
        self._r_lbl = None

        info = MODELOS_INFO[modelo]

        # 1. Card de información del modelo y fórmula
        card = ctk.CTkFrame(self._scroll, fg_color=COLORS["surface"],
                            corner_radius=14,
                            border_width=1, border_color=COLORS["border"])
        card.grid(row=0, column=0, sticky="ew", padx=14, pady=(16, 0))
        card.grid_columnconfigure(0, weight=1)

        hdr = ctk.CTkFrame(card, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=14, pady=(14, 6))
        ctk.CTkLabel(hdr, text=" ƒ ",
                     font=("Arial", 14, "bold"),
                     text_color="#FFFFFF",
                     fg_color=COLORS["green"],
                     corner_radius=6).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(hdr, text=info["titulo"],
                     font=("Arial", 14, "bold"),
                     text_color=COLORS["text_main"],
                     wraplength=260, justify="left").pack(side="left")

        ctk.CTkLabel(card, text=info["desc"],
                     font=("Arial", 13),
                     text_color=COLORS["text_sub"],
                     anchor="w", wraplength=370,
                     justify="left").grid(row=1, column=0, sticky="w",
                                          padx=14, pady=(0, 8))

        ctk.CTkLabel(card, text="Ecuación diferencial:",
                     font=("Arial", 12, "bold"),
                     text_color=COLORS["text_hint"],
                     anchor="w").grid(row=2, column=0, sticky="w", padx=14)

        fb1 = ctk.CTkFrame(card, fg_color="#FFFFFF", corner_radius=8,
                           border_width=1, border_color=COLORS["border"])
        fb1.grid(row=3, column=0, sticky="ew", padx=14, pady=(4, 8))
        
        ruta_relativa = os.path.join("assets", info["img_file"])
        img_path = resolver_ruta_asset(ruta_relativa)
        try:
            pil_image = Image.open(img_path)
            original_width, original_height = pil_image.size
            target_height = 45
            target_width = int((target_height / original_height) * original_width)
            
            ctk_img = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(target_width, target_height))
            img_label = ctk.CTkLabel(fb1, text="", image=ctk_img)
            img_label.pack(padx=14, pady=12)
        except Exception:
            ctk.CTkLabel(fb1, text=f"[ Imagen no encontrada: {info['img_file']} ]", 
                         text_color="red").pack(padx=14, pady=12)

        ctk.CTkLabel(card, text="Solución analítica:",
                     font=("Arial", 12, "bold"),
                     text_color=COLORS["text_hint"],
                     anchor="w").grid(row=4, column=0, sticky="w", padx=14)

        fb2 = ctk.CTkFrame(card, fg_color=COLORS["green_subtle"], corner_radius=8,
                           border_width=1, border_color=COLORS["green"])
        fb2.grid(row=5, column=0, sticky="ew", padx=14, pady=(4, 8))
        ctk.CTkLabel(fb2, text=info["eq_sol"],
                     font=("Arial", 14, "bold"),
                     text_color=COLORS["green_dark"],
                     wraplength=360, justify="center").pack(padx=14, pady=8)

        glos = _Collapsible(card, "Glosario de variables")
        glos.grid(row=6, column=0, sticky="ew", padx=14, pady=(0, 14))
        for sym, name, desc in info["variables"]:
            rf = ctk.CTkFrame(glos.body, fg_color="transparent")
            rf.pack(fill="x", padx=12, pady=4)
            ctk.CTkLabel(rf, text=sym,
                         font=("Arial", 14, "bold"),
                         text_color=COLORS["green"],
                         width=44, anchor="w").pack(side="left")
            col_ = ctk.CTkFrame(rf, fg_color="transparent")
            col_.pack(side="left", fill="x", expand=True)
            ctk.CTkLabel(col_, text=name,
                         font=("Arial", 13, "bold"),
                         text_color=COLORS["text_main"],
                         anchor="w").pack(anchor="w")
            ctk.CTkLabel(col_, text=desc,
                         font=("Arial", 12),
                         text_color=COLORS["text_sub"],
                         anchor="w", wraplength=250,
                         justify="left").pack(anchor="w")

        # 2. Card de Unidad de Tiempo e Intervalo
        tiempo_card = ctk.CTkFrame(
            self._scroll,
            fg_color=COLORS["surface"],
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border"]
        )
        tiempo_card.grid(row=1, column=0, sticky="ew", padx=14, pady=(20, 10))

        ctk.CTkLabel(tiempo_card, text="UNIDAD DE TIEMPO", font=("Arial", 12, "bold"),
                     text_color=COLORS["text_hint"]).pack(anchor="w", padx=14, pady=(10, 4))
        ctk.CTkLabel(tiempo_card, text="Selecciona la unidad en la que se realizará la simulación:",
                     font=("Arial", 12), text_color=COLORS["text_sub"]).pack(anchor="w", padx=14, pady=(0, 8))

        self._unidad_tiempo = ctk.CTkComboBox(
            tiempo_card,
            values=["Segundos", "Minutos", "Horas", "Días", "Meses", "Años"],
            height=35
        )
        self._unidad_tiempo.set("Años")
        self._unidad_tiempo.pack(fill="x", padx=14, pady=(0, 12))

        ctk.CTkLabel(tiempo_card, text="INTERVALO DE MUESTRA", font=("Arial", 12, "bold"),
                     text_color=COLORS["text_hint"]).pack(anchor="w", padx=14, pady=(0, 4))

        self._intervalo = ctk.CTkEntry(tiempo_card, placeholder_text="Ejemplo: 1, 5, 10")
        self._intervalo.insert(0, "1")
        self._intervalo.pack(fill="x", padx=14, pady=(0, 12))

        # 3. Entradas de datos del problema
        ctk.CTkLabel(self._scroll, text="DATOS DEL PROBLEMA",
                     font=("Arial", 12, "bold"), text_color=COLORS["text_hint"],
                     anchor="w").grid(row=2, column=0, sticky="w", padx=18, pady=(20, 6))

        campos_comunes = [
            ("t_inicial", "Tiempo inicial (t₀)", "0", "Tiempo donde inicia la medición."),
            ("p0", "Población inicial (P₀)", "3500", "Número de individuos en el tiempo inicial."),
            ("t_ref", "Tiempo de referencia (t₁)", "10", "Tiempo de la segunda medición usada para calcular r."),
            ("pf", "Población de referencia (Pf)", "5000", "Número de individuos en el tiempo de referencia."),
            ("t_objetivo", "Tiempo objetivo (proyección)", "50", "Tiempo donde se calculará la población futura."),
        ]

        for idx, (key, label, dflt, tip) in enumerate(campos_comunes):
            e = CustomEntry(self._scroll, label=label, placeholder=dflt, tooltip=tip)
            e.insert(0, dflt)
            e.grid(row=3 + idx, column=0, sticky="ew", padx=14, pady=(0, 15))
            self._entries[key] = e

        next_row = 3 + len(campos_comunes)

        for i, (label, dflt, unit, tip) in enumerate(info["extra_params"]):
            e = CustomEntry(self._scroll, label=label, placeholder=dflt, unit=unit, tooltip=tip)
            e.insert(0, dflt)
            e.grid(row=next_row + i, column=0, sticky="ew", padx=14, pady=(0, 10))
            self._entries[label] = e

        # 4. Tasa r calculada
        r_card = ctk.CTkFrame(self._scroll, fg_color=COLORS["surface"],
                             corner_radius=12, border_width=1, border_color=COLORS["border"])
        r_card.grid(row=next_row + len(info["extra_params"]) + 1, column=0,
                    sticky="ew", padx=14, pady=(14, 14))
        r_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(r_card, text="Tasa de crecimiento calculada  (r)",
                     font=("Arial", 12, "bold"), text_color=COLORS["text_hint"],
                     anchor="w").grid(row=0, column=0, sticky="w", padx=14, pady=(10, 2))

        self._r_lbl = ctk.CTkLabel(
            r_card, text="r  =  —  (ejecuta la simulación para calcular)",
            font=("Arial", 15, "italic"), text_color=COLORS["text_sub"],
            fg_color=COLORS["card"], corner_radius=8,
            anchor="w", wraplength=360)
        self._r_lbl.grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 12))

    def _ejecutar(self):
        modelo = self._modelo_actual

        def read(key, default):
            e = self._entries.get(key)
            return _safe_float(e.get(), default) if e else default

        try:
            t0 = _safe_float(self._entries["t_inicial"].get(), 0)
            p0 = read("p0", 3500.0)
            t_ref = _safe_float(self._entries["t_ref"].get(), 10)
            pf = read("pf", 5000.0)
            t_obj = _safe_float(self._entries["t_objetivo"].get(), 50)
            
            if p0 <= 0:
                self._set_status("⚠  P₀ debe ser mayor que 0", error=True); return
            if pf <= 0:
                self._set_status("⚠  Pf debe ser mayor que 0", error=True); return
            if t_ref <= t0:
                self._set_status("⚠ El tiempo de referencia debe ser mayor que el tiempo inicial",
                                error=True); return
            if t_obj <= t0:
                self._set_status("⚠ El tiempo objetivo debe ser mayor que el tiempo inicial",
                                error=True); return

            dt_ref = t_ref - t0
            dt_obj = t_obj - t0

            if modelo == "Modelo Exponencial":
                r = math.log(pf / p0) / dt_ref
                texto_r = f"r  =  ln({pf:g} / {p0:g}) / {dt_ref}  =  {r:.6f}"
            else:
                k = read("Capacidad de Carga (K)", 10000.0)
                if k <= 0:
                    self._set_status("⚠  K debe ser mayor que 0", error=True); return
                if p0 >= k:
                    self._set_status("⚠  P₀ debe ser menor que K", error=True); return
                if pf >= k:
                    self._set_status("⚠  Pf debe ser menor que K", error=True); return
                
                numerador = pf * (k - p0)
                denominador = p0 * (k - pf)
                r = math.log(numerador / denominador) / dt_ref
                texto_r = f"r  =  (1/{dt_ref}) · ln( ({pf:g}({k:g}-{p0:g})) / ({p0:g}({k:g}-{pf:g})) )  =  {r:.6f}"

            self._r_calculated = r
            if self._r_lbl:
                self._r_lbl.configure(
                    text=texto_r,
                    text_color=COLORS["green_dark"])

            paso = int(self._intervalo.get())
            tiempos = list(range(int(t0), int(t_obj) + 1, paso))
            if tiempos[-1] != t_obj:
                tiempos.append(t_obj)
            t_vals = [t - t0 for t in tiempos]

            if modelo == "Modelo Exponencial":
                try:
                    p_vals = [p0 * math.exp(r * t) for t in t_vals]
                except OverflowError:
                    self._set_status("⚠  Desbordamiento: valores demasiado grandes", error=True)
                    return

                p_final  = p0 * math.exp(r * dt_obj)
                
                # FÓRMULA SUSTITUIDA CON VALORES REALES
                eq_sustituida = f"P(t) = {p0:g} · e^({r:.6f} · t)"
                
                # MENSAJE SUPERIOR LIMPIO CON PARÁMETROS DE ENTRADA
                sol_str = (
                    f"Parámetros: P₀ = {p0:g}  |  r = {r:.6f}  |  t = {t_obj:g}\n\n"
                    f"Resultado: {p_final:,.0f} habitantes"
                )
                
                # ACTUALIZACIÓN AQUÍ: Se añade "unidad_tiempo"
                params = {"P₀": p0, "r": r, "t0": t0,
                          "t_obj": t_obj, "sol_str": sol_str, "eq_sustituida": eq_sustituida,
                          "unidad_tiempo": self._unidad_tiempo.get()}

            else:
                A = (k - p0) / p0
                try:
                    p_vals = [k / (1 + A * math.exp(-r * t)) for t in t_vals]
                except OverflowError:
                    p_vals = [k if t > 0 else p0 for t in t_vals]

                p_final = k / (1 + A * math.exp(-r * dt_obj))
                
                # FÓRMULA SUSTITUIDA CON VALORES REALES
                eq_sustituida = f"P(t) = {k:g} / (1 + {A:.6f} · e^(-{r:.6f} · t))"
                
                # MENSAJE SUPERIOR LIMPIO CON PARÁMETROS DE ENTRADA
                sol_str = (
                    f"Parámetros: P₀ = {p0:g}  |  K = {k:g}  |  r = {r:.6f}  |  t = {t_obj:g}\n\n"
                    f"Resultado: {p_final:,.0f} habitantes"
                )
                
                # ACTUALIZACIÓN AQUÍ: Se añade "unidad_tiempo"
                params = {"P₀": p0, "r": r, "K": k, "A": A,
                          "t0": t0, "t_obj": t_obj, "sol_str": sol_str, "eq_sustituida": eq_sustituida,
                          "unidad_tiempo": self._unidad_tiempo.get()}

            self._set_status(
                f"✓  r = {r:.6f}   |   "
                f"P({t_obj}) ≈ {p_final:,.0f} habitantes")

            if self.on_result:
                self.on_result(modelo, tiempos, p_vals, params)

        except Exception as ex:
            self._set_status(f"Error: {ex}", error=True)
            import traceback; traceback.print_exc()

    def cambiar_modelo(self, modelo):
        if modelo != self._modelo_actual:
            self._modelo_actual = modelo
            self._render_modelo(modelo)
            if self._status_lbl:
                self._status_lbl.configure(text="")

    def _set_status(self, msg, error=False):
        if self._status_lbl:
            color = "#EF4444" if error else COLORS["text_hint"]
            self._status_lbl.configure(text=msg, text_color=color)