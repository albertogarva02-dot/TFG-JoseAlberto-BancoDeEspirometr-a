#_____________________________________________________________________________________________________________________
#    Nombre del Script: generadoronda.py
#    Autor: José Alberto García Valiño
#    Fecha: 07-12-2025
#    Descripción:
#        Clase encargada de generar trayectorias matemáticas.
#        Creación de ondas estándar (senoidales, rectificadas) y
#        Evalua ecuaciones personalizadas introducidas por el usuario.
#______________________________________________________________________________________________________________________

__author__ = "José Alberto García Valiño"
__copyright__ = "Copyright 2025, José Alberto García Valiño"
__credits__ = ["José Alberto García Valiño"]
__license__ = "MIT"
__version__ = "1.0"
__status__ = "Beta"


import math

class GENERADORONDA:
    def __init__(self, amplitud_mm, velocidad_pct, tipo_onda, ecuacion_usuario=""):
        if amplitud_mm is None: amplitud_mm = 0
        self.amplitud_mm_raw = amplitud_mm 
        
        self.amplitud_grados = amplitud_mm / 0.2618
        
        if velocidad_pct is None: velocidad_pct = 10
        self.V = velocidad_pct * 0.01 
        self.frecuencia = self.V * 2 * math.pi
        
        self.tipo = tipo_onda
        self.ecuacion = ecuacion_usuario
        
        self.volviendo = False
        self.fin_retorno = False
        self.pos_actual_grados = 0.0 
        
        self.OFFSET_GRADOS = 0 / 0.2618 

    def siguiente_valor(self, tiempo_acumulado):
        # MODO RETORNO
        if self.volviendo:
            velocidad_bajada = 2.0 
            self.pos_actual_grados -= velocidad_bajada
            if self.pos_actual_grados <= self.OFFSET_GRADOS:
                self.pos_actual_grados = self.OFFSET_GRADOS
                self.fin_retorno = True
            return tiempo_acumulado, self.pos_actual_grados

        # MODO GENERACIÓN
        val_grados = 0.0
        
        t_fase = tiempo_acumulado - 0.05 
        if t_fase < 0: t_fase = 0

        if self.tipo == "Onda Senoidal":
            onda_pura = (self.amplitud_grados / 2) * (1 - math.cos(self.frecuencia * t_fase))
            val_grados = onda_pura + self.OFFSET_GRADOS

        elif self.tipo == "Onda Respiración (Rect 1/2 Onda)":
            t_ciclo = (t_fase * self.frecuencia) % (2 * math.pi)
            if t_ciclo < math.pi:
                val_grados = (self.amplitud_grados * math.sin(t_ciclo)) + self.OFFSET_GRADOS
            else:
                val_grados = self.OFFSET_GRADOS
        
        elif self.tipo == "Onda Rectificada":
             val_grados = (self.amplitud_grados * abs(math.sin(self.frecuencia * t_fase))) + self.OFFSET_GRADOS

        else:
            try:
                contexto = {
                    "t": tiempo_acumulado, 
                    "A": self.amplitud_mm_raw, 
                    "V": self.V,
                    "sin": math.sin, "cos": math.cos, "tan": math.tan,
                    "asin": math.asin, "acos": math.acos, "atan": math.atan,
                    "abs": abs, "sqrt": math.sqrt, "exp": math.exp,
                    "log": math.log, "log10": math.log10,
                    "pow": math.pow, "pi": math.pi, "e": math.e
                }
                
                resultado = eval(self.ecuacion, {"__builtins__": None}, contexto)
                val_calculado_mm = float(resultado)
                
                if val_calculado_mm < 0: val_calculado_mm = 0
                
                val_grados = (val_calculado_mm / 0.2618) + self.OFFSET_GRADOS

            except Exception as e:
                print(f"ERROR ECUACIÓN: {e}")
                val_grados = self.OFFSET_GRADOS

        self.pos_actual_grados = val_grados
        return tiempo_acumulado, self.pos_actual_grados

    def activar_retorno_a_cero(self):
        self.volviendo = True
    def esta_volviendo(self):
        return self.volviendo
    def retorno_finalizado(self):
        return self.fin_retorno
    
class GeneradorPerfil:
    def __init__(self, lista_puntos_grados, intervalo_ms=20):
        self.puntos = lista_puntos_grados
        self.intervalo_s = intervalo_ms / 1000.0
        self.max_index = len(self.puntos) - 1
        self.volviendo = False
        self.fin_retorno = False
        self.finalizado = False
        self.pos_actual_grados = 0.0
        self.OFFSET_GRADOS = 0 / 0.2618 

    def siguiente_valor(self, tiempo_acumulado):
        if self.volviendo:
            velocidad_bajada = 2.0 
            self.pos_actual_grados -= velocidad_bajada
            if self.pos_actual_grados <= self.OFFSET_GRADOS:
                self.pos_actual_grados = self.OFFSET_GRADOS
                self.fin_retorno = True
            return tiempo_acumulado, self.pos_actual_grados

        indice = int(tiempo_acumulado / self.intervalo_s)
        if indice >= self.max_index:
            self.pos_actual_grados = self.puntos[-1]
            self.finalizado = True
        else:
            self.pos_actual_grados = self.puntos[indice]
            
        return tiempo_acumulado, self.pos_actual_grados

    def activar_retorno_a_cero(self):
        self.volviendo = True
    def esta_volviendo(self):
        return self.volviendo
    def retorno_finalizado(self):
        return self.fin_retorno 
    def ha_terminado_perfil(self):
        return self.finalizado