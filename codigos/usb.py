#_____________________________________________________________________________________________________________________
#    Nombre del Script: usb.py
#    Autor: José Alberto García Valiño
#    Fecha: 07-12-2025
#    Descripción:
#        Módulo de bajo nivel para la comunicación USB con espirómetros DATOSPIR.
#        Implementa algoritmos de filtrado digital (Savitzky-Golay, Butterworth),
#        detección de ciclos respiratorios, reducción de dimensionalidad (PCA) para
#        calibración y limpieza de ruido en la señal de flujo en tiempo real. 
#______________________________________________________________________________________________________________________

__author__ = "José Alberto García Valiño"
__copyright__ = "Copyright 2025, José Alberto García Valiño"
__credits__ = ["José Alberto García Valiño"]
__license__ = "MIT"
__version__ = "1.0"
__status__ = "Beta"


import pywinusb.hid as hid
from sklearn.decomposition import PCA
import numpy as np
import time
from collections import deque
from scipy.signal import medfilt, savgol_filter, butter, lfilter

class USB:
    def __init__(self, main_callback=None):
        self.__main_callback = main_callback
        self.__last_flow = None
        self.__last_valid_flow = None
        self.__diccionario = {-2.0: -1.7856068676404497, -1.75: -35.894771689582406, -1.52: -73.33565300719218, -1.5: -46.970265089213996, -1.27: -54.95181154520439, -1.26: -52.10517997741817, -1.03: -53.46812561553946, -1.02: -43.334532088969176, -0.78: -60.161081825353634, -0.77: -36.76441210241806, -0.53: -45.12393816452163, -0.52: -49.8347586491475, -0.2: -9.015009908889624, 0.0: -8.030953482258377, 0.19: -14.913791253698644, 0.51: -5.2546071758893085, 0.75: -9.430606658441265, 0.99: -13.549123207407746, 1.23: -17.64203690817353, 1.47: -17.219680796591586, 1.71: -14.662383490745425, 1.95: -9.039543134650145, 2.19: -17.052692418554383, 2.43: -16.77842952577111, 2.67: -21.450918733694913, 2.91: -23.726532880314853, 3.15: -28.896524967656863, 3.39: -26.17377257548503, 3.63: -26.790381027350204, 3.88: -28.21304102159883, 4.12: -29.0606886652721, 4.36: -21.278320863139225, 4.61: -29.701564211327817, 4.84: -25.98762680928558, 5.09: -34.01937539537192, 5.34: -36.146048035086466, 5.58: -27.514385103361473, 5.82: -24.570372836032277, 6.07: -27.77923569999838}
        self.__TOLERANCIA = 1
        self.__FLUJO_UMBRAL_DETECCION = 0.1  
        self.__UMBRAL_BAJADA_PICO = 0.1  
        self.__NUMERO_MUESTRAS_PICO = 200  
        self.__TIMEOUT_NUEVO_DATO = 0.05  
        self.__VENTANA_SUAVIZADO = 100 
        self.__VENTANA_SUAVIZADO_FUERTE = 15 
        self.__VENTANA_SAVGOL = 21        
        self.__POLYNOMIAL_SAVGOL = 3   
        self.__estado_respiracion = None  
        self.__ultimo_flujo_no_cero = None
        self.__finalizar_toma_datos = False

        self.__flujo_inicial = None
        self.__tiempo_inicio = None
        self.__volumen_acumulado = 0.0
        self.__conteo_ceros = 0

        self.__ultimo_dato_recibido = None
        self.__flujo_pendiente = None
        self.__buffer_flujos = deque(maxlen=self.__NUMERO_MUESTRAS_PICO)
        self.__pico_en_curso = False
        self.__valor_inicio_pico = None
        self.__contador_pico = 0
        self.__lista_flujos_crudos = deque(maxlen=100) 

        self.__lista_flujos_procesados = [] 
        self.__tiempo_procesado_previo = None

        self.__lista_flujos = []
        self.__tiempo_previo = None  
        self.__detener_impresion = True  
        self.__device = None
        self.__flujo_final = None
        self.__volumen_final = None
        self.__data_listeners = []  
        self.__ultimo_volumen_notificado = None
        self.__lectura_activa = False

    def conectar_y_empezar_lectura(self):
        if self.conectado():
            self.__lectura_activa = True
            self.__reiniciar_datos() 
            self.__lista_flujos_crudos = deque(maxlen=100)
            return True
        return False

    def detener_lectura(self):
        self.__lectura_activa = False

    def recibir_dato(self):
        if self.__flujo_final is not None and self.__volumen_final is not None:
            flujo = self.__flujo_final
            volumen = self.__volumen_final
            self.__flujo_final = None
            self.__volumen_final = None
            return flujo, volumen
        return None, None

    def __notify_main(self, flow, volume):
        if self.__main_callback:
            self.__main_callback(flow, volume)

    def add_data_listener(self, listener_function):
        self.__data_listeners.append(listener_function)

    def __notify_data_listeners(self, flow, volume):
        if not self.__finalizar_toma_datos and (self.__ultimo_volumen_notificado is None or abs(volume - self.__ultimo_volumen_notificado) > self.__TOLERANCIA):
            flow_cleaned = self.__limpiar_flujo(flow)
            for listener in self.__data_listeners:
                listener(flow_cleaned, volume)
            self.__ultimo_volumen_notificado = volume
            if self.__estado_respiracion == 'inspiracion' and abs(flow) < self.__TOLERANCIA:
                self.__finalizar_toma_datos = True
                print("Toma de datos finalizada por flujo cero al final de la inspiración.")

    def __generar_volumen(self, flujo, tiempo_transcurrido):
        return flujo * tiempo_transcurrido

    def remove_data_listener(self, listener_function):
        if listener_function in self.__data_listeners:
            self.__data_listeners.remove(listener_function)

    def __interpolar_clave_por_valor_faltante(self, diccionario, valor_faltante):
        pares_ordenados = sorted(diccionario.items(), key=lambda item: item[1])
        valor_menor = None
        clave_menor = None
        valor_mayor = None
        clave_mayor = None

        for clave, valor in pares_ordenados:
            if valor < valor_faltante:
                valor_menor = valor
                clave_menor = clave
            elif valor > valor_faltante:
                valor_mayor = valor
                clave_mayor = clave
                break

        if valor_menor is not None and valor_mayor is not None:
            clave_interpolada = clave_menor + (clave_mayor - clave_menor) * \
                                (valor_faltante - valor_menor) / (valor_mayor - valor_menor)
            return clave_interpolada
        else:
            return None

    def __reducir_a_un_valor_con_pca(self, data):
        if len(data) != 37:
            raise ValueError("La lista debe contener exactamente 37 elementos.")
        indices = np.arange(37)
        data_con_indices = np.column_stack((indices, data))
        pca = PCA(n_components=1)
        data_reducida = pca.fit_transform(data_con_indices)
        return data_reducida[0][0]

    def __suavizar_flujos_fuerte(self, flujos):
        if len(flujos) < self.__VENTANA_SUAVIZADO_FUERTE or self.__VENTANA_SUAVIZADO_FUERTE % 2 == 0:
            return flujos
        return medfilt(flujos, kernel_size=self.__VENTANA_SUAVIZADO_FUERTE).tolist()

    def _suavizar_flujos_savgol(self, flujos):
        if len(flujos) < self.__VENTANA_SAVGOL or self.__VENTANA_SAVGOL % 2 == 0 or self.__VENTANA_SAVGOL <= self.__POLYNOMIAL_SAVGOL:
            return flujos
        try:
            return savgol_filter(flujos, self.__VENTANA_SAVGOL, self.__POLYNOMIAL_SAVGOL).tolist()
        except ValueError:
            return flujos # Manejar errores si la ventana es demasiado pequeña

    def __filtrar_paso_bajo(self, flujos, cutoff_freq=5.0, fs=100.0, order=5):
        nyquist_freq = 0.5 * fs
        normalized_cutoff = cutoff_freq / nyquist_freq
        b, a = butter(order, normalized_cutoff, btype='low', analog=False)
        return lfilter(b, a, flujos).tolist()

    def __procesar_flujo(self, flujo_actual, tiempo_actual):
        flujo_crudo = flujo_actual
        self.__lista_flujos_crudos.append(flujo_crudo)

        flujos_suavizados = list(self.__lista_flujos_crudos)
        flujo_procesado = self._suavizar_flujos_savgol(flujos_suavizados)[-1] if flujos_suavizados else flujo_crudo

        if self.__ultimo_flujo_no_cero is not None:
            if flujo_crudo > self.__TOLERANCIA and self.__ultimo_flujo_no_cero < -self.__TOLERANCIA:
                self.__estado_respiracion = 'expiracion'
            elif flujo_crudo < -self.__TOLERANCIA and self.__ultimo_flujo_no_cero > self.__TOLERANCIA:
                self.__estado_respiracion = 'inspiracion'
        elif abs(flujo_crudo) > self.__TOLERANCIA:
            if flujo_crudo > 0:
                self.__estado_respiracion = 'expiracion'
            else:
                self.__estado_respiracion = 'inspiracion'

        flujo_para_volumen = flujo_procesado
        if self.__estado_respiracion == 'expiracion' and flujo_procesado < -self.__TOLERANCIA:
            if self.__last_valid_flow is not None and self.__last_valid_flow > 0:
                flujo_para_volumen = self.__last_valid_flow
            else:
                flujo_para_volumen = 0.0 
        elif self.__estado_respiracion == 'inspiracion' and flujo_procesado > self.__TOLERANCIA:
            if self.__last_valid_flow is not None and self.__last_valid_flow < 0:
                flujo_para_volumen = self.__last_valid_flow
            else:
                flujo_para_volumen = 0.0 
        else:
            self.__last_valid_flow = flujo_procesado 

        if self.__flujo_inicial is None and abs(
                flujo_para_volumen) > self.__FLUJO_UMBRAL_DETECCION and flujo_para_volumen < 0:
            self.__flujo_inicial = flujo_para_volumen
            self.__tiempo_inicio = tiempo_actual
            self.__volumen_acumulado = 0.0
            self.__conteo_ceros = 0
        elif self.__tiempo_inicio is not None:
            delta_t = tiempo_actual - self.__tiempo_procesado_previo if self.__tiempo_procesado_previo is not None else 0.01
            volumen_instantaneo = flujo_para_volumen * delta_t
            self.__volumen_acumulado += volumen_instantaneo
            if self.__volumen_acumulado < 0:
                self.__volumen_acumulado = 0.0

        flujo_limpio = flujo_para_volumen  
        if not self.__finalizar_toma_datos and (
                self.__last_flow is None or abs(flujo_limpio - self.__last_flow) > self.__TOLERANCIA):
            self.__flujo_final = flujo_limpio
            self.__volumen_final = self.__volumen_acumulado
            self.__notify_data_listeners(self.__flujo_final, self.__volumen_final)
            self.__notify_main(self.__flujo_final, self.__volumen_final)
            self.__last_flow = flujo_limpio

        if abs(flujo_crudo) > self.__TOLERANCIA:
            self.__ultimo_flujo_no_cero = flujo_crudo

        self.__tiempo_procesado_previo = tiempo_actual

    def __limpiar_flujo(self, flujo):
        if self.__estado_respiracion == 'inspiracion' and flujo > self.__TOLERANCIA:
            return 0.0
        elif self.__estado_respiracion == 'expiracion' and flujo < -self.__TOLERANCIA:
            return 0.0
        return flujo

    def __suavizar_flujos(self, flujos):
        if len(flujos) < self.__VENTANA_SUAVIZADO:
            return flujos
        return np.convolve(flujos, np.ones(self.__VENTANA_SUAVIZADO) / self.__VENTANA_SUAVIZADO, mode='same').tolist()

    def __detectar_y_corregir_picos(self, flujos):
        flujos_corregidos = list(flujos)
        n = len(flujos)
        for i in range(1, n - 1):
            if (flujos[i] > 0 and flujos[i - 1] < 0 and flujos[i + 1] < 0) or \
                    (flujos[i] < 0 and flujos[i - 1] > 0 and flujos[i + 1] > 0):
                tendencia = 0
                if abs(flujos[i - 1]) > abs(flujos[i + 1]):
                    tendencia = flujos[i - 1]
                else:
                    tendencia = flujos[i + 1]
                if abs(flujos[i]) < abs(tendencia) * 0.5:  
                    flujos_corregidos[i] = tendencia
        return flujos_corregidos

    def __on_data(self, data):
        if not self.__lectura_activa:
            return

        tiempo_actual = time.time()
        self.__ultimo_dato_recibido = tiempo_actual

        if self.__finalizar_toma_datos:
            return

        try:
            valor_reducido_pca = self.__reducir_a_un_valor_con_pca(list(data))
            flujo_crudo = None

            for clave, valor in self.__diccionario.items():
                if abs(valor_reducido_pca - valor) < self.__TOLERANCIA:
                    flujo_crudo = clave
                    break

            if flujo_crudo is None:
                flujo_interpolado = self.__interpolar_clave_por_valor_faltante(self.__diccionario, valor_reducido_pca)
                if flujo_interpolado is not None:
                    flujo_crudo = flujo_interpolado

            if flujo_crudo is not None:
                self.__lista_flujos.append(flujo_crudo)
                self.__flujo_pendiente = flujo_crudo  

                if self.__tiempo_previo is None or (tiempo_actual - self.__tiempo_previo) >= self.__TIMEOUT_NUEVO_DATO:
                    if self.__flujo_pendiente is not None:
                        self.__procesar_flujo(self.__flujo_pendiente, tiempo_actual)
                        self.__flujo_pendiente = None  
                        self.__tiempo_previo = tiempo_actual  

            self.__last_data = data
        except ValueError as ve:
            print(f"Error de valor en reducir_a_un_valor_con_pca: {ve}")
        except Exception as e:
            print(f"Error general en on_data: {e}")

    def conectado(self):
        try:
            all_hids = hid.find_all_hid_devices()
            datospir_device = None
            for device in all_hids:
                if device.vendor_id == 0x0483 and device.product_id == 0x5750:
                    datospir_device = device
                    break

            if datospir_device:
                print("¡Dispositivo DATOSPIR encontrado!")
                try:
                    datospir_device.open()
                    self.__device = datospir_device
                    datospir_device.set_raw_data_handler(self.__on_data)
                    return True
                except Exception as e:
                    print(f"Error al abrir el dispositivo: {e}")
                    return False
            else:
                print("Dispositivo DATOSPIR no encontrado.")
                return False
        except Exception as e:
            print(f"Error general al buscar el dispositivo: {e}")
            return False

    def __reiniciar_datos(self):
        """Reinicia las variables de estado de la toma de datos."""
        self.__estado_respiracion = None
        self.__ultimo_flujo_no_cero = None
        self.__finalizar_toma_datos = False
        self.__flujo_inicial = None
        self.__tiempo_inicio = None
        self.__volumen_acumulado = 0.0
        self.__conteo_ceros = 0
        self.__ultimo_dato_recibido = None
        self.__flujo_pendiente = None
        self.__buffer_flujos.clear()
        self.__pico_en_curso = False
        self.__valor_inicio_pico = None
        self.__contador_pico = 0
        self.__lista_flujos_crudos.clear()
        self.__lista_flujos_procesados = []
        self.__tiempo_procesado_previo = None
        self.__lista_flujos.clear()
        self.__tiempo_previo = None
        self.__flujo_final = None
        self.__volumen_final = None
        self.__ultimo_volumen_notificado = None

    def cerrar_conexion(self):
        self.detener_lectura()
        self.__reiniciar_datos()
        self.cerrar()

    def cerrar(self):
        if self.__device and self.__device.is_opened():
            self.__device.close()
            print("Conexión cerrada.")
            self.__device = None