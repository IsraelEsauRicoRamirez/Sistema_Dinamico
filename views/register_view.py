# views/register_view.py
import customtkinter as ctk
from utils.theme import COLORS, FONTS, SIZES
from components.custom_entry import CustomEntry


class RegisterView(ctk.CTkFrame):
    """
    Pantalla de registro de cuenta.
    Llama a `on_go_login` cuando el usuario pulsa el enlace de inicio de sesión.
    """

    def __init__(self, parent, on_go_login, **kwargs):
        super().__init__(parent, fg_color=COLORS["bg"], **kwargs)
        self.on_go_login = on_go_login
        self._build()

    def _build(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ── Card ──────────────────────────────────────────
        card = ctk.CTkFrame(
            self,
            width=SIZES["card_width"],
            fg_color=COLORS["card"],
            corner_radius=20,
        )
        card.grid(row=0, column=0)
        card.grid_propagate(False)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(
            padx=SIZES["card_pad_x"],
            pady=SIZES["card_pad_y"],
            fill="both",
            expand=True,
        )

        # ── Logo + Nombre ──────────────────────────────────
        brand_frame = ctk.CTkFrame(inner, fg_color="transparent")
        brand_frame.pack(pady=(0, 24))

        ctk.CTkLabel(
            brand_frame,
            text="⬡",
            font=("Arial", 28),
            text_color=COLORS["green"],
        ).pack(side="left", padx=(0, 8))

        ctk.CTkLabel(
            brand_frame,
            text="DynaPop Sim",
            font=FONTS["brand"],
            text_color=COLORS["text_main"],
        ).pack(side="left")

        # ── Títulos ────────────────────────────────────────
        ctk.CTkLabel(
            inner,
            text="Crear cuenta",
            font=FONTS["title"],
            text_color=COLORS["text_main"],
            anchor="w",
        ).pack(fill="x")

        ctk.CTkLabel(
            inner,
            text="Completa los datos para unirte a la plataforma.",
            font=FONTS["subtitle"],
            text_color=COLORS["text_sub"],
            anchor="w",
        ).pack(fill="x", pady=(4, 20))

        # ── Campos ────────────────────────────────────────
        self.name_entry = CustomEntry(
            inner, label="Nombre completo", placeholder="Juan Pérez"
        )
        self.name_entry.pack(fill="x", pady=(0, 12))

        self.id_entry = CustomEntry(
            inner, label="Matrícula / ID", placeholder="A01234567"
        )
        self.id_entry.pack(fill="x", pady=(0, 12))

        self.email_entry = CustomEntry(
            inner, label="Correo electrónico", placeholder="usuario@ejemplo.com"
        )
        self.email_entry.pack(fill="x", pady=(0, 12))

        self.pass_entry = CustomEntry(
            inner, label="Contraseña", placeholder="Mínimo 8 caracteres", show="•"
        )
        self.pass_entry.pack(fill="x", pady=(0, 12))

        # Rol (OptionMenu en lugar de select)
        ctk.CTkLabel(
            inner,
            text="Rol",
            font=FONTS["label"],
            text_color=COLORS["text_main"],
            anchor="w",
        ).pack(fill="x", pady=(0, 5))

        self.rol_var = ctk.StringVar(value="Estudiante")
        ctk.CTkOptionMenu(
            inner,
            values=["Estudiante", "Profesor", "Administrador"],
            variable=self.rol_var,
            font=FONTS["input"],
            height=SIZES["input_height"],
            corner_radius=SIZES["corner_radius"],
            fg_color=COLORS["input_bg"],
            button_color=COLORS["green"],
            button_hover_color=COLORS["green_hover"],
            dropdown_fg_color=COLORS["card"],
            text_color=COLORS["text_main"],
        ).pack(fill="x", pady=(0, 20))

        # ── Botón ─────────────────────────────────────────
        btn = ctk.CTkButton(
            inner,
            text="Crear Cuenta",
            font=FONTS["button"],
            height=SIZES["button_height"],
            corner_radius=SIZES["corner_radius"],
            fg_color=COLORS["green"],
            hover_color=COLORS["green_hover"],
            text_color="#FFFFFF",
        )
        btn.pack(fill="x")

        # ── Link a Login ───────────────────────────────────
        link_frame = ctk.CTkFrame(inner, fg_color="transparent")
        link_frame.pack(pady=(16, 0))

        ctk.CTkLabel(
            link_frame,
            text="¿Ya tienes cuenta? ",
            font=FONTS["link"],
            text_color=COLORS["text_sub"],
        ).pack(side="left")

        link = ctk.CTkLabel(
            link_frame,
            text="Inicia sesión",
            font=(FONTS["link"][0], FONTS["link"][1], "bold"),
            text_color=COLORS["green_dark"],
            cursor="hand2",
        )
        link.pack(side="left")
        link.bind("<Button-1>", lambda _e: self.on_go_login())
        link.bind("<Enter>",    lambda _e: link.configure(text_color=COLORS["green"]))
        link.bind("<Leave>",    lambda _e: link.configure(text_color=COLORS["green_dark"]))