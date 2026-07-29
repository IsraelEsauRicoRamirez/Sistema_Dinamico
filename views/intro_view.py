import customtkinter as ctk

class IntroView(ctk.CTkScrollableFrame): 
    # 1. Agregamos on_continue como parámetro explícito
    def __init__(self, master, on_continue=None, **kwargs): 
        # 2. Pasamos solo **kwargs al padre, on_continue ya fue extraído
        super().__init__(master, **kwargs)
        
        # Guardamos la función para usarla en el botón
        self.on_continue = on_continue 
        
        self.grid_columnconfigure(0, weight=1)
        self.configure(fg_color="transparent")

        # --- ENCABEZADO ---
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, pady=(10, 30), sticky="ew")
        
        title = ctk.CTkLabel(header_frame, text="SDCP", font=ctk.CTkFont(size=40, weight="bold"), text_color="#E0E0E0")
        title.pack()
        subtitle = ctk.CTkLabel(header_frame, text="Sistemas Dinámicos de Crecimiento Poblacional", font=ctk.CTkFont(size=16), text_color="gray")
        subtitle.pack()

        # --- SECCIÓN 1: ¿QUÉ ES? ---
        self.create_section_title("¿Qué es un Sistema Dinámico?")
        
        intro_text = (
            "Es un modelo matemático que describe cómo cambia una población en el tiempo.\n"
            "Utiliza Ecuaciones Diferenciales Ordinarias (EDO) para calcular la tasa de cambio "
            "(qué tan rápido crece o decrece la población)."
        )
        self.create_info_card(intro_text)

        # --- SECCIÓN 2: MODELO DE MALTHUS ---
        self.create_section_title("Modelo Exponencial de Malthus")
        
        malthus_frame = ctk.CTkFrame(self, fg_color="#2B2B2B", corner_radius=10)
        malthus_frame.grid(row=4, column=0, pady=(0, 20), sticky="ew", ipadx=20, ipady=20)
        malthus_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(malthus_frame, text="Premisa: El crecimiento es proporcional al número de individuos. Asume recursos infinitos.", 
                     font=ctk.CTkFont(size=14, weight="bold"), text_color="#2ECC71").grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky="w")

        # Ecuaciones
        ctk.CTkLabel(malthus_frame, text="Ecuación Diferencial:\n\ndP/dt = r · P", font=ctk.CTkFont(size=14)).grid(row=1, column=0, padx=10, sticky="ew")
        ctk.CTkLabel(malthus_frame, text="Solución Analítica:\n\nP(t) = P₀ · e^(r·t)", font=ctk.CTkFont(size=14), 
                     fg_color="#1E5128", corner_radius=8).grid(row=1, column=1, padx=10, sticky="ew")

        # Variables Resumidas
        vars_text = "Variables: P(t) = Población final | P₀ = Población inicial | r = Tasa de crecimiento | t = Tiempo"
        ctk.CTkLabel(malthus_frame, text=vars_text, text_color="gray").grid(row=2, column=0, columnspan=2, pady=(15, 0), sticky="w")

        # --- SECCIÓN 3: MODELO LOGÍSTICO ---
        self.create_section_title("Modelo Logístico (Verhulst)")
        
        log_frame = ctk.CTkFrame(self, fg_color="#2B2B2B", corner_radius=10)
        log_frame.grid(row=6, column=0, pady=(0, 20), sticky="ew", ipadx=20, ipady=20)
        log_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(log_frame, text="Premisa: El crecimiento disminuye a medida que la población alcanza el límite de recursos.", 
                     font=ctk.CTkFont(size=14, weight="bold"), text_color="#3498DB").grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky="w")

        # Ecuaciones
        ctk.CTkLabel(log_frame, text="Ecuación Diferencial:\n\ndP/dt = r · P(1 - P/K)", font=ctk.CTkFont(size=14)).grid(row=1, column=0, padx=10, sticky="ew")
        ctk.CTkLabel(log_frame, text="Solución Analítica:\n\nP(t) = K / (1 + C · e^(-r·t))", font=ctk.CTkFont(size=14), 
                     fg_color="#1A3B5C", corner_radius=8).grid(row=1, column=1, padx=10, sticky="ew")

        # Variables Resumidas
        vars_log_text = "Variables extra: K = Capacidad de carga (límite máximo) | C = Constante de integración"
        ctk.CTkLabel(log_frame, text=vars_log_text, text_color="gray").grid(row=2, column=0, columnspan=2, pady=(15, 0), sticky="w")

        # --- EJEMPLO RESUELTO ---
        ejemplo_frame = ctk.CTkFrame(self, fg_color="#D5F5E3", corner_radius=10) 
        ejemplo_frame.grid(row=7, column=0, pady=(10, 30), sticky="ew", ipadx=20, ipady=15)
        
        ctk.CTkLabel(ejemplo_frame, text="Ejemplo resuelto — Cultivo de bacterias", font=ctk.CTkFont(size=16, weight="bold"), 
                     text_color="#145A32").pack(anchor="w", pady=(0, 10))
        ctk.CTkLabel(ejemplo_frame, text="Si iniciamos con 150 bacterias y crecen a una tasa del 20% (0.2) por hora, ¿cuántas habrá en 5 horas?\nP(5) = 150 · e^(0.2 · 5) ≈ 407 bacterias.", 
                     justify="left", text_color="black").pack(anchor="w")

        # --- BOTÓN DE CONTINUAR ---
        # Usamos el parámetro on_continue que extrajimos en el __init__
        if self.on_continue:
            btn_continuar = ctk.CTkButton(self, text="Continuar al Simulador", font=ctk.CTkFont(weight="bold"),
                                          command=self.on_continue, height=40)
            btn_continuar.grid(row=8, column=0, pady=(0, 40))

    def create_section_title(self, text):
        title_lbl = ctk.CTkLabel(self, text=f"▍ {text}", font=ctk.CTkFont(size=20, weight="bold"), text_color="#2ECC71")
        row = self.grid_size()[1] 
        title_lbl.grid(row=row, column=0, pady=(10, 10), sticky="w")

    def create_info_card(self, text):
        card = ctk.CTkFrame(self, fg_color="#2B2B2B", corner_radius=10)
        row = self.grid_size()[1]
        card.grid(row=row, column=0, pady=(0, 20), sticky="ew", ipadx=20, ipady=15)
        lbl = ctk.CTkLabel(card, text=text, justify="left", font=ctk.CTkFont(size=14), text_color="#CCCCCC")
        lbl.pack(anchor="w")