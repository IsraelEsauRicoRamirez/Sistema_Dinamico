import os
import sys
import customtkinter as ctk
from PIL import Image
from utils.theme import COLORS, FONTS, SIZES

def resolver_ruta_asset(ruta_relativa):
    if getattr(sys, 'frozen', False):
        ruta_base = sys._MEIPASS
    else:
        ruta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(ruta_base, ruta_relativa)

class IntroView(ctk.CTkFrame):
    def __init__(self, master, on_continue=None, **kwargs):
        super().__init__(master, fg_color=COLORS["bg"], corner_radius=0, **kwargs)
        self.on_continue = on_continue
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self._build()

    def _build(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent",
                                        scrollbar_button_color=COLORS["border"])
        scroll.grid(row=0, column=0, sticky="nsew")
        scroll.grid_columnconfigure(0, weight=1)

        row = 0

        header = ctk.CTkFrame(scroll, fg_color="transparent")
        header.grid(row=row, column=0, sticky="ew", padx=28, pady=(32, 8))
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(header, text="SDCP",
                     font=FONTS["display"],
                     text_color=COLORS["text_main"]).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(header,
                     text="Sistemas Dinámicos de Crecimiento Poblacional",
                     font=FONTS["subtitle"],
                     text_color=COLORS["text_sub"]).grid(row=1, column=0, sticky="w", pady=(2, 0))
        row += 1

        intro_card = ctk.CTkFrame(scroll, fg_color=COLORS["card"],
                                  corner_radius=18,
                                  border_width=1, border_color=COLORS["border"])
        intro_card.grid(row=row, column=0, sticky="ew", padx=28, pady=(14, 0))
        intro_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(intro_card, text="¿Qué es un sistema dinámico?",
                     font=FONTS["label"],
                     text_color=COLORS["text_sub"],
                     anchor="w").grid(row=0, column=0, sticky="w", padx=24, pady=(18, 8))

        ctk.CTkLabel(
            intro_card,
            text=("Es un modelo matemático que describe cómo cambia una población "
                  "con el tiempo. La app resuelve una ecuación diferencial que define "
                  "la tasa de crecimiento y calcula la población P para cada instante t."),
            font=FONTS["subtitle"],
            text_color=COLORS["text_main"],
            wraplength=760, justify="left", anchor="w",
        ).grid(row=1, column=0, sticky="w", padx=24, pady=(0, 20))
        row += 1

        ctk.CTkLabel(scroll, text="Modelos disponibles",
                     font=FONTS["label"],
                     text_color=COLORS["text_sub"],
                     anchor="w").grid(row=row, column=0, sticky="w",
                                      padx=28, pady=(22, 8))
        row += 1

        models_row = ctk.CTkFrame(scroll, fg_color="transparent")
        models_row.grid(row=row, column=0, sticky="ew", padx=28, pady=(0, 0))
        models_row.grid_columnconfigure((0, 1), weight=1)

        self._build_model_card(
            models_row, col=0,
            badge="Exponencial", badge_bg=COLORS["green_glow"], badge_fg=COLORS["green_dark"],
            titulo="Modelo de Malthus",
            para_que=("Sirve para crecimiento libre, sin límite de recursos: "
                      "bacterias en sus primeras horas, capital con interés compuesto, "
                      "poblaciones al inicio de su expansión."),
            image_filename="ecuacion_exponencial.png",
            solucion="P(t) = P₀ · e^(r·t)",
            variables=[("P₀", "Población inicial"), ("r", "Tasa de crecimiento"), ("t", "Tiempo")],
            como_funciona=("La app toma P₀ y r, y evalúa la fórmula para cada t. "
                           "Como no hay freno, la población crece cada vez más rápido."),
        )

        self._build_model_card(
            models_row, col=1,
            badge="Logístico", badge_bg="#EFF6FF", badge_fg="#3B82F6",
            titulo="Modelo de Verhulst",
            para_que=("Sirve cuando los recursos son limitados: la población crece rápido "
                      "al inicio, pero se frena al acercarse a una capacidad máxima K "
                      "(alimento, espacio, mercado)."),
            image_filename="ecuacion_logistica.png",
            solucion="P(t) = K / (1 + C · e^(−r·t))",
            variables=[("K", "Capacidad de carga (límite)"), ("C", "Constante = (K − P₀)/P₀")],
            como_funciona=("La app calcula C a partir de P₀ y K, luego evalúa la fórmula "
                           "en cada t. La curva se aplana al acercarse a K."),
        )
        row += 1

        comp_card = ctk.CTkFrame(scroll, fg_color=COLORS["card"],
                                 corner_radius=18,
                                 border_width=1, border_color=COLORS["border"])
        comp_card.grid(row=row, column=0, sticky="ew", padx=28, pady=(18, 0))
        comp_card.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(comp_card, text="¿Cuál elegir?",
                     font=FONTS["label"], text_color=COLORS["text_sub"],
                     anchor="w").grid(row=0, column=0, columnspan=2, sticky="w",
                                      padx=24, pady=(18, 10))

        tip = ctk.CTkFrame(comp_card, fg_color=COLORS["green_glow"], corner_radius=8)
        tip.grid(row=1, column=0, sticky="ew", padx=(24, 8), pady=(0, 18))
        ctk.CTkLabel(tip, text="Sin límite de recursos → Exponencial",
                     font=FONTS["caption"], text_color=COLORS["green_dark"],
                     wraplength=340, justify="left").pack(padx=14, pady=10, anchor="w")

        tip2 = ctk.CTkFrame(comp_card, fg_color="#EFF6FF", corner_radius=8)
        tip2.grid(row=1, column=1, sticky="ew", padx=(8, 24), pady=(0, 18))
        ctk.CTkLabel(tip2, text="Con capacidad máxima conocida (K) → Logístico",
                     font=FONTS["caption"], text_color="#3B82F6",
                     wraplength=340, justify="left").pack(padx=14, pady=10, anchor="w")
        row += 1

        ctk.CTkButton(scroll, text="Continuar al simulador",
                      font=FONTS["button"],
                      height=SIZES["button_height"],
                      corner_radius=SIZES["corner_radius"],
                      fg_color=COLORS["green"],
                      hover_color=COLORS["green_hover"],
                      text_color="#FFFFFF",
                      command=lambda: self.on_continue() if self.on_continue else None
                      ).grid(row=row, column=0, sticky="ew", padx=28, pady=(24, 32))

    def _build_model_card(self, parent, col, badge, badge_bg, badge_fg, titulo,
                          para_que, image_filename, solucion, variables, como_funciona):
        pad = (0, 10) if col == 0 else (10, 0)
        card = ctk.CTkFrame(parent, fg_color=COLORS["card"],
                            corner_radius=18,
                            border_width=1, border_color=COLORS["border"])
        card.grid(row=0, column=col, sticky="new", padx=pad, pady=(0, 0))
        card.grid_columnconfigure(0, weight=1)

        hdr = ctk.CTkFrame(card, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="w", padx=22, pady=(18, 4))
        ctk.CTkLabel(hdr, text=f"  {badge}  ",
                     font=("Arial", 10, "bold"),
                     text_color=badge_fg, fg_color=badge_bg,
                     corner_radius=8).pack(side="left")

        ctk.CTkLabel(card, text=titulo,
                     font=("Arial", 17, "bold"),
                     text_color=COLORS["text_main"],
                     anchor="w").grid(row=1, column=0, sticky="w", padx=22, pady=(4, 8))

        ctk.CTkLabel(card, text=para_que,
                     font=FONTS["caption"],
                     text_color=COLORS["text_sub"],
                     wraplength=330, justify="left", anchor="w"
                     ).grid(row=2, column=0, sticky="w", padx=22, pady=(0, 14))

        eq_frame = ctk.CTkFrame(card, fg_color=COLORS["surface"], corner_radius=12)
        eq_frame.grid(row=3, column=0, sticky="ew", padx=22, pady=(0, 12))
        eq_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(eq_frame, text="Ecuación diferencial",
                     font=FONTS["small"], text_color=COLORS["text_hint"],
                     anchor="w").grid(row=0, column=0, sticky="w", padx=14, pady=(10, 0))

        try:
            ruta_relativa = os.path.join("assets", image_filename)
            image_path = resolver_ruta_asset(ruta_relativa)
            
            pil_img = Image.open(image_path)
            base_height = 35
            w_percent = (base_height / float(pil_img.size[1]))
            h_size = int((float(pil_img.size[0]) * float(w_percent)))
            
            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(h_size, base_height))
            
            ctk.CTkLabel(eq_frame, text="", image=ctk_img).grid(row=1, column=0, sticky="w", padx=14, pady=(5, 10))
        except Exception as e:
            ctk.CTkLabel(eq_frame, text=f"[Falta imagen: {image_filename}]",
                         font=("Arial", 12, "italic"), text_color=COLORS["text_main"],
                         anchor="w").grid(row=1, column=0, sticky="w", padx=14, pady=(0, 10))

        ctk.CTkFrame(eq_frame, height=1, fg_color=COLORS["border"]).grid(
            row=2, column=0, sticky="ew", padx=14)

        ctk.CTkLabel(eq_frame, text="Solución (lo que grafica la app)",
                     font=FONTS["small"], text_color=COLORS["text_hint"],
                     anchor="w").grid(row=3, column=0, sticky="w", padx=14, pady=(10, 0))
        ctk.CTkLabel(eq_frame, text=solucion,
                     font=("Arial", 14, "bold"), text_color=COLORS["green_dark"],
                     anchor="w").grid(row=4, column=0, sticky="w", padx=14, pady=(0, 12))

        var_text = "  ·  ".join(f"{k} = {v}" for k, v in variables)
        ctk.CTkLabel(card, text=var_text,
                     font=FONTS["small"], text_color=COLORS["text_hint"],
                     wraplength=330, justify="left", anchor="w"
                     ).grid(row=4, column=0, sticky="w", padx=22, pady=(0, 10))

        how = ctk.CTkFrame(card, fg_color="transparent")
        how.grid(row=5, column=0, sticky="ew", padx=22, pady=(0, 20))
        ctk.CTkLabel(how, text=como_funciona,
                     font=("Arial", 11, "italic"),
                     text_color=COLORS["text_sub"],
                     wraplength=330, justify="left", anchor="w").pack(anchor="w")