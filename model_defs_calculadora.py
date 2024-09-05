# model_defs_calculadora.py

import math
from fractions import Fraction
import re
from sympy import symbols, Eq, solve
from math import perm, comb 

def nPr(a, b):
    return perm(a, b)

def nCr(a, b):
    return comb(a, b)

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
            if not ecuacion.strip():
                return "Error: Ecuación vacía"
            
            if 'nPr(a,b)' in ecuacion or 'nCr(a,b)' in ecuacion:
                return "Error: Sintaxis incompleta en permutación o combinación"

            # Reemplazar símbolos especiales
            ecuacion = ecuacion.replace('÷', '/').replace('^', '**').replace(',', '.').replace('π', 'math.pi')
            ecuacion = self.reemplazar_raices_cuadradas(ecuacion)
            ecuacion = self.manejar_porcentajes(ecuacion)
            ecuacion = ecuacion.replace('|a|', 'abs(')
            ecuacion = ecuacion.replace('π', 'math.pi').replace('e', 'math.e')
            ecuacion = ecuacion.replace('10^', '10**')
            ecuacion = re.sub(r'(\d+)/(\d+)', r'Fraction(\1, \2)', ecuacion)

            # Reemplazar 'log' por 'math.log10' (logaritmo base 10)
            ecuacion = ecuacion.replace('log(', 'math.log10(')
            # Reemplazar 'ln' por 'math.log' (logaritmo natural)
            ecuacion = ecuacion.replace('ln(', 'math.log(')              
            
            # Reemplazar funciones trigonométricas 
            ecuacion = ecuacion.replace('sin(', 'math.sin(')
            ecuacion = ecuacion.replace('cos(', 'math.cos(')
            ecuacion = ecuacion.replace('tan(', 'math.tan(')
            ecuacion = ecuacion.replace('asin(', 'math.asin(')
            ecuacion = ecuacion.replace('acos(', 'math.acos(')
            ecuacion = ecuacion.replace('atan(', 'math.atan(')
            ecuacion = ecuacion.replace('sinh(', 'math.sinh(')
            ecuacion = ecuacion.replace('cosh(', 'math.cosh(')
            ecuacion = ecuacion.replace('tanh(', 'math.tanh(')
            
            # Convertir a radianes si el modo es de grados
            if es_grado:
                ecuacion = self.ecuacion_grados_a_radianes(ecuacion)
           
            # Manejar factorial
            ecuacion = re.sub(r'(\d+)!', r'math.factorial(\1)', ecuacion)
            # Manejar permutación
            ecuacion = re.sub(r'nPr\(([^,]+),\s*([^,]+)\)', r'nPr(int(\1), int(\2))', ecuacion)
            # Manejar combinación
            ecuacion = re.sub(r'nCr\(([^,]+),\s*([^,]+)\)', r'nCr(int(\1), int(\2))', ecuacion)
            # Evaluar fracciones en la forma a/b
            ecuacion = re.sub(r'(\d+)/(\d+)', r'Fraction(\1, \2)', ecuacion)
            
            while '|' in ecuacion:
                ecuacion = re.sub(r'\|([^|]+)\|', r'abs(\1)', ecuacion)

            # Comprobar si 'x' está en la ecuacion para resolver ecuaciones lineales
            if 'x' in ecuacion:
                return self.resolver_ecuacion_lineal(ecuacion)

            if es_grado:
                ecuacion = self.ecuacion_grados_a_radianes(ecuacion)

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
    
    def ecuacion_grados_a_radianes(self, ecuacion):
        # Actualizar solo funciones trigonométricas básicas
        patrones = ['sin', 'cos', 'tan', 'asin', 'acos', 'atan']
        for func in patrones:
            ecuacion = ecuacion.replace(f"{func}(", f"math.{func}(math.radians(")
        return ecuacion

    def resolver_ecuacion_lineal(self, ecuacion):
        x = symbols('x')
        lhs, rhs = ecuacion.split('=')
        lhs_eval = eval(lhs, {"x": x, "math": math})
        rhs_eval = eval(rhs, {"x": x, "math": math})
        eq = Eq(lhs_eval, rhs_eval)
        resultado = solve(eq, x)
        return f"x = {', '.join(map(str, resultado))}"
    
    
    def resolver_ecuacion_lineal(self, ecuacion):
        x = symbols('x')
        try:
            lhs, rhs = ecuacion.split('=')
            lhs_eval = eval(lhs, {"x": x, "math": math, "Fraction": Fraction})
            rhs_eval = eval(rhs, {"x": x, "math": math, "Fraction": Fraction})
        
            eq = Eq(lhs_eval, rhs_eval)
            resultado = solve(eq, x)
            return f"x = {', '.join(map(str, resultado))}"
    
        except Exception as e:
            return f"Error resolviendo la ecuación: {e}"

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