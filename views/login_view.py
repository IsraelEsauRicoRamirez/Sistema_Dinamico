# views/login_view.py
import tkinter as tk
import customtkinter as ctk
from utils.theme import COLORS, FONTS, SIZES
from components.custom_entry import CustomEntry


def draw_logo(parent, size=42, bg="#FFFFFF"):
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


class LoginView(ctk.CTkFrame):
    """Login fullscreen. Lado izquierdo: liquid glass blanco con blobs verdes.
       Lado derecho: formulario blanco limpio."""

    def __init__(self, parent, on_go_register=None, on_login_success=None, **kwargs):
        super().__init__(parent, fg_color="#FFFFFF", corner_radius=0, **kwargs)
        self.on_go_register   = on_go_register
        self.on_login_success = on_login_success
        self._build()

    def _build(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=2)   # izquierda más ancha
        self.grid_columnconfigure(1, weight=3)   # derecha formulario

        self._build_left()
        self._build_right()

    # ── Panel izquierdo: liquid glass ────────────────────────────────────────
    def _build_left(self):
        left = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        left.grid(row=0, column=0, sticky="nsew")

        # Canvas de fondo con blobs
        canvas = tk.Canvas(left, highlightthickness=0, bd=0, bg="#FFFFFF")
        canvas.place(x=0, y=0, relwidth=1, relheight=1)

        def redraw(event=None):
            canvas.delete("all")
            w = canvas.winfo_width()  or 500
            h = canvas.winfo_height() or 700
            canvas.create_rectangle(0, 0, w, h, fill="#FFFFFF", outline="")
            # Blobs verdes suaves
            canvas.create_oval(-w*0.3, -h*0.2, w*0.9, h*0.6,
                               fill="#DCFCE7", outline="")
            canvas.create_oval(w*0.1, h*0.5, w*1.3, h*1.2,
                               fill="#BBF7D0", outline="")
            canvas.create_oval(w*0.3, h*0.15, w*1.1, h*0.85,
                               fill="#F0FDF4", outline="")
            # Highlight blanco glass
            canvas.create_oval(-w*0.1, -h*0.3, w*0.85, h*0.5,
                               fill="#FFFFFF", outline="", stipple="gray75")

        canvas.bind("<Configure>", redraw)
        canvas.after(50, redraw)

        # Contenido sobre el canvas
        content = ctk.CTkFrame(left, fg_color="transparent")
        content.place(relx=0.5, rely=0.5, anchor="center")

        # Logo + nombre
        brand = ctk.CTkFrame(content, fg_color="transparent")
        brand.pack(anchor="w")
        logo = draw_logo(brand, size=48, bg="#FFFFFF")
        # fondo transparente sobre el canvas
        logo.configure(bg="#FFFFFF")
        logo.pack(side="left", padx=(0, 12))
        ctk.CTkLabel(brand, text="SDCP",
                     font=("Arial", 26, "bold"),
                     text_color="#0F172A").pack(side="left")

        ctk.CTkLabel(content,
                     text="Simula.\nAnaliza.\nComprende.",
                     font=("Arial", 38, "bold"),
                     text_color="#0F172A",
                     justify="left").pack(anchor="w", pady=(44, 0))

        ctk.CTkLabel(content,
                     text="Sistemas Dinámicos de\nCrecimiento Poblacional",
                     font=("Arial", 14, "normal"),
                     text_color="#16A34A",
                     justify="left").pack(anchor="w", pady=(12, 0))

        # Dots
        dots = ctk.CTkFrame(content, fg_color="transparent")
        dots.pack(anchor="w", pady=(32, 0))
        for color, sz in [("#22C55E",12),("#86EFAC",8),("#BBFAD0",6)]:
            ctk.CTkFrame(dots, width=sz, height=sz,
                         fg_color=color, corner_radius=sz).pack(side="left", padx=3)

    # ── Panel derecho: formulario ─────────────────────────────────────────────
    def _build_right(self):
        right = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=0,
                              border_width=1, border_color=COLORS["border"])
        right.grid(row=0, column=1, sticky="nsew")
        right.grid_rowconfigure(0, weight=1)
        right.grid_columnconfigure(0, weight=1)

        inner = ctk.CTkFrame(right, fg_color="transparent")
        inner.grid(row=0, column=0)

        ctk.CTkLabel(inner, text="Bienvenido de vuelta",
                     font=FONTS["display"],
                     text_color=COLORS["text_main"],
                     anchor="w").pack(fill="x")

        ctk.CTkLabel(inner,
                     text="Ingresa tus credenciales para acceder.",
                     font=FONTS["subtitle"],
                     text_color=COLORS["text_sub"],
                     anchor="w").pack(fill="x", pady=(4, 22))

        # Social
        sf = ctk.CTkFrame(inner, fg_color="transparent")
        sf.pack(fill="x")
        sf.grid_columnconfigure((0,1), weight=1)

        ctk.CTkButton(sf, text="G   Google",
                      font=("Arial", 12, "bold"), height=42,
                      corner_radius=SIZES["corner_radius"],
                      fg_color="#FFFFFF", hover_color="#F8FAFC",
                      text_color=COLORS["text_main"],
                      border_width=1, border_color=COLORS["border_strong"],
                      ).grid(row=0, column=0, sticky="ew", padx=(0,5))

        ctk.CTkButton(sf, text="f   Facebook",
                      font=("Arial", 12, "bold"), height=42,
                      corner_radius=SIZES["corner_radius"],
                      fg_color="#1877F2", hover_color="#1667D9",
                      text_color="#FFFFFF",
                      ).grid(row=0, column=1, sticky="ew", padx=(5,0))

        # Divider
        dv = ctk.CTkFrame(inner, fg_color="transparent")
        dv.pack(fill="x", pady=14)
        dv.grid_columnconfigure((0,2), weight=1)
        ctk.CTkFrame(dv, height=1, fg_color=COLORS["border"]).grid(row=0,column=0,sticky="ew")
        ctk.CTkLabel(dv, text="  o con tu correo  ",
                     font=FONTS["caption"],
                     text_color=COLORS["text_hint"]).grid(row=0, column=1)
        ctk.CTkFrame(dv, height=1, fg_color=COLORS["border"]).grid(row=0,column=2,sticky="ew")

        self.email_entry = CustomEntry(inner, label="Correo electrónico",
                                       placeholder="usuario@ejemplo.com")
        self.email_entry.pack(fill="x", pady=(0,12))

        self.pass_entry = CustomEntry(inner, label="Contraseña",
                                      placeholder="••••••••", show="•")
        self.pass_entry.pack(fill="x", pady=(0,4))

        forgot = ctk.CTkLabel(inner, text="¿Olvidaste tu contraseña?",
                               font=FONTS["caption"],
                               text_color=COLORS["green_dark"],
                               anchor="e", cursor="hand2")
        forgot.pack(fill="x", pady=(0,20))
        forgot.bind("<Enter>", lambda _: forgot.configure(text_color=COLORS["green"]))
        forgot.bind("<Leave>", lambda _: forgot.configure(text_color=COLORS["green_dark"]))

        ctk.CTkButton(inner, text="Iniciar Sesión",
                      font=FONTS["button"],
                      height=SIZES["button_height"],
                      corner_radius=SIZES["corner_radius"],
                      fg_color=COLORS["green"],
                      hover_color=COLORS["green_hover"],
                      text_color="#FFFFFF",
                      command=self._handle_login).pack(fill="x")

        lf = ctk.CTkFrame(inner, fg_color="transparent")
        lf.pack(pady=(18, 0))
        ctk.CTkLabel(lf, text="¿No tienes cuenta?  ",
                     font=FONTS["link"],
                     text_color=COLORS["text_sub"]).pack(side="left")
        link = ctk.CTkLabel(lf, text="Regístrate gratis",
                            font=("Arial", 11, "bold"),
                            text_color=COLORS["green_dark"], cursor="hand2")
        link.pack(side="left")
        link.bind("<Button-1>", lambda _: self.on_go_register() if self.on_go_register else None)
        link.bind("<Enter>",    lambda _: link.configure(text_color=COLORS["green"]))
        link.bind("<Leave>",    lambda _: link.configure(text_color=COLORS["green_dark"]))

    def _handle_login(self):
        if self.on_login_success:
            self.on_login_success()