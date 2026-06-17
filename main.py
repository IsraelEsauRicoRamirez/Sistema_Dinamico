# main.py
import customtkinter as ctk
from views.login_view import LoginView
from views.register_view import RegisterView
from views.dashboard_view import DashboardView
from utils.theme import COLORS

# ── Apariencia global ──────────────────────────────────────────────────────────
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DynaPop Sim")
        self.geometry("1200x760")
        self.minsize(900, 600)
        self.configure(fg_color=COLORS["bg"])

        # Todas las vistas ocupan la misma celda (se apilan)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ── Crear vistas ───────────────────────────────────
        self.login_view = LoginView(
            self,
            on_go_register=self.show_register,
            on_login_success=self.show_dashboard,   # ← nuevo callback
        )
        self.login_view.grid(row=0, column=0, sticky="nsew")

        self.register_view = RegisterView(
            self,
            on_go_login=self.show_login,
        )
        self.register_view.grid(row=0, column=0, sticky="nsew")

        # El dashboard se crea una sola vez
        self.dashboard_view = DashboardView(
            self,
            user_data={"nombre": "Juan Pérez", "rol": "Estudiante"},
        )
        self.dashboard_view.grid(row=0, column=0, sticky="nsew")

        # ── Empezar en Login ───────────────────────────────
        self.show_login()

    # ── Navegación ─────────────────────────────────────────────────────────────
    def show_login(self):
        self.geometry("900x680")
        self.login_view.tkraise()

    def show_register(self):
        self.geometry("900x760")
        self.register_view.tkraise()

    def show_dashboard(self, user_data=None):
        """Navega al dashboard. Puede recibir datos del usuario logueado."""
        self.geometry("1280x800")
        if user_data:
            # Reconstruir dashboard con datos reales cuando conectes el backend
            pass
        self.dashboard_view.tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()