# vista_cal_grafica.py

import tkinter as tk
import matplotlib.pyplot as plt

class VistaGraficadora:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Graficadora y Evaluadora")
        self.panels = []
        self.lines = {}
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.axhline(0, color='black', linewidth=1)
        self.ax.axvline(0, color='black', linewidth=1)
        self.ax.grid(True)
        self.add_panel_button = tk.Button(self.root, text="Agregar Panel +")
        self.add_panel_button.grid(row=1, column=0, pady=10)

    def create_function_panel(self, row, panel_index, on_graficar, on_clear, on_eliminar):
        frame = tk.Frame(self.root)
        frame.grid(row=row, column=0, padx=10, pady=5)
        self.panels.append(frame)
        label = tk.Label(frame, text=f"Ingrese la función a graficar o evaluar (Panel {panel_index + 1}):")
        label.grid(row=0, column=0, columnspan=4, sticky=tk.W)
        equation_entry = tk.Entry(frame, width=50)
        equation_entry.grid(row=1, column=0, columnspan=4, sticky=tk.W)
        button_graficar = tk.Button(frame, text="Graficar/Evaluar", command=lambda: on_graficar(equation_entry.get(), panel_index))
        button_graficar.grid(row=1, column=4, padx=5)
        button_clear = tk.Button(frame, text="AC", command=lambda: on_clear(panel_index))
        button_clear.grid(row=1, column=5, padx=5)
        button_eliminar = tk.Button(frame, text="Eliminar", command=lambda: on_eliminar(panel_index))
        button_eliminar.grid(row=1, column=6, padx=5)
        return frame

    def show_error(self, message):
        tk.messagebox.showerror("Error", message)

    def show_result(self, result):
        tk.messagebox.showinfo("Resultado", f"El resultado de la expresión es: {result}")

    def update_plot(self, x_vals, y_vals, label, panel_index):
        line, = self.ax.plot(x_vals, y_vals, label=label)
        self.lines[panel_index] = line
        self.ax.legend()
        self.fig.canvas.draw()
        plt.show()

    def clear_plot(self, panel_index):
        if panel_index in self.lines:
            self.lines[panel_index].remove()
            del self.lines[panel_index]
        self.ax.legend()
        self.fig.canvas.draw()