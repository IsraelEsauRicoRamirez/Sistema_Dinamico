import customtkinter as ctk
from tkinter import messagebox
from utils.theme import COLORS, FONTS
from utils.settings_manager import load_settings, save_settings
from utils.db import eliminar_usuario

class SettingsPanel(ctk.CTkFrame):
    """Panel de configuración — sección del dashboard."""

    
    def __init__(self, parent, user_data=None, on_logout=None, **kwargs):
        super().__init__(parent, fg_color=COLORS["bg"], corner_radius=0, **kwargs)
        self.user_data = user_data
        self.on_logout = on_logout
        
        self.settings = load_settings()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self._build()

    def _build(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent",
                                        scrollbar_button_color=COLORS["border"])
        scroll.grid(row=0, column=0, sticky="nsew")
        scroll.grid_columnconfigure(0, weight=1)

        # Respaldo seguro por si "display" no está en tu theme.py
        font_title = FONTS.get("display", FONTS["title"])

        ctk.CTkLabel(scroll, text="Configuración",
                     font=font_title,
                     text_color=COLORS["text_main"],
                     anchor="w").grid(row=0, column=0, sticky="w",
                                      padx=28, pady=(24, 18))

        
        sections = [
            ("🎨 Apariencia", [
                ("Tema de la aplicación", "switch", "tema_app"),
                ("Modo oscuro", "switch", "modo_oscuro"),
                ("Tamaño de fuente", "option", ("tamano_fuente", ["Normal","Grande","Pequeño"])),
            ]),
            ("📊 Simulación", [
                ("Precisión de cálculo", "option", ("precision", ["Alta","Media","Baja"])),
                ("Guardar resultados automáticamente", "switch", "auto_guardar"),
                ("Mostrar animación de gráfica", "switch", "animacion_grafica"),
            ]),
            ("🔔 Notificaciones", [
                ("Alertas de simulación completada", "switch", "alertas"),
                ("Correo al exportar CSV", "switch", "correo_csv"),
            ]),
            ("🌐 Idioma y región", [
                ("Idioma", "option", ("idioma", ["Español","English","Português"])),
                ("Formato de números", "option", ("formato_num", ["1,000.00","1.000,00"])),
            ]),
        ]

        for sec_idx, (sec_title, items) in enumerate(sections):
            card = ctk.CTkFrame(scroll, fg_color=COLORS["card"],
                                corner_radius=18,
                                border_width=1, border_color=COLORS["border"])
            card.grid(row=sec_idx+1, column=0, sticky="ew", padx=28, pady=(0, 14))
            card.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(card, text=sec_title,
                         font=FONTS["label"], text_color=COLORS["text_sub"],
                         anchor="w").grid(row=0, column=0, sticky="w", padx=22, pady=(16,8))

            current_row = 1 
            
            for item_idx, (label, kind, config_data) in enumerate(items):
                is_last = (item_idx == len(items) - 1)
                
                row_f = ctk.CTkFrame(card, fg_color="transparent")
                row_f.grid(row=current_row, column=0, sticky="ew", padx=22, pady=(0, 14 if is_last else 0))
                row_f.grid_columnconfigure(0, weight=1)

                ctk.CTkLabel(row_f, text=label, font=FONTS["subtitle"],
                             text_color=COLORS["text_main"], anchor="w").grid(row=0, column=0, sticky="w", pady=8)

                
                if kind == "switch":
                    config_key = config_data
                    current_val = self.settings.get(config_key, False)
                    
                    sw = ctk.CTkSwitch(row_f, text="",
                                       onvalue=True, offvalue=False,
                                       progress_color=COLORS["green"],
                                       button_color=COLORS["card"],
                                       button_hover_color=COLORS["green_glow"])
                    
                    
                    sw.configure(command=lambda k=config_key, w=sw: self._on_switch_change(k, w.get()))
                    
                    if current_val:
                        sw.select()
                    sw.grid(row=0, column=1, sticky="e")

                elif kind == "option":
                    config_key = config_data[0]
                    options_list = config_data[1]
                    current_val = self.settings.get(config_key, options_list[0])
                    
                    opt = ctk.CTkOptionMenu(row_f,
                                            values=options_list, font=FONTS["subtitle"],
                                            height=36, corner_radius=10,
                                            fg_color=COLORS.get("input_bg", COLORS["surface"]),
                                            button_color=COLORS["green"],
                                            button_hover_color=COLORS.get("green_hover", COLORS["green_dark"]),
                                            dropdown_fg_color=COLORS["card"],
                                            text_color=COLORS["text_main"])
                    
                    
                    opt.configure(command=lambda v, k=config_key: self._on_option_change(k, v))
                    opt.set(current_val)
                    opt.grid(row=0, column=1, sticky="e")
                                      
                current_row += 1 

                if not is_last:
                    ctk.CTkFrame(card, height=1, fg_color=COLORS["border"]).grid(
                        row=current_row, column=0, sticky="ew", padx=22)
                    current_row += 1 

        
        danger = ctk.CTkFrame(scroll, fg_color=COLORS["card"], corner_radius=18,
                              border_width=1, border_color="#FECACA")
        danger.grid(row=len(sections)+1, column=0, sticky="ew", padx=28, pady=(0, 28))
        danger.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(danger, text="⚠️ Zona peligrosa", font=FONTS["label"],
                     text_color="#EF4444", anchor="w").grid(row=0, column=0, sticky="w", padx=22, pady=(16,8))

        row_d = ctk.CTkFrame(danger, fg_color="transparent")
        row_d.grid(row=1, column=0, sticky="ew", padx=22, pady=(0,18))
        row_d.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(row_d, text="Eliminar cuenta permanentemente. Esta acción no se puede deshacer.",
                     font=FONTS["subtitle"], text_color=COLORS["text_sub"], anchor="w").grid(row=0, column=0, sticky="w")

        
        ctk.CTkButton(row_d, text="Eliminar cuenta", font=FONTS["label"],
                      height=36, corner_radius=10, fg_color="transparent",
                      border_width=1, border_color="#EF4444",
                      hover_color="#FEF2F2", text_color="#EF4444",
                      command=self._eliminar_cuenta).grid(row=0, column=1, sticky="e", padx=(16,0))


    

    def _on_switch_change(self, key, is_on):
        """Se ejecuta cada vez que un switch cambia de estado."""
        self.settings[key] = bool(is_on)
        save_settings(self.settings)

        # Si el switch que cambiaron fue el de modo oscuro, aplicamos el tema
        if key == "modo_oscuro":
            if is_on:
                ctk.set_appearance_mode("dark")
            else:
                ctk.set_appearance_mode("light")

    def _on_option_change(self, key, new_value):
        """Se ejecuta cada vez que se selecciona algo en un menú desplegable."""
        self.settings[key] = new_value
        save_settings(self.settings)

        # Si cambiaron la fuente, ajustamos la escala global
        if key == "tamano_fuente":
            escala = 1.0
            if new_value == "Pequeño":
                escala = 0.9
            elif new_value == "Grande":
                escala = 1.15
            
            ctk.set_widget_scaling(escala)

        # Si cambiaron el idioma, notificamos al usuario
        if key == "idioma":
            messagebox.showinfo("Reinicio requerido", "Para aplicar el cambio de idioma en toda la interfaz, por favor reinicia la aplicación.")

    def _eliminar_cuenta(self):
        """Pregunta confirmación y elimina la cuenta."""
        if not self.user_data or self.user_data.get("correo") == "invitado@sdcp.com":
            messagebox.showwarning("Aviso", "No puedes eliminar la cuenta de invitado.")
            return

        respuesta = messagebox.askyesno(
            "Confirmación",
            "¿Estás seguro de que deseas eliminar tu cuenta permanentemente?\nSe borrarán todos tus datos.",
            icon="warning"
        )
        
        if respuesta:
            exito = eliminar_usuario(self.user_data["correo"])
            if exito:
                messagebox.showinfo("Cuenta eliminada", "Tu cuenta ha sido eliminada con éxito.")
                if self.on_logout:
                    self.on_logout() # Cierra sesión
            else:
                messagebox.showerror("Error", "No se pudo eliminar la cuenta.")