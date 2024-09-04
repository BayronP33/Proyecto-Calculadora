#control_calculadora.py:

import tkinter as tk
from vista_cal_basica import VistaCalculadora
from model_defs_calculadora import ModeloCalculadora
import subprocess
import sys
import tkinter.messagebox as tk_messagebox
import control_firebase
import math

class ControladorCalculadora:
    def __init__(self, root, nombre_usuario):
        self.nombre_usuario = nombre_usuario
        self.modelo = ModeloCalculadora()
        self.vista = VistaCalculadora(root, self)
        self.vista.ventana_principal.after(0, self.inicializar_vista, nombre_usuario)

    def inicializar_vista(self, nombre_usuario):
        self.vista.ventana_principal.title(f"Calculadora de {nombre_usuario}")
        if self.vista.interfaz_creada:
            self.modo_basico()
        self.cargar_historial()

    def cargar_historial(self):
        # Cargar el historial individual del usuario desde Firestore
        historial_usuario = control_firebase.leer_historial_usuario(self.nombre_usuario)
        self.modelo.historial = historial_usuario

        # Cargar las últimas 90 operaciones desde la base de datos en tiempo real y actualizar la vista
        historial_general = control_firebase.leer_historial_realtime()
        self.vista.actualizar_panel_historial(historial_general)

    def actualizar_historiales(self):
        historial = self.modelo.historial
        control_firebase.actualizar_historial_usuario(self.nombre_usuario, historial)

        historial_realtime_db = control_firebase.leer_historial_realtime()
        # Mantener solo las últimas 90 operaciones
        historial_realtime_db = historial[-90:]
        control_firebase.actualizar_historial_realtime(historial_realtime_db)

        # Actualizar panel de historial inmediatamente
        self.vista.actualizar_panel_historial(historial)

    def al_hacer_clic_en_boton(self, caracter):
        if self.vista.resultado_mostrado:
            if caracter not in ('+', '-', '*', '÷', '^'):
                self.vista.ecuacion.set("")  # Reiniciar solo si no es un operador
                self.vista.resultado_mostrado = False

        if caracter == '=':
            operacion = self.vista.ecuacion.get()
            resultado = self.modelo.calcular_resultado(operacion, self.modelo.modo_grados)
            self.vista.ecuacion.set(resultado)
            operacion_completa = f'{operacion} = {resultado}'
            self.modelo.agregar_al_historial(operacion_completa)
            self.actualizar_historiales()  # Actualizar ambos historiales (usuario y general)
            self.vista.resultado_mostrado = True
        elif caracter in ('+', '-', '*', '÷', '^'):
            if self.vista.resultado_mostrado:
                self.vista.ecuacion.set(self.vista.ecuacion.get() + caracter)  # Continuar con la operación
                self.vista.resultado_mostrado = False
            else:
                self.vista.ecuacion.set(self.vista.ecuacion.get() + caracter)
        elif caracter == 'AC':
            self.vista.ecuacion.set("")
        elif caracter == '√':
            self.vista.ecuacion.set(self.vista.ecuacion.get() + "√[")
        elif caracter == ']':
            self.vista.ecuacion.set(self.vista.ecuacion.get() + "](")
        elif caracter.lower() == 'del':
            self.vista.ecuacion.set(self.vista.ecuacion.get()[:-1])
        elif caracter in ['π', 'e', '10^']:
            self.vista.ecuacion.set(self.vista.ecuacion.get() + caracter)
        elif caracter == '|a|':
            self.vista.ecuacion.set(self.vista.ecuacion.get() + "abs(")
        elif caracter == 'a/b':
            self.vista.ecuacion.set(self.vista.ecuacion.get() + "Fraction(")
        elif caracter in {'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh', 'log', 'ln'}:
            self.vista.ecuacion.set(self.vista.ecuacion.get() + f"{caracter}(")
        elif caracter == '10^':
            self.vista.ecuacion.set(self.vista.ecuacion.get() + "10**")
        elif caracter in {'nPr', 'nCr'}:
            self.vista.ecuacion.set(self.vista.ecuacion.get() + f"{caracter}(")
        elif caracter == 'Deg':
            self.modelo.modo_grados = True
            tk_messagebox.showinfo("Modo", "Modo Grados Activado")
        elif caracter == 'Rad':
            self.modelo.modo_grados = False
            tk_messagebox.showinfo("Modo", "Modo Radianes Activado")
        elif caracter.isnumeric():
            if self.vista.resultado_mostrado:
                self.vista.ecuacion.set(caracter)
                self.vista.resultado_mostrado = False 
            else:
                self.vista.ecuacion.set(self.vista.ecuacion.get() + caracter)
        else:
            if self.vista.resultado_mostrado and caracter.isdigit():
                self.vista.ecuacion.set(caracter)
                self.vista.resultado_mostrado = False
            else:
                self.vista.ecuacion.set(self.vista.ecuacion.get() + caracter)

    def modo_basico(self):
        self.vista.limpiar_botones()
        self.vista.ventana_principal.geometry("800x600")
        botones = [
            ('(', 1, 0), (')', 1, 1), ('7', 1, 2), ('8', 1, 3), ('9', 1, 4), ('÷', 1, 5),
            ('^', 2, 0), ('√', 2, 1), ('4', 2, 2), ('5', 2, 3), ('6', 2, 4), ('*', 2, 5),
            ('Del', 3, 0), ('AC', 3, 1), ('1', 3, 2), ('2', 3, 3), ('3', 3, 4), ('-', 3, 5),
            ('π', 4, 0), ('%', 4, 1), ('0', 4, 2), (',', 4, 3), ('=', 4, 4), ('+', 4, 5)
        ]
        self.vista.crear_botones(botones, font=("Arial", 20))

    def modo_cientifico(self):
        self.vista.limpiar_botones()
        self.vista.ventana_principal.geometry("1000x600")
        botones = [
            ('sin', 1, 0), ('cos', 1, 1), ('tan', 1, 2), ('7', 1, 3), ('8', 1, 4), ('9', 1, 5), ('%', 1, 6), ('*', 1, 7), ('^', 1, 8),
            ('asin', 2, 0), ('acos', 2, 1), ('atan', 2, 2), ('4', 2, 3), ('5', 2, 4), ('6', 2, 5), ('e', 2, 6), ('+', 2, 7), ('-', 2, 8),
            ('sinh', 3, 0), ('cosh', 3, 1), ('tanh', 3, 2), ('3', 3, 3), ('2', 3, 4), ('1', 3, 5), ('!', 3, 6), ('÷', 3, 7), ('√', 3, 8),
            ('(', 4, 0), (')', 4, 1), ('a/b', 4, 2), ('0', 4, 3), ('Del', 4, 4), ('AC', 4, 5), ('x', 4, 6), ('|a|', 4, 7), ('nPr', 4, 8),
            ('10^', 5, 0), ('Deg', 5, 1), ('Rad', 5, 2), ('=', 5, 3), ('.', 5, 4), ('log', 5, 5), ('ln', 5, 6), ('π', 5, 7), ('nCr', 5, 8)
        ]
        self.vista.crear_botones(botones, font=("Arial", 12))

    def lanzar_graficadora(self):
        subprocess.Popen(['python', 'control_cal_grafica.py'])

def iniciar_vista(nombre_usuario="Usuario"):
    root = tk.Tk()
    controlador = ControladorCalculadora(root, nombre_usuario)
    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        nombre_usuario = sys.argv[1]
    else:
        nombre_usuario = "Usuario"
    iniciar_vista(nombre_usuario)