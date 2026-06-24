# views/register_view.py
import tkinter as tk
import customtkinter as ctk
from utils.theme import COLORS, FONTS, SIZES
from components.custom_entry import CustomEntry


def draw_logo(parent, size=44, bg="#FFFFFF"):
    scale = size / 100
    c = tk.Canvas(parent, width=size, height=size, highlightthickness=0, bg=bg)
    c.create_rectangle(0, 0, size, size, fill="#F4F4F5", outline="")
    def sc(v): return int(v * scale)
    c.create_line(sc(25),sc(75),sc(50),sc(45),sc(75),sc(45),
                  fill="#22c55e",width=max(2,int(5*scale)),capstyle="round",joinstyle="round")
    c.create_line(sc(25),sc(75),sc(60),sc(75),sc(75),sc(45),
                  fill="#d4d4d8",width=max(1,int(4*scale)),capstyle="round",joinstyle="round")
    c.create_line(sc(50),sc(45),sc(60),sc(75),fill="#e4e4e7",width=max(1,int(2*scale)))
    def oval(cx,cy,r,fill):
        cx,cy,r=sc(cx),sc(cy),max(2,int(r*scale))
        c.create_oval(cx-r,cy-r,cx+r,cy+r,fill=fill,outline="")
    oval(25,75,7,"#18181b"); oval(50,45,6,"#71717a"); oval(60,75,5,"#a1a1aa")
    oval(75,45,9,"#22c55e"); oval(75,45,3,"#ffffff")
    return c


class RegisterView(ctk.CTkFrame):
    """Registro fullscreen. Izquierda: liquid glass blanco+verde. Derecha: formulario."""

    def __init__(self, parent, on_go_login=None, **kwargs):
        super().__init__(parent, fg_color="#FFFFFF", corner_radius=0, **kwargs)
        self.on_go_login = on_go_login
        self._build()

    def _build(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=3)
        self._build_left()
        self._build_right()

    # ── Panel izquierdo ───────────────────────────────────────────────────────
    def _build_left(self):
        left = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        left.grid(row=0, column=0, sticky="nsew")

        canvas = tk.Canvas(left, highlightthickness=0, bd=0, bg="#FFFFFF")
        canvas.place(x=0, y=0, relwidth=1, relheight=1)

        def redraw(event=None):
            canvas.delete("all")
            w = canvas.winfo_width()  or 500
            h = canvas.winfo_height() or 800
            canvas.create_rectangle(0, 0, w, h, fill="#FFFFFF", outline="")
            canvas.create_oval(-w*0.3, -h*0.1, w*0.9, h*0.55, fill="#DCFCE7", outline="")
            canvas.create_oval(w*0.1, h*0.55, w*1.3, h*1.2, fill="#BBF7D0", outline="")
            canvas.create_oval(w*0.3, h*0.20, w*1.1, h*0.90, fill="#F0FDF4", outline="")
            canvas.create_oval(-w*0.1, -h*0.3, w*0.85, h*0.5,
                               fill="#FFFFFF", outline="", stipple="gray75")

        canvas.bind("<Configure>", redraw)
        canvas.after(50, redraw)

        content = ctk.CTkFrame(left, fg_color="transparent")
        content.place(relx=0.5, rely=0.5, anchor="center")

        brand = ctk.CTkFrame(content, fg_color="transparent")
        brand.pack(anchor="w")
        logo = draw_logo(brand, size=46, bg="#FFFFFF")
        logo.pack(side="left", padx=(0, 12))
        ctk.CTkLabel(brand, text="SDCP",
                     font=("Arial", 24, "bold"),
                     text_color="#0F172A").pack(side="left")

        ctk.CTkLabel(content,
                     text="Únete y\nexplora la\nciencia.",
                     font=("Arial", 36, "bold"),
                     text_color="#0F172A",
                     justify="left").pack(anchor="w", pady=(44, 0))

        ctk.CTkLabel(content,
                     text="Modela poblaciones,\nentiende el futuro.",
                     font=("Arial", 13, "normal"),
                     text_color="#16A34A",
                     justify="left").pack(anchor="w", pady=(12, 0))

        # Pasos
        steps_frame = ctk.CTkFrame(content, fg_color="transparent")
        steps_frame.pack(anchor="w", pady=(32, 0))
        for i, step in enumerate(["Crea tu cuenta","Elige tu modelo","Ejecuta simulaciones"]):
            rf = ctk.CTkFrame(steps_frame, fg_color="transparent")
            rf.pack(anchor="w", pady=5)
            num_badge = ctk.CTkLabel(rf,
                                      text=f"0{i+1}",
                                      font=("Arial", 9, "bold"),
                                      text_color=COLORS["green_dark"],
                                      fg_color=COLORS["green_glow"],
                                      width=26, height=26,
                                      corner_radius=13)
            num_badge.pack(side="left")
            ctk.CTkLabel(rf, text=f"  {step}",
                         font=("Arial", 11, "normal"),
                         text_color=COLORS["text_sub"]).pack(side="left")

    # ── Panel derecho: formulario ─────────────────────────────────────────────
    def _build_right(self):
        right = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=0,
                              border_width=1, border_color=COLORS["border"])
        right.grid(row=0, column=1, sticky="nsew")
        right.grid_rowconfigure(0, weight=1)
        right.grid_columnconfigure(0, weight=1)

        scroll = ctk.CTkScrollableFrame(right, fg_color="transparent",
                                         scrollbar_button_color=COLORS["border"])
        scroll.grid(row=0, column=0, sticky="nsew")
        scroll.grid_columnconfigure(0, weight=1)

        inner = ctk.CTkFrame(scroll, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=56, pady=48)

        ctk.CTkLabel(inner, text="Crear cuenta",
                     font=FONTS["display"],
                     text_color=COLORS["text_main"],
                     anchor="w").pack(fill="x")
        ctk.CTkLabel(inner,
                     text="Completa los datos para empezar a simular.",
                     font=FONTS["subtitle"],
                     text_color=COLORS["text_sub"],
                     anchor="w").pack(fill="x", pady=(4, 24))

        # Social
        sf = ctk.CTkFrame(inner, fg_color="transparent")
        sf.pack(fill="x")
        sf.grid_columnconfigure((0,1), weight=1)
        ctk.CTkButton(sf, text="G   Registrarse con Google",
                      font=("Arial", 12, "bold"), height=44,
                      corner_radius=SIZES["corner_radius"],
                      fg_color="#FFFFFF", hover_color="#F8FAFC",
                      text_color=COLORS["text_main"],
                      border_width=1, border_color=COLORS["border_strong"],
                      ).grid(row=0, column=0, sticky="ew", padx=(0,6))
        ctk.CTkButton(sf, text="f   Registrarse con Facebook",
                      font=("Arial", 12, "bold"), height=44,
                      corner_radius=SIZES["corner_radius"],
                      fg_color="#1877F2", hover_color="#1667D9",
                      text_color="#FFFFFF",
                      ).grid(row=0, column=1, sticky="ew", padx=(6,0))

        # Divider
        dv = ctk.CTkFrame(inner, fg_color="transparent")
        dv.pack(fill="x", pady=18)
        dv.grid_columnconfigure((0,2), weight=1)
        ctk.CTkFrame(dv, height=1, fg_color=COLORS["border"]).grid(row=0,column=0,sticky="ew")
        ctk.CTkLabel(dv, text="  o con tu correo  ",
                     font=FONTS["caption"],
                     text_color=COLORS["text_hint"]).grid(row=0, column=1)
        ctk.CTkFrame(dv, height=1, fg_color=COLORS["border"]).grid(row=0,column=2,sticky="ew")

        # Nombre + Matrícula en la misma fila
        row1 = ctk.CTkFrame(inner, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 14))
        row1.grid_columnconfigure((0,1), weight=1)
        self.name_entry = CustomEntry(row1, label="Nombre completo",
                                      placeholder="Juan Pérez")
        self.name_entry.grid(row=0, column=0, sticky="ew", padx=(0,8))
        self.id_entry = CustomEntry(row1, label="Matrícula / ID",
                                    placeholder="A01234567")
        self.id_entry.grid(row=0, column=1, sticky="ew", padx=(8,0))

        self.email_entry = CustomEntry(inner, label="Correo electrónico",
                                       placeholder="usuario@ejemplo.com")
        self.email_entry.pack(fill="x", pady=(0,14))

        self.pass_entry = CustomEntry(inner, label="Contraseña",
                                      placeholder="Mínimo 8 caracteres", show="•")
        self.pass_entry.pack(fill="x", pady=(0,20))

        # Tipo de cuenta
        ctk.CTkLabel(inner, text="Tipo de cuenta",
                     font=FONTS["label"],
                     text_color=COLORS["text_main"],
                     anchor="w").pack(fill="x", pady=(0,8))

        self.rol_var = ctk.StringVar(value="Alumno")
        roles = ctk.CTkFrame(inner, fg_color="transparent")
        roles.pack(fill="x", pady=(0,24))
        roles.grid_columnconfigure((0,1), weight=1)

        for i, rol in enumerate(["Alumno", "Profesor"]):
            active = (i == 0)
            b = ctk.CTkButton(roles, text=rol,
                              font=("Arial", 13, "bold") if active else FONTS["label"],
                              height=44, corner_radius=12,
                              fg_color=COLORS["green"] if active else COLORS["input_bg"],
                              hover_color=COLORS["green_dark"] if active else COLORS["border"],
                              text_color="#FFFFFF" if active else COLORS["text_sub"],
                              border_width=1,
                              border_color=COLORS["green"] if active else COLORS["border"],
                              command=lambda r=rol: self._select_rol(r))
            b.grid(row=0, column=i, sticky="ew",
                   padx=(0,7) if i==0 else (7,0))
            setattr(self, f"_btn_{rol.lower()}", b)

        ctk.CTkButton(inner, text="Crear cuenta",
                      font=FONTS["button"],
                      height=SIZES["button_height"],
                      corner_radius=SIZES["corner_radius"],
                      fg_color=COLORS["green"],
                      hover_color=COLORS["green_hover"],
                      text_color="#FFFFFF").pack(fill="x")

        ctk.CTkLabel(inner,
                     text="Al registrarte aceptas los Términos de uso y la Política de privacidad.",
                     font=("Arial", 9, "normal"),
                     text_color=COLORS["text_hint"],
                     wraplength=460, justify="center").pack(pady=(10, 0))

        lf = ctk.CTkFrame(inner, fg_color="transparent")
        lf.pack(pady=(14, 0))
        ctk.CTkLabel(lf, text="¿Ya tienes una cuenta?  ",
                     font=FONTS["link"],
                     text_color=COLORS["text_sub"]).pack(side="left")
        link = ctk.CTkLabel(lf, text="Inicia sesión",
                            font=("Arial", 11, "bold"),
                            text_color=COLORS["green_dark"], cursor="hand2")
        link.pack(side="left")
        link.bind("<Button-1>", lambda _: self.on_go_login() if self.on_go_login else None)
        link.bind("<Enter>",    lambda _: link.configure(text_color=COLORS["green"]))
        link.bind("<Leave>",    lambda _: link.configure(text_color=COLORS["green_dark"]))

    def _select_rol(self, rol):
        self.rol_var.set(rol)
        for r in ["Alumno", "Profesor"]:
            b = getattr(self, f"_btn_{r.lower()}")
            active = (r == rol)
            b.configure(
                fg_color=COLORS["green"] if active else COLORS["input_bg"],
                text_color="#FFFFFF" if active else COLORS["text_sub"],
                border_color=COLORS["green"] if active else COLORS["border"],
                hover_color=COLORS["green_dark"] if active else COLORS["border"],
                font=("Arial", 13, "bold") if active else FONTS["label"],
            )