import customtkinter as ctk
from views.login_view import LoginView
from views.register_view import RegisterView
from views.intro_view import IntroView
from views.dashboard_view import DashboardView
from utils.theme import COLORS
from utils.db import init_db
from utils.settings_manager import load_settings  # <-- IMPORTAMOS EL SETTINGS MANAGER

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # 1. Cargar configuraciones ANTES de renderizar la ventana
        config = load_settings()
        
        # 2. Aplicar modo oscuro/claro guardado
        if config.get("modo_oscuro", False):
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")
            
        # 3. Aplicar tamaño de fuente guardado globalmente
        tamano = config.get("tamano_fuente", "Normal")
        if tamano == "Pequeño":
            ctk.set_widget_scaling(0.9)
        elif tamano == "Grande":
            ctk.set_widget_scaling(1.15)
        else:
            ctk.set_widget_scaling(1.0)
            
        ctk.set_default_color_theme("green")

        self.title("SDCP — Sistemas Dinámicos de Crecimiento Poblacional")
        self.geometry("1100x720")
        self.minsize(900, 620)
        self.configure(fg_color=COLORS["bg"])

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Variables para almacenar el estado global
        self.current_user_data = None

        # Instanciamos las vistas base
        self.login_view = LoginView(
            self,
            on_go_register=self.show_register,
            on_login_success=self.show_intro
        )

        self.register_view = RegisterView(
            self,
            on_go_login=self.show_login,
        )

        self.intro_view = IntroView(
            self,
            on_continue=self.show_dashboard,
        )

        # El Dashboard se instanciará más adelante dinámicamente cuando sepamos quién entró
        self.dashboard_view = None
        
        # Iniciamos mostrando la pantalla de login de forma segura
        self.show_login()

    # --- NUEVA FUNCIÓN PARA LIMPIAR LA PANTALLA ---
    def hide_all_views(self):
        """Oculta todas las vistas activas de la pantalla para evitar que se encimen."""
        self.login_view.grid_forget()
        self.register_view.grid_forget()
        self.intro_view.grid_forget()
        if self.dashboard_view is not None:
            self.dashboard_view.grid_forget()

    # --- NAVEGACIÓN CORREGIDA ---
    def show_login(self):
        self.hide_all_views() # Ocultamos todo primero
        self.geometry("1100x720")
        self.login_view.grid(row=0, column=0, sticky="nsew") # Mostramos solo el login

    def show_register(self):
        self.hide_all_views()
        self.geometry("1100x800")
        self.register_view.grid(row=0, column=0, sticky="nsew")

    # Modificado para recibir los datos tras un login exitoso
    def show_intro(self, user_data=None):
        if user_data:
            self.current_user_data = user_data
            
        self.hide_all_views()
        self.geometry("1280x820")
        self.intro_view.grid(row=0, column=0, sticky="nsew")

    def show_dashboard(self):
        self.hide_all_views()
        
        # Si es la primera vez que entramos al dashboard, lo creamos con los datos reales
        if self.dashboard_view is None:
            # Datos por defecto como respaldo por si falla el login
            fallback_data = {
                "nombre": "Invitado",
                "rol": "Usuario",
                "matricula": "N/A",
                "correo": "invitado@sdcp.com"
            }
            
            self.dashboard_view = DashboardView(
                self,
                user_data=self.current_user_data or fallback_data,
                on_show_intro=self.show_intro_from_dashboard,  # solo muestra intro, sin cerrar sesión
            )
            
        self.geometry("1400x860")
        self.dashboard_view.grid(row=0, column=0, sticky="nsew")
        
    def show_intro_from_dashboard(self):
        """Muestra la intro desde el dashboard sin cerrar sesión.
        El botón 'Volver al simulador' de la intro regresa al dashboard."""
        self.hide_all_views()
        self.geometry("1280x820")
        # Reconectamos on_continue para que regrese al dashboard (no a show_dashboard
        # que recrearía el widget), sino directamente mostrar el dashboard existente
        self.intro_view.on_continue = self._return_to_dashboard
        self.intro_view.grid(row=0, column=0, sticky="nsew")

    def _return_to_dashboard(self):
        """Regresa al dashboard existente después de ver la intro (sin recrearlo)."""
        self.hide_all_views()
        self.geometry("1400x860")
        if self.dashboard_view is not None:
            self.dashboard_view.grid(row=0, column=0, sticky="nsew")
        else:
            # Si por alguna razón no existe, lo recreamos
            self.show_dashboard()

    def logout(self):
        """Se ejecuta al cerrar sesión o al eliminar la cuenta."""
        self.current_user_data = None  # Borramos la sesión activa
        
        # Destruimos la vista del Dashboard para obligar a que se regenere 
        # desde cero cuando entre el siguiente usuario.
        if self.dashboard_view is not None:
            self.dashboard_view.destroy()
            self.dashboard_view = None

        # Restauramos on_continue de la intro para que vaya a show_dashboard normal
        self.intro_view.on_continue = self.show_dashboard
            
        # Regresamos a la pantalla de inicio de sesión
        self.show_login()


if __name__ == "__main__":
    init_db()  # <-- CREAMOS LA BASE DE DATOS Y LA TABLA ANTES DE ABRIR LA APP
    app = App()
    app.mainloop()