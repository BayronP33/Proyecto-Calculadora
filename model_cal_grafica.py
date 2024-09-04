# model_cal_grafica.py
import sympy as sp
import numpy as np
import re
import matplotlib.pyplot as plt


class ModeloGraficadora:
    def preprocess_equation(self, eq_str):
        processed_eq = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', eq_str)
        processed_eq = processed_eq.replace('^', '**')
        return processed_eq

    def plot_function(self, equation_str):
        try:
            equation_str = self.preprocess_equation(equation_str)
            x = sp.Symbol('x')
            if 'x' not in equation_str:
                function = sp.sympify(equation_str)
                y_vals = [function] * 400
                x_vals = np.linspace(-10, 10, 400)
            else:
                function = sp.sympify(equation_str)
                f = sp.lambdify(x, function, 'numpy')
                x_vals = np.linspace(-10, 10, 400)
                y_vals = f(x_vals)
            return x_vals, y_vals, str(function)
        except Exception as e:
            raise ValueError(f"Error al graficar la función: {e}")

    def evaluate_expression(self, expression_str):
        try:
            expression_str = self.preprocess_equation(expression_str)
            result = sp.sympify(expression_str).evalf()
            return result
        except Exception as e:
            raise ValueError(f"Error al evaluar la expresión: {e}")
        
    def plot_circle(self, centro_x, centro_y, radio):
        """
        Grafica un círculo en el plano XY dado su centro y radio.
        
        Parámetros:
        centro_x (float): Coordenada X del centro del círculo.
        centro_y (float): Coordenada Y del centro del círculo.
        radio (float): Radio del círculo.
        """
        # Generar ángulo para el círculo
        theta = np.linspace(0, 2 * np.pi, 100)

        # Coordenadas del círculo
        x = centro_x + radio * np.cos(theta)
        y = centro_y + radio * np.sin(theta)

        # Crear la gráfica
        plt.figure(figsize=(6, 6))
        plt.plot(x, y, label=f'Círculo con centro ({centro_x}, {centro_y}) y radio {radio}')
        plt.scatter(centro_x, centro_y, color='red', zorder=5)  # Centro del círculo
        plt.text(centro_x, centro_y, f'  Centro ({centro_x}, {centro_y})', verticalalignment='bottom', horizontalalignment='right')

        # Configurar los ejes
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        plt.grid(True, which='both')
        plt.gca().set_aspect('equal', adjustable='box')  # Aspecto igual para x e y
        plt.title('Gráfico del Círculo')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.show()
