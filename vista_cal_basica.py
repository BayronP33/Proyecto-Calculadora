# vista_cal_basica.py

import tkinter as tk

class VistaCalculadora:
    def __init__(self, root, controlador):
        self.ventana_principal = root
        self.controlador = controlador
        self.ecuacion = tk.StringVar()
        self.panel_historial = None
        self.opciones_modo = None
        self.interfaz_creada = False
        self.resultado_mostrado = False
        self.crear_interfaz()

    def crear_interfaz(self):
        self.ventana_principal.title("Calculadora")
        self.ventana_principal.geometry("1000x600")

        self.marco_principal = tk.Frame(self.ventana_principal, bg="#8D99AE")
        self.marco_principal.pack(expand=True, fill='both')

        self.marco_entrada = tk.Frame(self.marco_principal, bg="#8D99AE")
        self.marco_entrada.grid(row=0, column=0, columnspan=10, ipadx=8, ipady=8, padx=10, pady=10, sticky="nsew")

        self.campo_entrada = tk.Entry(self.marco_entrada, textvariable=self.ecuacion, font=("Arial", 20), justify='right', bg="#2B2D42", fg="#EDF2F4")
        self.campo_entrada.pack(fill='both', expand=True)

        self.marco_historial = tk.Frame(self.marco_principal, bg="#8D99AE")
        self.marco_historial.grid(row=0, column=10, rowspan=6, sticky="nsew", padx=10, pady=10)

        self.panel_historial = tk.Listbox(self.marco_historial, height=10, font=("Arial", 14), bg="#2B2D42", fg="#EDF2F4")
        self.panel_historial.pack(fill='both', expand=True)

        self.boton_cambiar_modo = tk.Button(self.marco_historial, text="Cambiar Modo", command=self.mostrar_opciones_modo, font=("Arial", 14), bg="#2B2D42", fg="#EDF2F4")
        self.boton_cambiar_modo.pack(pady=10)

        self.opciones_modo = tk.Frame(self.marco_historial, bg="#8D99AE")
        self.boton_basica = tk.Button(self.opciones_modo, text="Básica", command=self.controlador.modo_basico, font=("Arial", 14), bg="#2B2D42", fg="#EDF2F4")
        self.boton_cientifica = tk.Button(self.opciones_modo, text="Científica", command=self.controlador.modo_cientifico, font=("Arial", 14), bg="#2B2D42", fg="#EDF2F4")
        self.boton_graficadora = tk.Button(self.opciones_modo, text="Graficadora", command=self.controlador.lanzar_graficadora, font=("Arial", 14), bg="#2B2D42", fg="#EDF2F4")

        self.boton_basica.pack(pady=5)
        self.boton_cientifica.pack(pady=5)
        self.boton_graficadora.pack(pady=5)

        self.interfaz_creada = True

    def mostrar_opciones_modo(self):
        if self.opciones_modo.winfo_ismapped():
            self.opciones_modo.pack_forget()
        else:
            self.opciones_modo.pack(pady=10)

    def crear_botones(self, botones, font):
        for (texto, fila, columna) in botones:
            color_fondo = "#2B2D42"
            color_fuente = "white"
            if texto in {'+', '-', '*', '÷', '(', ')', 'π', '√', '^', 'sin', 'cos', 'tan', 'log', 'ln', 'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh'}:
                color_fuente = "#FCBF49"
            elif texto in {'AC', 'Del'}:
                color_fuente = "#EF233C"
            elif texto in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '%', ',', '=', 'a/b', '10^', 'e', '|a|', 'nPr', 'nCr'}:
                color_fuente = "#EDF2F4"

            boton = tk.Button(self.marco_principal, text=texto, command=lambda t=texto: self.controlador.al_hacer_clic_en_boton(t),
                              font=font, bg=color_fondo, fg=color_fuente, width=4, height=2)
            boton.grid(row=fila, column=columna, sticky="nsew", ipadx=10, ipady=10, padx=5, pady=5)
            self.marco_principal.grid_rowconfigure(fila, weight=1)
            self.marco_principal.grid_columnconfigure(columna, weight=1)

    def limpiar_botones(self):
        for widget in self.marco_principal.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()

    def actualizar_panel_historial(self, historial):
        self.panel_historial.delete(0, tk.END)
        historial = list(reversed(historial))  # Reversar para que el más nuevo aparezca arriba
        for item in historial:
            self.panel_historial.insert(tk.END, item)