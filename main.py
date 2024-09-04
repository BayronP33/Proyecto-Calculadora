from vista_ventana_de_inicio import VentanaDeInicio
import tkinter as tk

if __name__ == "__main__":
    # Crear la ventana principal
    root = tk.Tk()
    # Iniciar la ventana de inicio
    app = VentanaDeInicio(root)
    # Ejecutar el bucle principal de la interfaz
    root.mainloop()
