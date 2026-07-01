import tkinter as tk
import customtkinter as ctk
from utils.theme import COLORS, FONTS, SIZES


def _draw_logo(parent, size=56, bg="#FFFFFF"):
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
        super().__init__(parent, fg_color="#FFFFFF", corner_radius=0, **kwargs)
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
            canvas.create_oval(-w*0.2, -h*0.2, w*0.7, h*0.7,
                               fill="#DCFCE7", outline="")
            canvas.create_oval(w*0.4, h*0.5, w*1.2, h*1.3,
                               fill="#BBF7D0", outline="")
            canvas.create_oval(w*0.1, h*0.15, w*0.9, h*0.95,
                               fill="#ECFDF5", outline="")
            canvas.create_oval(-w*0.05, -h*0.3, w*0.9, h*0.45,
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

        brand = ctk.CTkFrame(content, fg_color="transparent")
        brand.pack(anchor="center", pady=(0, 0))
        logo = _draw_logo(brand, size=64, bg="#ECFDF5")
        logo.configure(bg="#FFFFFF")
        logo.pack(side="left", padx=(0, 16))
        ctk.CTkLabel(brand, text="SDCP",
                     font=("Arial", 36, "bold"),
                     text_color=COLORS["text_main"]).pack(side="left")

        ctk.CTkLabel(content,
                     text="Sistemas Dinámicos de Crecimiento Poblacional",
                     font=("Arial", 16, "normal"),
                     text_color=COLORS["text_sub"]).pack(anchor="center", pady=(6, 40))

        cards_frame = ctk.CTkFrame(content, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 40))
        cards_frame.grid_columnconfigure((0,1,2), weight=1)

        cards = [
            ("🌱", "¿Qué es?",
             "Una plataforma para modelar y visualizar cómo crece o decrece una población "
             "a lo largo del tiempo usando ecuaciones diferenciales ordinarias (EDOs)."),
            ("📐", "¿Qué modelos incluye?",
             "Modelo Exponencial: crecimiento ilimitado.\n"
             "Modelo Logístico: crecimiento con límite ambiental (capacidad de carga K)."),
            ("🎯", "¿Para qué sirve?",
             "Analizar escenarios de crecimiento poblacional, estimar parámetros a partir "
             "de datos reales y exportar resultados para reportes académicos."),
        ]
        for i, (icon, title, desc) in enumerate(cards):
            card = ctk.CTkFrame(cards_frame, fg_color=COLORS["card"],
                                corner_radius=18,
                                border_width=1, border_color=COLORS["border"])
            card.grid(row=0, column=i, sticky="nsew",
                      padx=(0,12) if i<2 else 0)
            card.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(card, text=icon,
                         font=("Arial", 32)).grid(
                row=0, column=0, pady=(22, 8))
            ctk.CTkLabel(card, text=title,
                         font=("Arial", 14, "bold"),
                         text_color=COLORS["text_main"]).grid(
                row=1, column=0, pady=(0, 8))
            ctk.CTkLabel(card, text=desc,
                         font=FONTS["caption"],
                         text_color=COLORS["text_sub"],
                         wraplength=260, justify="center").grid(
                row=2, column=0, padx=20, pady=(0, 22))

        sec_label = ctk.CTkLabel(content,
                                  text="Cómo funciona",
                                  font=("Arial", 18, "bold"),
                                  text_color=COLORS["text_main"])
        sec_label.pack(anchor="w", pady=(0, 16))

        steps = [
            ("01", "Inicia sesión o crea una cuenta",
             "Accede con tu correo institucional o redes sociales."),
            ("02", "Selecciona el modelo matemático",
             "Elige entre Modelo Exponencial o Logístico según tu problema."),
            ("03", "Ingresa los parámetros",
             "Define P₀, r, K (si aplica), el intervalo de tiempo y su unidad."),
            ("04", "Calcula r (opcional)",
             "Usa la calculadora integrada si tienes datos reales de población."),
            ("05", "Ejecuta la simulación",
             "Obtén la gráfica dinámica y la tabla de datos con un clic."),
            ("06", "Exporta los resultados",
             "Descarga los datos en formato CSV para tu reporte."),
        ]

        steps_frame = ctk.CTkFrame(content, fg_color="transparent")
        steps_frame.pack(fill="x", pady=(0, 40))
        steps_frame.grid_columnconfigure((0,1), weight=1)

        for i, (num, title, desc) in enumerate(steps):
            row, col = divmod(i, 2)
            step_card = ctk.CTkFrame(steps_frame, fg_color=COLORS["card"],
                                      corner_radius=14,
                                      border_width=1, border_color=COLORS["border"])
            step_card.grid(row=row, column=col, sticky="ew",
                           padx=(0,10) if col==0 else (10,0),
                           pady=(0,10))
            step_card.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(step_card, text=num,
                         font=("Arial", 13, "bold"),
                         text_color=COLORS["green_dark"],
                         fg_color=COLORS["green_glow"],
                         width=40, height=40,
                         corner_radius=20).grid(
                row=0, column=0, rowspan=2, padx=(16,12), pady=16)

            ctk.CTkLabel(step_card, text=title,
                         font=("Arial", 13, "bold"),
                         text_color=COLORS["text_main"],
                         anchor="w").grid(row=0, column=1, sticky="w", pady=(16,2))
            ctk.CTkLabel(step_card, text=desc,
                         font=FONTS["caption"],
                         text_color=COLORS["text_sub"],
                         anchor="w", wraplength=340,
                         justify="left").grid(row=1, column=1,
                                              sticky="w", pady=(0,16))

        models_label = ctk.CTkLabel(content,
                                     text="Los modelos matemáticos",
                                     font=("Arial", 18, "bold"),
                                     text_color=COLORS["text_main"])
        models_label.pack(anchor="w", pady=(0, 16))

        models_frame = ctk.CTkFrame(content, fg_color="transparent")
        models_frame.pack(fill="x", pady=(0, 40))
        models_frame.grid_columnconfigure((0,1), weight=1)

        model_data = [
            ("Modelo Exponencial",
             "dP/dt = r · P\nP(t) = P₀ · e^(r·t)",
             "Asume que la tasa de crecimiento es constante y proporcional "
             "al tamaño de la población. No tiene límite superior.\n\n"
             "Útil para: bacterias en fase logarítmica, poblaciones con "
             "recursos ilimitados, crecimiento económico inicial.",
             "#DCFCE7", COLORS["green"]),
            ("Modelo Logístico",
             "dP/dt = r · P · (1 - P/K)\nP(t) = K / (1 + A·e^(-r·t))",
             "Incorpora la capacidad de carga K: a medida que la población "
             "se acerca a K, el crecimiento se frena hasta detenerse.\n\n"
             "Útil para: poblaciones animales con recursos limitados, "
             "crecimiento de tumores, adopción de tecnologías.",
             "#EFF6FF", "#3B82F6"),
        ]

        for i, (title, formula, desc, bg_col, accent) in enumerate(model_data):
            mc = ctk.CTkFrame(models_frame, fg_color=bg_col,
                               corner_radius=16,
                               border_width=1, border_color=accent)
            mc.grid(row=0, column=i, sticky="nsew",
                    padx=(0,10) if i==0 else (10,0))
            mc.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(mc, text=title,
                         font=("Arial", 14, "bold"),
                         text_color=accent).grid(
                row=0, column=0, sticky="w", padx=20, pady=(18,8))

            fbox = ctk.CTkFrame(mc, fg_color="#FFFFFF",
                                 corner_radius=10,
                                 border_width=1, border_color=accent)
            fbox.grid(row=1, column=0, sticky="ew", padx=20, pady=(0,10))
            ctk.CTkLabel(fbox, text=formula,
                         font=("Arial", 13, "italic"),
                         text_color=COLORS["text_main"],
                         justify="center").pack(padx=16, pady=10)

            ctk.CTkLabel(mc, text=desc,
                         font=FONTS["caption"],
                         text_color=COLORS["text_sub"],
                         wraplength=320, justify="left",
                         anchor="w").grid(row=2, column=0,
                                          sticky="w", padx=20, pady=(0,20))

        ctk.CTkButton(content,
                      text="Ir al Simulador  →",
                      font=("Arial", 16, "bold"),
                      height=54, corner_radius=14,
                      fg_color=COLORS["green"],
                      hover_color=COLORS["green_hover"],
                      text_color="#FFFFFF",
                      command=self._continue).pack(
            fill="x", pady=(0, 10))

        ctk.CTkLabel(content,
                     text="Ya puedes cerrar esta introducción en cualquier momento desde el menú lateral.",
                     font=FONTS["caption"],
                     text_color=COLORS["text_hint"],
                     justify="center").pack(pady=(0, 40))

    def _continue(self):
        if self.on_continue:
            self.on_continue()