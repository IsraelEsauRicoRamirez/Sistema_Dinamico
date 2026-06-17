# views/login_view.py
import customtkinter as ctk
from utils.theme import COLORS, FONTS, SIZES
from components.custom_entry import CustomEntry


class LoginView(ctk.CTkFrame):
    """
    Pantalla de inicio de sesión.
    on_go_register  → navega al registro
    on_login_success → navega al dashboard (se llama al pulsar Iniciar Sesión)
    """

    def __init__(self, parent, on_go_register=None, on_login_success=None, **kwargs):
        super().__init__(parent, fg_color=COLORS["bg"], **kwargs)
        self.on_go_register   = on_go_register
        self.on_login_success = on_login_success
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
        brand_frame.pack(pady=(0, 28))

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
            text="Bienvenido de vuelta",
            font=FONTS["title"],
            text_color=COLORS["text_main"],
            anchor="w",
        ).pack(fill="x")

        ctk.CTkLabel(
            inner,
            text="Ingresa tus credenciales para continuar.",
            font=FONTS["subtitle"],
            text_color=COLORS["text_sub"],
            anchor="w",
        ).pack(fill="x", pady=(4, 24))

        # ── Campos ────────────────────────────────────────
        self.email_entry = CustomEntry(
            inner,
            label="Correo electrónico",
            placeholder="usuario@ejemplo.com",
        )
        self.email_entry.pack(fill="x", pady=(0, 14))

        self.pass_entry = CustomEntry(
            inner,
            label="Contraseña",
            placeholder="••••••••",
            show="•",
        )
        self.pass_entry.pack(fill="x", pady=(0, 22))

        # ── Botón ─────────────────────────────────────────
        ctk.CTkButton(
            inner,
            text="Iniciar Sesión",
            font=FONTS["button"],
            height=SIZES["button_height"],
            corner_radius=SIZES["corner_radius"],
            fg_color=COLORS["green"],
            hover_color=COLORS["green_hover"],
            text_color="#FFFFFF",
            command=self._handle_login,
        ).pack(fill="x")

        # ── Link a Registro ────────────────────────────────
        link_frame = ctk.CTkFrame(inner, fg_color="transparent")
        link_frame.pack(pady=(18, 0))

        ctk.CTkLabel(
            link_frame,
            text="¿No tienes cuenta? ",
            font=FONTS["link"],
            text_color=COLORS["text_sub"],
        ).pack(side="left")

        link = ctk.CTkLabel(
            link_frame,
            text="Regístrate aquí",
            font=(FONTS["link"][0], FONTS["link"][1], "bold"),
            text_color=COLORS["green_dark"],
            cursor="hand2",
        )
        link.pack(side="left")
        link.bind("<Button-1>", lambda _e: self.on_go_register() if self.on_go_register else None)
        link.bind("<Enter>",    lambda _e: link.configure(text_color=COLORS["green"]))
        link.bind("<Leave>",    lambda _e: link.configure(text_color=COLORS["green_dark"]))

    def _handle_login(self):
        """
        Por ahora navega directo al dashboard sin validar.
        Cuando conectes el backend, aquí harás la llamada a la API/DB.
        """
        if self.on_login_success:
            self.on_login_success()