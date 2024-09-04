# control_cal_grafica.py

import tkinter as tk
from model_cal_grafica import ModeloGraficadora
from vista_cal_grafica import VistaGraficadora

class ControladorGraficadora:
    def __init__(self, root):
        self.modelo = ModeloGraficadora()
        self.vista = VistaGraficadora(root)
        self.vista.add_panel_button.config(command=self.add_function_panel)
        self.vista.create_function_panel(0, 0, self.graficar, self.clear_entry, self.eliminar_panel)

    def graficar(self, equation_str, panel_index):
        try:
            if 'x' in equation_str or '(' in equation_str:
                x_vals, y_vals, label = self.modelo.plot_function(equation_str)
                self.vista.update_plot(x_vals, y_vals, label, panel_index)
            else:
                result = self.modelo.evaluate_expression(equation_str)
                self.vista.show_result(result)
        except ValueError as e:
            self.vista.show_error(str(e))

    def clear_entry(self, panel_index):
        self.vista.clear_plot(panel_index)

    def eliminar_panel(self, panel_index):
        self.clear_entry(panel_index)
        frame = self.vista.panels[panel_index]
        frame.destroy()
        del self.vista.panels[panel_index]
        for i, panel in enumerate(self.vista.panels):
            panel.grid(row=i, column=0, padx=10, pady=5)
        self.vista.add_panel_button.grid(row=len(self.vista.panels) + 1, column=0, pady=10)

    def add_function_panel(self):
        panel_index = len(self.vista.panels)
        self.vista.create_function_panel(panel_index, panel_index, self.graficar, self.clear_entry, self.eliminar_panel)

def iniciar_vista(nombre_usuario="Usuario"):
    root = tk.Tk()
    controlador = ControladorGraficadora(root)
    controlador.vista.root.title(f"Calculadora de {nombre_usuario}")  
    root.mainloop()

if __name__ == "__main__":
    iniciar_vista()