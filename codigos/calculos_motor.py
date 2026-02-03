#_____________________________________________________________________________________________________________________
#    Nombre del Script: calculos_motor.py
#    Autor: José Alberto García Valiño
#    Fecha: 07-12-2025
#    Descripción:
#        Módulo matemático encargado de transformar las curvas de Flujo-Volumen en
#        perfiles de movimiento (Posición-Tiempo) comprensibles para el motor.
#        Realiza interpolaciones, cálculos de conversión de litros a pasos/grados
#        y gestiona la inyección de arrays de datos al PLC vía Modbus.
#______________________________________________________________________________________________________________________

__author__ = "José Alberto García Valiño"
__copyright__ = "Copyright 2025, José Alberto García Valiño"
__credits__ = ["José Alberto García Valiño"]
__license__ = "MIT"
__version__ = "1.0"
__status__ = "Beta"


import numpy as np
from codigos.generadoronda import GENERADORONDA
from codigos.constantes import (
    FACTOR_MM_A_LITROS, VOLUMEN_MAXIMO_LITROS, 
    FACTOR_LITROS_A_GRADOS, OFFSET_GRADOS_SEGURIDAD, 
    CARRERA_TOTAL_MM)

def convertir_fv_a_perfil_motor(datos_fv, resolucion_plc_ms=20):
    if not datos_fv or len(datos_fv) < 2: return [0, 0], 0
    
    volumenes = np.array([p[0] for p in datos_fv])
    flujos = np.array([p[1] for p in datos_fv])
    
    max_vol = np.max(volumenes)
    
    if max_vol > VOLUMEN_MAXIMO_LITROS:
        return [0, 0], max_vol

    tiempos = [0.0]
    
    # RECONSTRUCCIÓN DEL TIEMPO
    for i in range(1, len(volumenes)):
        vol_delta = volumenes[i] - volumenes[i-1]
        flujo_promedio = (flujos[i] + flujos[i-1]) / 2.0
        
        if abs(flujo_promedio) < 0.05: flujo_promedio = 0.05
            
        dt = vol_delta / flujo_promedio
        
        if dt < 0: dt = 0 
        if dt > 0.5: dt = 0.02 
        
        tiempos.append(tiempos[-1] + dt)
    
    tiempos = np.array(tiempos)
    posiciones_grados = volumenes * FACTOR_LITROS_A_GRADOS
    
    tiempo_total = tiempos[-1]
    if tiempo_total <= 0: return [0, 0], 0
    
    # INTERPOLACIÓN
    paso_tiempo = resolucion_plc_ms / 1000.0 
    tiempos_plc = np.arange(0, tiempo_total, paso_tiempo)
    perfil_motor = np.interp(tiempos_plc, tiempos, posiciones_grados)
    
    perfil_motor_int = []
    for p in perfil_motor:
        p_con_offset = p + OFFSET_GRADOS_SEGURIDAD
        valor = int(p_con_offset * 10)
        if valor < 0: valor = 0 
        perfil_motor_int.append(valor)

    if len(perfil_motor_int) > 2:
         perfil_motor_int[-1] = perfil_motor_int[-2]
    
    return perfil_motor_int, tiempo_total

def gestionar_inyeccion_curva(ventana, plc, es_modo_simulacion, funcion_bbdd=None):
    if not plc.conectado:
        ventana.agregar_a_log("ERROR: PLC no conectado.")
        return False
    
    try: 
        plc.escribir_perfil_db(1000, [0]*4000) 
    except Exception: pass

    lista_puntos_plc = []
    duracion_exacta_segundos = 0.0 
    PASO_TIEMPO_PLC_SEG = 0.02

    if es_modo_simulacion:
        nombre_simulacion = ventana.devolversimulacionCB()
        ventana.agregar_a_log(f"DB: Procesando '{nombre_simulacion}'...")
        
        if funcion_bbdd: datos_fv = funcion_bbdd(nombre_simulacion)
        else: return False
        
        if datos_fv:
            lista_puntos_plc, valor_retorno = convertir_fv_a_perfil_motor(datos_fv, resolucion_plc_ms=20)
            
            if len(lista_puntos_plc) <= 2 and lista_puntos_plc[0] == 0:
                 vol_solicitado = valor_retorno
                 msg_error = f"ERROR: Curva ({vol_solicitado:.2f}L) excede máximo ({VOLUMEN_MAXIMO_LITROS:.2f}L)"
                 ventana.Linfosimulacion(msg_error)
                 ventana.agregar_a_log(msg_error) 
                 return False

            duracion_exacta_segundos = valor_retorno
            ventana.agregar_a_log(f"INFO: Curva OK. T={duracion_exacta_segundos:.2f}s ({len(lista_puntos_plc)} pts).")
        else: 
            ventana.agregar_a_log("ERROR: No se recuperaron datos de la BD.")
            return False
    else:
        tipo_onda = ventana.tipomovimientomotor()
        ventana.agregar_a_log(f"MANUAL: Calculando {tipo_onda}...")
        ecuacion = ventana.valorecuacion()
        try:
            amplitud_mm = float(ventana.valoramplitud())
            velocidad_pct = float(ventana.valorvelocidad())
            if velocidad_pct <= 0: velocidad_pct = 1.0
        except:
            amplitud_mm = CARRERA_TOTAL_MM 
            velocidad_pct = 10.0
            
        generador = GENERADORONDA(amplitud_mm, velocidad_pct, tipo_onda, ecuacion)
        periodo_segundos = 100.0 / velocidad_pct
        if periodo_segundos > 60: periodo_segundos = 60
        if periodo_segundos < 0.5: periodo_segundos = 0.5
        duracion_exacta_segundos = periodo_segundos
        
        tiempos_gen = np.arange(0, periodo_segundos, PASO_TIEMPO_PLC_SEG)
        for t in tiempos_gen:
            _, pos_grados = generador.siguiente_valor(t)
            valor_puro = int(pos_grados * 10)
            if valor_puro < 0: valor_puro = 0 
            lista_puntos_plc.append(valor_puro)
        
        if not es_modo_simulacion:
            if lista_puntos_plc:
                primero = lista_puntos_plc[0]
                if primero < 0: primero = 0
                lista_puntos_plc.append(primero)
            
    if not lista_puntos_plc: 
        ventana.agregar_a_log("ERROR: La lista de puntos generada está vacía.")
        return False

    longitud_real_curva = len(lista_puntos_plc)
    
    ultimo_valor = lista_puntos_plc[-1]
    
    padding = [ultimo_valor] * 50
    lista_a_enviar = lista_puntos_plc + padding
    
    MAX_PUNTOS_PLC = 4000
    if len(lista_a_enviar) > MAX_PUNTOS_PLC:
        lista_a_enviar = lista_a_enviar[:MAX_PUNTOS_PLC]

    try:
        ventana.agregar_a_log(f"PLC: Enviando perfil...")
        DIRECCION_VR = 1000 
        
        plc.escribir_perfil_db(DIRECCION_VR, lista_a_enviar)
    
        duracion_total_ms = int(duracion_exacta_segundos * 1000)
        
        plc.escribir_registro_simple(40012, longitud_real_curva - 1)
        
        plc.escribir_registro_simple(40013, duracion_total_ms)

        modo_bucle = 1 if es_modo_simulacion else 0
        
        plc.escribir_registro_simple(40015, modo_bucle) 
        plc.escribir_registro_simple(40016, 0) 
        
        ventana.agregar_a_log(f"PLC: Sincronizado. Iniciando movimiento.")
        plc.escribir_registro_simple(40011, 99) 
        return True
    except Exception as e:
        ventana.agregar_a_log(f"ERROR CRÍTICO Modbus: {e}")
        return False