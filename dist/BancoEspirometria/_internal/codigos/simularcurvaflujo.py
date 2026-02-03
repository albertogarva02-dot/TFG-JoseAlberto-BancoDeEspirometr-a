#_____________________________________________________________________________________________________________________
#    Nombre del Script: simularcurvaflujo.py
#    Autor: José Alberto García Valiño
#    Fecha: 07-12-2025
#    Descripción:
#        Genera curvas de Flujo-Volumen basadas en
#        modelos fisiológicos reales (ecuaciones NHANES III). Permite simular diferentes
#        patologías respiratorias (EPOC, Asma, Restricción) aplicando factores de corrección
#        y deformación a las curvas teóricas según edad, sexo, altura y condición del paciente.
#______________________________________________________________________________________________________________________

__author__ = "José Alberto García Valiño"
__copyright__ = "Copyright 2025, José Alberto García Valiño"
__credits__ = ["José Alberto García Valiño"]
__license__ = "MIT"
__version__ = "1.0"
__email__ = "albertogarva02@gmail.com"
__status__ = "Beta"


import math
import numpy as np
from codigos.constantes import (
    SIM_N_PUNTOS, SIM_TIEMPO_TOTAL, SIM_TIEMPO_SUBIDA, SIM_TAU_BASE,
    CONFIG_PATOLOGIAS)

class SIMULARCURVAFLUJO:
    def __init__(self, ventana_principal, timer):
        self.__ventana_principal = ventana_principal
        self.__timer = timer
        
        self.__datos_flujo = []
        self.__indice_dato = 0
        self.__simulacion_terminada = False
        self.__volumenes_completos = []
        self.__flujos_completos = []
        self.__datos_simulacion_guardar = []
        
        self.__datos_paciente = None
        self.__fvc_predicho = None
        self.__fev1_predicho = None
        self.__pef_predicho = None
        
        self.__fvc_real_simulado = 0
        self.__fev1_real_simulado = 0
        self.__pef_real_simulado = 0

    def recibir_datos_paciente(self, edad, altura, fumador, sexo, peso, patologia="Ninguna"):
        try:
            val_edad = float(edad)
            val_altura = float(altura)
        except ValueError:
            return

        self.__datos_paciente = {
            'edad': val_edad, 
            'altura': val_altura, 
            'fumador': fumador, 
            'sexo': sexo, 
            'peso': peso,
            'patologia': patologia 
        }
        
        self.__calcular_predichos_nhanes()
        self.__generar_curva_fisiologica()
        
        # Reset para animación
        self.__indice_dato = 0
        self.__simulacion_terminada = False
        self.__volumenes_completos = []
        self.__flujos_completos = []
        self.__datos_simulacion_guardar = []
        self.__timer.start(6) 

    def __calcular_predichos_nhanes(self):
        edad = max(18, min(90, self.__datos_paciente['edad']))
        altura = self.__datos_paciente['altura']
        sexo = self.__datos_paciente['sexo']
        
        if sexo == 'Hombre':
            self.__fvc_predicho = -0.1933 + (0.00064*edad) - (0.000269*(edad**2)) + (0.00018642*(altura**2))
            self.__fev1_predicho = 0.5536 - (0.01303*edad) - (0.000172*(edad**2)) + (0.00014098*(altura**2))
            pef = 0.6161 - (0.02511*edad) + (0.0000606*(edad**2)) + (0.00034337*(altura**2))
        else: 
            self.__fvc_predicho = -0.3560 + (0.01870*edad) - (0.000382*(edad**2)) + (0.00014815*(altura**2))
            self.__fev1_predicho = 0.4333 - (0.00361*edad) - (0.000194*(edad**2)) + (0.00011496*(altura**2))
            pef = 0.9267 - (0.02110*edad) + (0.0000318*(edad**2)) + (0.00022300*(altura**2))

        self.__pef_predicho = max(3.0, pef)
        self.__fvc_predicho = max(2.0, self.__fvc_predicho)
        self.__fev1_predicho = max(1.5, self.__fev1_predicho)
        
        if self.__fev1_predicho > self.__fvc_predicho:
            self.__fev1_predicho = self.__fvc_predicho * 0.85

    def __generar_curva_fisiologica(self):
        self.__datos_flujo = []
        
        es_fumador = (self.__datos_paciente['fumador'] == 'SI')
        patologia_nombre = self.__datos_paciente['patologia']
        
        factores = CONFIG_PATOLOGIAS.get(patologia_nombre, CONFIG_PATOLOGIAS["Ninguna"])
        
        factor_fvc_pat = factores[0]
        factor_pef_pat = factores[1]
        k_concavidad = factores[2]

        # Ajuste por Fumador
        factor_fvc_fumador = 0.95 if es_fumador else 1.0
        factor_pef_fumador = 0.85 if es_fumador else 1.0
        k_concavidad = 1.3 if (es_fumador and k_concavidad == 1.0) else k_concavidad

        target_fvc = self.__fvc_predicho * factor_fvc_pat * factor_fvc_fumador
        target_pef = self.__pef_predicho * factor_pef_pat * factor_pef_fumador
        
        dt = SIM_TIEMPO_TOTAL / SIM_N_PUNTOS
        
        datos_espiracion = []
        vol_acumulado = 0.0
        
        for i in range(SIM_N_PUNTOS):
            t = i * dt
            flujo = 0.0 
            
            if t <= SIM_TIEMPO_SUBIDA:
                # FASE 1: SUBIDA
                flujo = target_pef * (t / SIM_TIEMPO_SUBIDA)
                vol_acumulado = 0.5 * flujo * t
            else:
                # FASE 2: BAJADA
                t_eff = t - SIM_TIEMPO_SUBIDA
                decay = math.exp(-t_eff / (SIM_TAU_BASE / k_concavidad))
                flujo = target_pef * decay
                
                dv = flujo * dt
                vol_acumulado += dv
                
                if vol_acumulado > target_fvc:
                    vol_acumulado = target_fvc
                    flujo = 0
            
            # Captura FEV1 al segundo 1.0
            if abs(t - 1.0) < dt: 
                self.__fev1_real_simulado = vol_acumulado

            datos_espiracion.append((vol_acumulado, max(0, flujo)))
            
        self.__fvc_real_simulado = datos_espiracion[-1][0]
        self.__pef_real_simulado = max(f for v, f in datos_espiracion)
        self.__datos_flujo.extend(datos_espiracion)

        # FASE 3: INSPIRACIÓN
        n_insp = int(SIM_N_PUNTOS / 2)
        pif = self.__pef_real_simulado * 0.75
        
        for i in range(n_insp):
            p = i / (n_insp - 1)
            vol = self.__fvc_real_simulado * (1 - p)
            flujo = -pif * math.sin(p * math.pi)
            self.__datos_flujo.append((vol, flujo))

    def simulargrafica(self):
        if not self.__simulacion_terminada and self.__datos_flujo:
            if self.__indice_dato == 0:
                self.__ventana_principal.limpiarGraficaMedidas()
                self.__volumenes_completos = []
                self.__flujos_completos = []

            for _ in range(5):
                if self.__indice_dato < len(self.__datos_flujo):
                    v, f = self.__datos_flujo[self.__indice_dato]
                    self.__ventana_principal.meteDatosGraficaMedidas(v, f)
                    self.__volumenes_completos.append(v)
                    self.__flujos_completos.append(f)
                    self.__datos_simulacion_guardar.append((v, f))
                    self.__indice_dato += 1
                else:
                    self.__simulacion_terminada = True
                    self.__calcular_y_mostrar_valores()
                    self.__timer.stop()
                    break
        elif not self.__datos_flujo:
             self.__timer.stop()

    def __calcular_y_mostrar_valores(self):
        fvc = self.__fvc_real_simulado
        fev1 = self.__fev1_real_simulado
        pef = self.__pef_real_simulado
        ratio = (fev1 / fvc * 100) if fvc > 0 else 0
        
        self.__ventana_principal.valorLfvc(round(fvc, 2))
        self.__ventana_principal.valorLfev1(round(fev1, 2))
        self.__ventana_principal.valorLpef(round(pef, 2))
        self.__ventana_principal.valorLfev1_fvc(round(ratio, 2))
        self.__ventana_principal.valorLic(round(fvc, 2))

    def obtener_datos_simulacion(self):
        return self.__datos_simulacion_guardar