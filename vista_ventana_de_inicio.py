# vista_ventana_de_inicio.py

import tkinter as tk
from tkinter import messagebox
import subprocess

class VentanaDeInicio:
    def __init__(self, ventana_principal):
        self.ventana_principal = ventana_principal
        self.ventana_principal.title("Ventana de Inicio")
        self.ventana_principal.geometry("300x150")
        
        self.marco = tk.Frame(self.ventana_principal, bg='#2B2D42')
        self.marco.pack(expand=True, fill='both')
        
        self.etiqueta = tk.Label(self.marco, text="Ingrese su nombre:", font=("Arial", 14), bg='#2B2D42', fg='White')
        self.etiqueta.pack(pady=10)
        
        self.campo_nombre = tk.Entry(self.marco, font=("Arial", 14), bg='#8D99AE')
        self.campo_nombre.pack(pady=5)
        
        self.boton_continuar = tk.Button(self.marco, text="Continuar", command=self.continuar, font=("Arial", 14), bg='#33ffbd', fg='Black')
        self.boton_continuar.pack(pady=10)
    
    def continuar(self):
        nombre_usuario = self.campo_nombre.get().strip()
        if nombre_usuario:
            self.abrir_calculadora_basica(nombre_usuario)
        else:
            messagebox.showwarning("Advertencia", "Por favor ingrese su nombre.")
    
    def abrir_calculadora_basica(self, nombre_usuario):
        subprocess.Popen(['python', 'control_calculadora.py', nombre_usuario])
        self.ventana_principal.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaDeInicio(root)
    root.mainloop()