import tkinter as tk
import customtkinter as ctk
from utils.theme import COLORS, FONTS, SIZES


def _draw_logo(parent, size=70, bg="#FFFFFF"):
    scale = size / 100
    c = tk.Canvas(parent, width=size, height=size,
                  highlightthickness=0, bg=bg)
    c.create_rectangle(0, 0, size, size, fill="#F4F4F5", outline="")
    def sc(v): return int(v * scale)
    c.create_line(sc(25),sc(75),sc(50),sc(45),sc(75),sc(45),
                  fill="#22c55e", width=max(2,int(5*scale)),
                  capstyle="round", joinstyle="round")
    c.create_line(sc(25),sc(75),sc(60),sc(75),sc(75),sc(45),
                  fill="#d4d4d8", width=max(1,int(4*scale)),
                  capstyle="round", joinstyle="round")
    c.create_line(sc(50),sc(45),sc(60),sc(75),
                  fill="#e4e4e7", width=max(1,int(2*scale)))
    def oval(cx, cy, r, fill):
        cx,cy,r = sc(cx),sc(cy),max(2,int(r*scale))
        c.create_oval(cx-r,cy-r,cx+r,cy+r,fill=fill,outline="")
    oval(25,75,7,"#18181b"); oval(50,45,6,"#71717a")
    oval(60,75,5,"#a1a1aa"); oval(75,45,9,"#22c55e")
    oval(75,45,3,"#ffffff")
    return c


class IntroView(ctk.CTkFrame):
    def __init__(self, parent, on_continue=None, **kwargs):
        super().__init__(parent, fg_color="#FFFFFF",
                         corner_radius=0, **kwargs)
        self.on_continue = on_continue
        self._build()

    def _build(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        canvas = tk.Canvas(self, highlightthickness=0, bd=0, bg="#FFFFFF")
        canvas.place(x=0, y=0, relwidth=1, relheight=1)

        def redraw(event=None):
            canvas.delete("all")
            w = canvas.winfo_width()  or 1280
            h = canvas.winfo_height() or 800
            canvas.create_rectangle(0, 0, w, h, fill="#FFFFFF", outline="")
            canvas.create_oval(-w*0.2,-h*0.2, w*0.65,h*0.65,
                               fill="#DCFCE7", outline="")
            canvas.create_oval(w*0.4,h*0.5, w*1.2,h*1.3,
                               fill="#BBF7D0", outline="")
            canvas.create_oval(w*0.1,h*0.15, w*0.9,h*0.95,
                               fill="#ECFDF5", outline="")
            canvas.create_oval(-w*0.05,-h*0.3, w*0.9,h*0.45,
                               fill="#FFFFFF", outline="", stipple="gray75")

        canvas.bind("<Configure>", redraw)
        canvas.after(50, redraw)

        scroll = ctk.CTkScrollableFrame(
            self, fg_color="transparent",
            scrollbar_button_color=COLORS["border"])
        scroll.place(relx=0, rely=0, relwidth=1, relheight=1)
        scroll.grid_columnconfigure(0, weight=1)

        content = ctk.CTkFrame(scroll, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=80, pady=60)

        # ── Header ────────────────────────────────────────────────────
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(anchor="center", pady=(0, 12))

        logo = _draw_logo(header, size=72, bg="#FFFFFF")
        logo.pack(side="left", padx=(0, 20))

        title_col = ctk.CTkFrame(header, fg_color="transparent")
        title_col.pack(side="left")
        ctk.CTkLabel(title_col, text="SDCP",
                     font=("Arial", 44, "bold"),
                     text_color=COLORS["text_main"]).pack(anchor="w")
        ctk.CTkLabel(title_col,
                     text="Sistemas Dinámicos de Crecimiento Poblacional",
                     font=("Arial", 16, "normal"),
                     text_color=COLORS["text_sub"]).pack(anchor="w", pady=(4,0))

        # ── Sección 1: ¿Qué es un sistema dinámico? ───────────────────
        self._sec(content, "¿Qué es un Sistema Dinámico?")

        intro_card = ctk.CTkFrame(content, fg_color=COLORS["card"],
                                   corner_radius=16,
                                   border_width=1, border_color=COLORS["border"])
        intro_card.pack(fill="x", pady=(0, 32))

        ctk.CTkLabel(
            intro_card,
            text="Un sistema dinámico es un modelo matemático que describe cómo "
                 "evoluciona o cambia una situación a lo largo del tiempo.\n\n"
                 "Para medir matemáticamente estos cambios se usan las Ecuaciones "
                 "Diferenciales Ordinarias (EDO). Una ecuación diferencial relaciona "
                 "una función desconocida con sus derivadas, donde la derivada "
                 "representa la tasa de cambio, es decir, qué tan rápido varía "
                 "la población en cada instante de tiempo.",
            font=("Arial", 15, "normal"),
            text_color=COLORS["text_sub"],
            justify="left", anchor="w",
            wraplength=1000).pack(padx=28, pady=24, anchor="w")

        # ── Sección 2: Modelo Exponencial ─────────────────────────────
        self._sec(content, "Modelo Exponencial de Malthus")
        self._card_exp(content)

        # ── Sección 3: Modelo Logístico ───────────────────────────────
        self._sec(content, "Modelo Logístico")
        self._card_log(content)

        # ── Sección 4: Tabla de variables ─────────────────────────────
        self._sec(content, "Resumen de Variables y Constantes")
        self._tabla_vars(content)

        # ── Botón ─────────────────────────────────────────────────────
        ctk.CTkButton(content,
                      text="Ir al Simulador  →",
                      font=("Arial", 18, "bold"),
                      height=60, corner_radius=14,
                      fg_color=COLORS["green"],
                      hover_color=COLORS["green_hover"],
                      text_color="#FFFFFF",
                      command=self._continue).pack(fill="x", pady=(36, 8))

        ctk.CTkLabel(content,
                     text="Puedes volver a esta pantalla desde el dashboard en cualquier momento.",
                     font=("Arial", 13, "normal"),
                     text_color=COLORS["text_hint"],
                     justify="center").pack(pady=(0, 48))

    # ── Helpers ───────────────────────────────────────────────────────
    def _sec(self, parent, text):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=(0, 14), anchor="w")
        ctk.CTkFrame(row, width=5, height=30,
                     fg_color=COLORS["green"],
                     corner_radius=3).pack(side="left", padx=(0, 14))
        ctk.CTkLabel(row, text=text,
                     font=("Arial", 21, "bold"),
                     text_color=COLORS["text_main"]).pack(side="left")

    # ── Card Modelo Exponencial ────────────────────────────────────────
    def _card_exp(self, parent):
        card = ctk.CTkFrame(parent, fg_color=COLORS["card"],
                             corner_radius=16,
                             border_width=1, border_color=COLORS["border"])
        card.pack(fill="x", pady=(0, 32))
        card.grid_columnconfigure(0, weight=1)

        # Badge
        hdr = ctk.CTkFrame(card, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="w", padx=26, pady=(22, 8))
        ctk.CTkLabel(hdr, text="  Malthus  ",
                     font=("Arial", 14, "bold"),
                     text_color="#FFFFFF",
                     fg_color=COLORS["green"],
                     corner_radius=8).pack(side="left", padx=(0, 14))
        ctk.CTkLabel(hdr,
                     text="La velocidad de crecimiento es directamente proporcional "
                          "al número de individuos existentes.",
                     font=("Arial", 14, "normal"),
                     text_color=COLORS["text_sub"]).pack(side="left")

        # Ecuaciones lado a lado
        eq = ctk.CTkFrame(card, fg_color="transparent")
        eq.grid(row=1, column=0, sticky="ew", padx=26, pady=(0, 18))
        eq.grid_columnconfigure((0,1), weight=1)

        for i, (lbl, formula, bg, bc, fc) in enumerate([
            ("Ecuación diferencial",
             "dP/dt = r · P",
             COLORS["card"], COLORS["border"], COLORS["text_main"]),
            ("Solución analítica",
             "P(t) = P₀ · e^(r·t)",
             COLORS["green_subtle"], COLORS["green"], COLORS["green_dark"]),
        ]):
            col = ctk.CTkFrame(eq, fg_color="transparent")
            col.grid(row=0, column=i, sticky="ew",
                     padx=(0,8) if i==0 else (8,0))
            ctk.CTkLabel(col, text=lbl,
                         font=("Arial", 13, "bold"),
                         text_color=COLORS["text_hint"],
                         anchor="w").pack(anchor="w", pady=(0,5))
            box = ctk.CTkFrame(col, fg_color=bg, corner_radius=10,
                               border_width=1, border_color=bc)
            box.pack(fill="x")
            ctk.CTkLabel(box, text=formula,
                         font=("Arial", 17, "italic"),
                         text_color=fc).pack(padx=18, pady=14)

        # Variables
        vf = ctk.CTkFrame(card, fg_color=COLORS["surface"], corner_radius=10)
        vf.grid(row=2, column=0, sticky="ew", padx=26, pady=(0, 16))

        ctk.CTkLabel(vf, text="Variables del modelo:",
                     font=("Arial", 14, "bold"),
                     text_color=COLORS["text_main"],
                     anchor="w").pack(anchor="w", padx=18, pady=(14,8))

        vars_exp = [
            ("P(t)", "Población en el tiempo t",
             "Variable dependiente: número de individuos en el instante t"),
            ("P₀",  "Población inicial",
             "Valor de P cuando t = 0 — es la condición inicial del problema"),
            ("r",   "Tasa de crecimiento",
             "r > 0: población crece   |   r < 0: población decrece   |   r = 0: constante"),
            ("t",   "Tiempo",
             "Variable independiente. Toma valores 0, 1, 2, … hasta el valor ingresado"),
            ("e",   "Número de Euler",
             "Constante matemática ≈ 2.71828, base del crecimiento continuo"),
            ("dP/dt","Tasa de cambio",
             "Derivada de P respecto a t: velocidad con que cambia la población"),
        ]

        for sym, name, desc in vars_exp:
            vrow = ctk.CTkFrame(vf, fg_color="transparent")
            vrow.pack(fill="x", padx=18, pady=4)
            ctk.CTkLabel(vrow, text=sym,
                         font=("Arial", 16, "bold"),
                         text_color=COLORS["green"],
                         width=52, anchor="w").pack(side="left")
            ctk.CTkLabel(vrow, text=f"{name}:",
                         font=("Arial", 14, "bold"),
                         text_color=COLORS["text_main"],
                         anchor="w", width=220).pack(side="left")
            ctk.CTkLabel(vrow, text=desc,
                         font=("Arial", 14, "normal"),
                         text_color=COLORS["text_sub"],
                         anchor="w").pack(side="left")

        ctk.CTkFrame(vf, height=1,
                     fg_color=COLORS["border"]).pack(fill="x", padx=18, pady=10)

        ctk.CTkLabel(vf,
                     text="⚠  Limitación: este modelo asume que los recursos nunca se agotan, "
                          "lo que produce un crecimiento ilimitado que no ocurre en la realidad.",
                     font=("Arial", 14, "normal"),
                     text_color="#92400E",
                     fg_color="#FFFBEB",
                     corner_radius=8,
                     wraplength=920,
                     justify="left",
                     anchor="w").pack(fill="x", padx=18, pady=(0, 14))

        # Ejemplo
        ex = ctk.CTkFrame(card, fg_color="#F0FDF4",
                           corner_radius=12,
                           border_width=1, border_color=COLORS["green"])
        ex.grid(row=3, column=0, sticky="ew", padx=26, pady=(0, 24))

        ctk.CTkLabel(ex,
                     text="📋  Ejemplo resuelto — Cultivo de bacterias",
                     font=("Arial", 16, "bold"),
                     text_color=COLORS["green_dark"],
                     anchor="w").pack(anchor="w", padx=22, pady=(18, 8))

        ctk.CTkLabel(ex,
                     text="Datos:  P₀ = 150 bacterias  |  P(1) = 200 bacterias  |  t en horas",
                     font=("Arial", 15, "normal"),
                     text_color=COLORS["text_main"],
                     anchor="w").pack(anchor="w", padx=22, pady=(0, 12))

        pasos = [
            ("1", "Calcular la tasa r usando P(1) = 200",
             "200 = 150 · e^(r·1)\n"
             "e^r = 200/150 = 4/3\n"
             "r = ln(4/3)  ≈  0.2877 h⁻¹"),
            ("2", "Escribir la solución particular",
             "P(t) = 150 · e^(0.2877·t)"),
            ("3", "Calcular la población a las 2 horas",
             "P(2) = 150 · e^(0.2877 · 2)  ≈  266.67  ≈  267 bacterias"),
            ("4", "¿Cuándo se triplica la población?",
             "150 · e^(0.2877·t) = 450\n"
             "e^(0.2877·t) = 3\n"
             "t = ln(3) / 0.2877  ≈  3.82 horas  ≈  3h 49min"),
        ]

        for num, title, detalle in pasos:
            prow = ctk.CTkFrame(ex, fg_color="transparent")
            prow.pack(fill="x", padx=22, pady=(0, 12))

            ctk.CTkLabel(prow, text=num,
                         font=("Arial", 13, "bold"),
                         text_color=COLORS["green_dark"],
                         fg_color=COLORS["green_glow"],
                         width=30, height=30,
                         corner_radius=15).pack(side="left", padx=(0,14), anchor="n", pady=2)

            tcol = ctk.CTkFrame(prow, fg_color="transparent")
            tcol.pack(side="left", fill="x", expand=True)
            ctk.CTkLabel(tcol, text=title,
                         font=("Arial", 15, "bold"),
                         text_color=COLORS["text_main"],
                         anchor="w").pack(anchor="w")
            ctk.CTkLabel(tcol, text=detalle,
                         font=("Courier", 14, "normal"),
                         text_color=COLORS["text_sub"],
                         anchor="w", justify="left").pack(anchor="w")

        ctk.CTkFrame(ex, height=1).pack(pady=10)

    # ── Card Modelo Logístico ──────────────────────────────────────────
    def _card_log(self, parent):
        card = ctk.CTkFrame(parent, fg_color=COLORS["card"],
                             corner_radius=16,
                             border_width=1, border_color=COLORS["border"])
        card.pack(fill="x", pady=(0, 32))
        card.grid_columnconfigure(0, weight=1)

        hdr = ctk.CTkFrame(card, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="w", padx=26, pady=(22, 8))
        ctk.CTkLabel(hdr, text="  Logístico  ",
                     font=("Arial", 14, "bold"),
                     text_color="#FFFFFF",
                     fg_color="#3B82F6",
                     corner_radius=8).pack(side="left", padx=(0, 14))
        ctk.CTkLabel(hdr,
                     text="Introduce la Capacidad de Carga K: el límite máximo "
                          "que el ambiente puede sostener.",
                     font=("Arial", 14, "normal"),
                     text_color=COLORS["text_sub"]).pack(side="left")

        # Ecuaciones
        eq = ctk.CTkFrame(card, fg_color="transparent")
        eq.grid(row=1, column=0, sticky="ew", padx=26, pady=(0, 18))
        eq.grid_columnconfigure((0,1), weight=1)

        for i, (lbl, formula, bg, bc, fc) in enumerate([
            ("Ecuación diferencial",
             "dP/dt = r · P · (1 - P/K)",
             COLORS["card"], COLORS["border"], COLORS["text_main"]),
            ("Solución analítica",
             "P(t) = K / (1 + A · e^(-r·t))\nA = (K - P₀) / P₀",
             "#EFF6FF", "#3B82F6", "#1D4ED8"),
        ]):
            col = ctk.CTkFrame(eq, fg_color="transparent")
            col.grid(row=0, column=i, sticky="ew",
                     padx=(0,8) if i==0 else (8,0))
            ctk.CTkLabel(col, text=lbl,
                         font=("Arial", 13, "bold"),
                         text_color=COLORS["text_hint"],
                         anchor="w").pack(anchor="w", pady=(0,5))
            box = ctk.CTkFrame(col, fg_color=bg, corner_radius=10,
                               border_width=1, border_color=bc)
            box.pack(fill="x")
            ctk.CTkLabel(box, text=formula,
                         font=("Arial", 16, "italic"),
                         text_color=fc,
                         justify="center").pack(padx=18, pady=14)

        # Variables
        vf = ctk.CTkFrame(card, fg_color=COLORS["surface"], corner_radius=10)
        vf.grid(row=2, column=0, sticky="ew", padx=26, pady=(0, 16))

        ctk.CTkLabel(vf, text="Variables del modelo:",
                     font=("Arial", 14, "bold"),
                     text_color=COLORS["text_main"],
                     anchor="w").pack(anchor="w", padx=18, pady=(14,8))

        vars_log = [
            ("P(t)", "Población en t",
             "Número de individuos en el instante t"),
            ("P₀",  "Población inicial",
             "Valor de P cuando t = 0 — condición inicial del problema"),
            ("r",   "Tasa de crecimiento",
             "Velocidad intrínseca de crecimiento per cápita"),
            ("K",   "Capacidad de carga",
             "Número máximo de individuos que el ambiente puede sostener"),
            ("A",   "Constante auxiliar",
             "A = (K − P₀) / P₀ — determina la forma de la curva"),
            ("e",   "Número de Euler",
             "Constante matemática ≈ 2.71828"),
        ]

        for sym, name, desc in vars_log:
            vrow = ctk.CTkFrame(vf, fg_color="transparent")
            vrow.pack(fill="x", padx=18, pady=4)
            ctk.CTkLabel(vrow, text=sym,
                         font=("Arial", 16, "bold"),
                         text_color="#3B82F6",
                         width=52, anchor="w").pack(side="left")
            ctk.CTkLabel(vrow, text=f"{name}:",
                         font=("Arial", 14, "bold"),
                         text_color=COLORS["text_main"],
                         anchor="w", width=220).pack(side="left")
            ctk.CTkLabel(vrow, text=desc,
                         font=("Arial", 14, "normal"),
                         text_color=COLORS["text_sub"],
                         anchor="w").pack(side="left")

        ctk.CTkFrame(vf, height=1,
                     fg_color=COLORS["border"]).pack(fill="x", padx=18, pady=10)

        # Comportamiento
        ctk.CTkLabel(vf, text="Comportamiento de la curva sigmoidea (forma de S):",
                     font=("Arial", 14, "bold"),
                     text_color=COLORS["text_main"],
                     anchor="w").pack(anchor="w", padx=18, pady=(0,8))

        bf = ctk.CTkFrame(vf, fg_color="transparent")
        bf.pack(fill="x", padx=18, pady=(0,14))
        bf.grid_columnconfigure((0,1,2), weight=1)

        for i, (icon, title, desc) in enumerate([
            ("📈", "Fase inicial",
             "Cuando la población es pequeña, crece casi de forma exponencial."),
            ("📉", "Desaceleración",
             "Al acercarse a K los recursos escasean y el crecimiento se frena."),
            ("📊", "Equilibrio",
             "La población se estabiliza cerca de K y deja de crecer."),
        ]):
            bc = ctk.CTkFrame(bf, fg_color=COLORS["card"],
                               corner_radius=10,
                               border_width=1, border_color=COLORS["border"])
            bc.grid(row=0, column=i, sticky="nsew",
                    padx=(0,6) if i<2 else 0)
            ctk.CTkLabel(bc, text=icon,
                         font=("Arial", 22)).pack(pady=(12,4))
            ctk.CTkLabel(bc, text=title,
                         font=("Arial", 13, "bold"),
                         text_color=COLORS["text_main"]).pack()
            ctk.CTkLabel(bc, text=desc,
                         font=("Arial", 12, "normal"),
                         text_color=COLORS["text_sub"],
                         wraplength=210, justify="center").pack(padx=10, pady=(4,12))

        # Ejemplo
        ex = ctk.CTkFrame(card, fg_color="#EFF6FF",
                           corner_radius=12,
                           border_width=1, border_color="#3B82F6")
        ex.grid(row=3, column=0, sticky="ew", padx=26, pady=(0, 24))

        ctk.CTkLabel(ex,
                     text="📋  Ejemplo — Población de peces en un lago",
                     font=("Arial", 16, "bold"),
                     text_color="#1D4ED8",
                     anchor="w").pack(anchor="w", padx=22, pady=(18, 8))

        ctk.CTkLabel(ex,
                     text="Datos:  P₀ = 100 peces  |  r = 0.4 por año  |  K = 1,000 peces",
                     font=("Arial", 15, "normal"),
                     text_color=COLORS["text_main"],
                     anchor="w").pack(anchor="w", padx=22, pady=(0, 10))

        ctk.CTkLabel(ex,
                     text="Con solo 100 peces y recursos abundantes, la población crece rápidamente "
                          "al inicio.\nConforme se acerca a los 1,000 peces, el alimento y el espacio "
                          "escasean y el crecimiento se reduce.\nFinalmente la población se estabiliza "
                          "alrededor de K = 1,000 peces.\nLa gráfica tiene forma de S (curva sigmoidea), "
                          "característica de este modelo.",
                     font=("Arial", 14, "normal"),
                     text_color=COLORS["text_sub"],
                     justify="left", anchor="w",
                     wraplength=960).pack(anchor="w", padx=22, pady=(0, 20))

    # ── Tabla de variables ─────────────────────────────────────────────
    def _tabla_vars(self, parent):
        card = ctk.CTkFrame(parent, fg_color=COLORS["card"],
                             corner_radius=16,
                             border_width=1, border_color=COLORS["border"])
        card.pack(fill="x", pady=(0, 32))

        hdr_row = ctk.CTkFrame(card, fg_color=COLORS["surface"],
                                corner_radius=0)
        hdr_row.pack(fill="x")
        hdr_row.grid_columnconfigure((0,1,2,3), weight=1)
        for i, col in enumerate(["Símbolo","Nombre","Tipo","Descripción"]):
            ctk.CTkLabel(hdr_row, text=col,
                         font=("Arial", 13, "bold"),
                         text_color=COLORS["text_hint"],
                         anchor="w").grid(row=0, column=i,
                                          padx=22, pady=12, sticky="w")

        filas = [
            ("P(t)", "Población",           "Variable dependiente",
             "Número de individuos en el tiempo t"),
            ("t",    "Tiempo",              "Variable independiente",
             "Tiempo transcurrido desde el inicio"),
            ("P₀",   "Población inicial",   "Condición inicial",
             "Valor de P cuando t = 0"),
            ("r",    "Tasa de crecimiento", "Constante",
             "Crecimiento per cápita por unidad de tiempo"),
            ("K",    "Capacidad de carga",  "Parámetro (logístico)",
             "Máximo de individuos que soporta el ambiente"),
            ("dP/dt","Derivada de P",       "Tasa de cambio",
             "Velocidad con que cambia la población"),
            ("e",    "Número de Euler",     "Constante matemática",
             "≈ 2.71828, base del crecimiento continuo"),
        ]

        for idx, (sym, name, tipo, desc) in enumerate(filas):
            bg = COLORS["card"] if idx % 2 == 0 else COLORS["surface"]
            row = ctk.CTkFrame(card, fg_color=bg, corner_radius=0)
            row.pack(fill="x")
            row.grid_columnconfigure((0,1,2,3), weight=1)

            ctk.CTkLabel(row, text=sym,
                         font=("Arial", 16, "bold"),
                         text_color=COLORS["green"],
                         anchor="w").grid(row=0, column=0,
                                          padx=22, pady=10, sticky="w")
            ctk.CTkLabel(row, text=name,
                         font=("Arial", 14, "bold"),
                         text_color=COLORS["text_main"],
                         anchor="w").grid(row=0, column=1,
                                          padx=22, pady=10, sticky="w")
            ctk.CTkLabel(row, text=tipo,
                         font=("Arial", 13, "normal"),
                         text_color="#3B82F6",
                         anchor="w").grid(row=0, column=2,
                                          padx=22, pady=10, sticky="w")
            ctk.CTkLabel(row, text=desc,
                         font=("Arial", 13, "normal"),
                         text_color=COLORS["text_sub"],
                         anchor="w").grid(row=0, column=3,
                                          padx=22, pady=10, sticky="w")

    def _continue(self):
        if self.on_continue:
            self.on_continue()