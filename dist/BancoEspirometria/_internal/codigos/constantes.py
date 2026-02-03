#_____________________________________________________________________________________________________________________
#    Nombre del Script: constantes.py
#    Autor: José Alberto García Valiño
#    Fecha: 07-12-2025
#    Descripción:
#        Archivo central de configuración. Define:
#            1. Parámetros físicos del banco (diámetros, carreras, factores de conversión).
#            2. Configuración de bucles de control y límites de seguridad.
#            3. Diccionarios de definiciones para patologías respiratorias y sus factores de curva.
#______________________________________________________________________________________________________________________

__author__ = "José Alberto García Valiño"
__copyright__ = "Copyright 2025, José Alberto García Valiño"
__credits__ = ["José Alberto García Valiño"]
__license__ = "MIT"
__version__ = "1.0"
__email__ = "albertogarva02@gmail.com"
__status__ = "Beta"

import math

# CONFIGURACIÓN GENERAL
LIMITE_BASE_MM = 20.0 
TIEMPO_GRACIA_INICIAL_S = 3.0
ANSYS_MAX_FRAME_IN = 199 
ANSYS_MAX_FRAME_OUT = 99
ANSYS_LOOP_START_IN = 149 
ANSYS_LOOP_START_OUT = 49
ANSYS_BASE_INTERVAL_MS = 100 
MAX_PUNTOS_TENDENCIA = 400

# CONSTANTES FÍSICAS (MOTOR Y CILINDRO)
PLC_ESPERA_GRADOS = True 
DIAMETRO_PINON_MM = 30.0       
CARRERA_TOTAL_MM = 345.0     
DIAMETRO_CILINDRO_MM = 100.0   
NUMERO_CILINDROS = 2

# Cálculos de Conversión (Estáticos) 
RADIO_METROS = (DIAMETRO_CILINDRO_MM / 1000.0) / 2 
AREA_UNO_M2 = math.pi * (RADIO_METROS ** 2)
AREA_TOTAL_M2 = AREA_UNO_M2 * NUMERO_CILINDROS

# FACTOR: 1 mm de avance * Area (m2) = Volumen en Litros
FACTOR_MM_A_LITROS = AREA_TOTAL_M2 

# Volumen máximo físico del sistema
VOLUMEN_MAXIMO_LITROS = CARRERA_TOTAL_MM * FACTOR_MM_A_LITROS

PERIMETRO_PINON = math.pi * DIAMETRO_PINON_MM  
VUELTAS_TOTALES = CARRERA_TOTAL_MM / PERIMETRO_PINON 
GRADOS_TOTALES = VUELTAS_TOTALES * 360.0     

# Factor: Grados por Litro
_divisor_grados = (CARRERA_TOTAL_MM * FACTOR_MM_A_LITROS)
if _divisor_grados == 0: _divisor_grados = 1
FACTOR_LITROS_A_GRADOS = GRADOS_TOTALES / _divisor_grados

OFFSET_GRADOS_SEGURIDAD = 0.0 

# CONFIGURACIÓN SIMULACIÓN CURVA
SIM_N_PUNTOS = 1000        
SIM_TIEMPO_TOTAL = 6.0   
SIM_TIEMPO_SUBIDA = 0.10  
SIM_TAU_BASE = 0.65       


# GRUPOS DE PATOLOGÍAS
PATOLOGIAS_OBS_LEVES = ["Asma", "Bronquitis Crónica", "Bronquiectasias"]
PATOLOGIAS_OBS_SEVERAS = ["EPOC", "Enfisema", "Fibrosis Quística"]
PATOLOGIAS_RESTRICTIVAS = ["Restrictiva", "Fibrosis Pulmonar", "Cifoescoliosis", "Neumotórax", "Neumonía"]
PATOLOGIAS_EXTRINSECAS = ["Obesidad Mórbida", "Enfermedad Neuromuscular"]
PATOLOGIAS_MIXTAS = ["Sarcoidosis", "Tuberculosis", "Cáncer de Pulmón"]


# DICCIONARIO DE FACTORES
# Clave: Nombre Patología
# Valor: (Factor_FVC, Factor_PEF, K_Concavidad)
# K_Concavidad: 1.0=Recto, >1.0=Cóncavo (Obstrucción), <1.0=Convexo (Restricción)
CONFIG_PATOLOGIAS = {
    # Sano / Defecto
    "Ninguna":              (1.00, 1.00, 1.0),
    
    # Obstructivas Leves/Moderadas
    "Asma":                 (0.92, 0.70, 3.0),
    "Bronquitis Crónica":   (0.92, 0.70, 3.0),
    "Bronquiectasias":      (0.92, 0.70, 3.0),
    
    # Obstructivas Severas 
    "EPOC":                 (0.80, 0.50, 5.5),
    "Enfisema":             (0.80, 0.50, 5.5),
    "Fibrosis Quística":    (0.80, 0.50, 5.5),
    
    # Restrictivas (Pulmón Rígido)
    "Restrictiva":          (0.55, 0.60, 0.8),
    "Fibrosis Pulmonar":    (0.55, 0.60, 0.8),
    "Cifoescoliosis":       (0.55, 0.60, 0.8),
    "Neumotórax":           (0.55, 0.60, 0.8),
    "Neumonía":             (0.55, 0.60, 0.8),
    
    # Restrictivas Extrínsecas
    "Obesidad Mórbida":     (0.70, 0.75, 1.0),
    "Enfermedad Neuromuscular": (0.70, 0.75, 1.0),
    
    # Mixtas / Complejas 
    "Sarcoidosis":          (0.75, 0.60, 2.5),
    "Tuberculosis":         (0.75, 0.60, 2.5),
    "Cáncer de Pulmón":     (0.75, 0.60, 2.5),
    
    # Transitorias
    "Gripe":                (0.95, 0.90, 1.1)
}