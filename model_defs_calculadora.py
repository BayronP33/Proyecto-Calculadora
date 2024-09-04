# model_defs_calculadora.py

import math
from fractions import Fraction
import re
from sympy import symbols, Eq, solve
from math import comb, perm

class ModeloCalculadora:
    def __init__(self):
        self.historial = []
        self.modo_grados = True

    def agregar_al_historial(self, operacion):
        self.historial.insert(0, operacion)  # Insertar al principio de la lista
        if len(self.historial) > 30:
            self.historial.pop()  # Eliminar el último elemento si el tamaño es mayor a 30

    def calcular_resultado(self, ecuacion, es_grado):
        try:
            # Reemplazar símbolos especiales
            ecuacion = ecuacion.replace('÷', '/').replace('^', '**').replace(',', '.').replace('π', 'math.pi')
            ecuacion = self.reemplazar_raices_cuadradas(ecuacion)
            ecuacion = self.manejar_porcentajes(ecuacion)
            ecuacion = ecuacion.replace('π', 'math.pi').replace('e', 'math.e')
            ecuacion = ecuacion.replace('10^', '10**')

            # Manejar factorial
            ecuacion = re.sub(r'(\d+)!', r'math.factorial(\1)', ecuacion)
            # Manejar permutación
            ecuacion = re.sub(r'nPr\(([^,]+),\s*([^,]+)\)', r'perm(\1, \2)', ecuacion)
            # Manejar combinación
            ecuacion = re.sub(r'nCr\(([^,]+),\s*([^,]+)\)', r'comb(\1, \2)', ecuacion)

            # Reemplazar funciones trigonométricas con math.<funcion>(
            funciones_trigonometricas = ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh']
            for funcion in funciones_trigonometricas:
                ecuacion = ecuacion.replace(funcion+'(', 'math.'+funcion+'(')

            if es_grado:
                ecuacion = self.ecuacion_grados_a_radianes(ecuacion)

            # Comprobar si 'x' está en la ecuacion para resolver ecuaciones lineales
            if 'x' in ecuacion:
                return self.resolver_ecuacion_lineal(ecuacion)

            # Manejar el cálculo
            resultado = str(eval(ecuacion, {"math": math, "Fraction": Fraction, "perm": perm, "comb": comb}))

            # Limpieza de ceros innecesarios
            if '.' in resultado:
                resultado = resultado.rstrip('0').rstrip('.') if '.' in resultado else resultado

            return resultado.replace('.', ',')
        except ZeroDivisionError:
            return "Error: Div/0"
        except SyntaxError:
            return "Error: Syntax"
        except Exception as e:
            print(f"Error inesperado: {e}")
            return "Error"

    def resolver_ecuacion_lineal(self, ecuacion):
        x = symbols('x')
        lhs, rhs = ecuacion.split('=')
        eq = Eq(eval(lhs, {"x": x}), eval(rhs, {"x": x}))
        resultado = solve(eq, x)
        return f"x = {', '.join(map(str, resultado))}"

    def ecuacion_grados_a_radianes(self, ecuacion):
        funciones_trigonometricas = ['sin', 'cos', 'tan', 'asin', 'acos', 'atan']
        for funcion in funciones_trigonometricas:
            ecuacion = ecuacion.replace(f"{funcion}(", f"math.{funcion}(math.radians(")
        return ecuacion
    
    def reemplazar_raices_cuadradas(self, ecuacion):
        patron = re.compile(r'√\[(\d+)\]\(([^)]+)\)')
        while '√' in ecuacion:
            coincidencia = patron.search(ecuacion)
            if not coincidencia:
                break
            n = int(coincidencia.group(1))
            x = coincidencia.group(2)
            reemplazo = f'({x})**(1/{n})'
            ecuacion = ecuacion[:coincidencia.start()] + reemplazo + ecuacion[coincidencia.end():]
        return ecuacion

    
    def manejar_porcentajes(self, ecuacion):
        patron = re.compile(r'(\d+(\.\d+)?)%(\d+(\.\d+)?)')
        coincidencias = patron.findall(ecuacion)

        for coincidencia in coincidencias:
            porcentaje = float(coincidencia[0]) / 100
            numero = coincidencia[2]
            reemplazo = f'({porcentaje}*{numero})'
            coincidencia_completa = coincidencia[0] + '%' + coincidencia[2]
            ecuacion = ecuacion.replace(coincidencia_completa, reemplazo)

        return ecuacion