import customtkinter as ctk
from views.login_view import LoginView
from views.register_view import RegisterView
from views.intro_view import IntroView
from views.dashboard_view import DashboardView
from utils.theme import COLORS

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SDCP — Sistemas Dinámicos de Crecimiento Poblacional")
        self.geometry("1100x720")
        self.minsize(900, 620)
        self.configure(fg_color=COLORS["bg"])

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.login_view = LoginView(
            self,
            on_go_register=self.show_register,
            on_login_success=self.show_intro,
        )
        self.login_view.grid(row=0, column=0, sticky="nsew")

        self.register_view = RegisterView(
            self,
            on_go_login=self.show_login,
        )
        self.register_view.grid(row=0, column=0, sticky="nsew")

        self.intro_view = IntroView(
            self,
            on_continue=self.show_dashboard,
        )
        self.intro_view.grid(row=0, column=0, sticky="nsew")

        self.dashboard_view = DashboardView(
            self,
            user_data={
                "nombre":    "Juan Pérez",
                "rol":       "Alumno",
                "matricula": "A01234567",
                "correo":    "juan@ejemplo.com",
            },
            on_show_intro=self.show_intro,
        )
        self.dashboard_view.grid(row=0, column=0, sticky="nsew")

        self.show_login()

    def show_login(self):
        self.geometry("1100x720")
        self.login_view.tkraise()

    def show_register(self):
        self.geometry("1100x800")
        self.register_view.tkraise()

    def show_intro(self):
        self.geometry("1280x820")
        self.intro_view.tkraise()

    def show_dashboard(self):
        self.geometry("1400x860")
        self.dashboard_view.tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()