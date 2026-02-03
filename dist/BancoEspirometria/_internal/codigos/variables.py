#_____________________________________________________________________________________________________________________
#    Nombre del Script: variables.py
#    Autor: José Alberto García Valiño
#    Fecha: 07-12-2025
#    Descripción:
#        Clase que centraliza todas las variables de estado,
#        referencias a objetos principales y buffers de datos de la aplicación.
#        Facilita el intercambio de información entre los distintos módulos (GUI, PLC,
#        Base de Datos, Lógica).
#______________________________________________________________________________________________________________________

__author__ = "José Alberto García Valiño"
__copyright__ = "Copyright 2025, José Alberto García Valiño"
__credits__ = ["José Alberto García Valiño"]
__license__ = "MIT"
__version__ = "1.0"
__email__ = "albertogarva02@gmail.com"
__status__ = "Beta"

from collections import deque
from codigos.constantes import MAX_PUNTOS_TENDENCIA

class VariablesGlobales:
    def __init__(self):
        # Referencias a Objetos
        self.base_datos = None
        self.ventana_principal = None
        self.espirometro_usb = None
        self.manejador_plc = None
        self.simulador_curva = None
        
        # Timers
        self.ansys_video_timer = None
        self.timer_plc = None

        # Variables de Estado 
        self.parada_emergencia_activa = False
        self.movimiento_activo = False
        self.movimiento_activo_previo = False
        self.tiempo_acumulado = 0.0
        self.tiempo_lampara = 0
        self.valor = False
        self.posicion_inicial = 0
        self.generar_onda = None
        self.ultimo_tipo = ""
        self.ultima_amp = 0
        self.ultima_vel = 0
        self.ultima_ecuacion = ""
        self.volviendo_a_inicio = False
        self.tiempo_antes_de_volver = 0
        self.retorno_a_cero_completado = False
        self.movimiento_volver_inicio = False
        self.indice_datos_graficados = 0
        self.simulacion_actual_graficando = None
        self.ultimo_tiempo_generado = None
        self.forzar_posicion_cero = False
        self.primer_valor_tras_cero = False
        self.datos_paciente_previos = None
        self.datos_flujo_volumen = []
        self.medida_activa = False
        self.simulacion_finalizada_naturalmente = False
        self.tiempo_primer_movimiento_fisico = None
        self.contador_error_seguimiento = 0

        # Variables Ansys
        self.ansys_frame_index_in = 0
        self.ansys_frame_index_out = 0
        self.ansys_video_active = False

        # Variables PLC
        self.plc_conectado = False
        self.calibrando_activo = False
        self.contador_glitches = 0
        self.modo_simulacion_iniciado = False
        self.s_sup = None
        self.s_inf = None

        # Variables de Gráficas y Cálculo
        self.datos_grafica_eje_t = deque(maxlen=MAX_PUNTOS_TENDENCIA)
        self.datos_grafica_posicion = deque(maxlen=MAX_PUNTOS_TENDENCIA) 
        self.datos_grafica_velocidad = deque(maxlen=MAX_PUNTOS_TENDENCIA) 
        self.datos_grafica_aceleracion = deque(maxlen=MAX_PUNTOS_TENDENCIA) 
        self.datos_grafica_sensor1 = deque(maxlen=MAX_PUNTOS_TENDENCIA)
        self.datos_grafica_sensor2 = deque(maxlen=MAX_PUNTOS_TENDENCIA)

        self.prev_posicion_mm = 0.0
        self.prev_velocidad = 0.0
        self.prev_tiempo_lectura = 0.0
        self.tiempo_inicio_grafica = 0.0

        self.posicion_real_motor = 0.0
        self.posicion_mm_consigna = 0.0 
        self.prev_volumen_consigna = 0.0
        self.prev_volumen_real = 0.0
        self.prev_tiempo_grafica_flujo = 0.0
        self.flujo_real_filtrado = 0.0 
        self.flujo_consigna_filtrado = 0.0
        self.tiempo_inicio_movimiento_motor = 0.0

        self.contador_refresco_ui = 0 
        self.contador_pintado_motor = 0