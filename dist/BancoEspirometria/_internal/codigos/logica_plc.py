#_____________________________________________________________________________________________________________________
#    Nombre del Script: logica_plc.py
#    Autor: José Alberto García Valiño
#    Fecha: 07-12-2025
#    Descripción:
#        Conecta la interfaz de usuario con el driver Modbus.
#        Maneja los hilos de lectura, interpreta los estados del autómata,
#        monitoriza alarmas (finales de carrera, errores) y traduce las órdenes de la GUI
#        en comandos de escritura para el PLC.
#______________________________________________________________________________________________________________________

__author__ = "José Alberto García Valiño"
__copyright__ = "Copyright 2025, José Alberto García Valiño"
__credits__ = ["José Alberto García Valiño"]
__license__ = "MIT"
__version__ = "1.0"
__email__ = "albertogarva02@gmail.com"
__status__ = "Beta"

import time
from codigos.calculos_motor import FACTOR_MM_A_LITROS
from codigos.constantes import TIEMPO_GRACIA_INICIAL_S, LIMITE_BASE_MM
from codigos.logica_video import resetear_video_ansys
from codigos.logica_db import generar_nombre_unico_prueba

def configurar_defaults_plc(vars):
    vars.ventana_principal.configurar_tabla_monitor_defaults()
    vars.ventana_principal.actualizar_estado_conexion(False)
    vars.ventana_principal.agregar_a_log("SISTEMA: Aplicación iniciada. Listo.")

def conectar_plc(vars, ip, puerto_str): 
    try:
        mensaje_exito = vars.manejador_plc.conectar(ip, puerto_str)
        vars.plc_conectado = True
        vars.ventana_principal.actualizar_estado_conexion(True)
        vars.ventana_principal.agregar_a_log(f"PLC: {mensaje_exito}")
        vars.ventana_principal.actualizar_lamparas_inicio(True)
        vars.datos_grafica_eje_t.clear()
        vars.datos_grafica_posicion.clear()
        vars.datos_grafica_velocidad.clear()
        vars.datos_grafica_aceleracion.clear()
        vars.datos_grafica_sensor1.clear()
        vars.datos_grafica_sensor2.clear()
        vars.prev_posicion_mm = 0.0
        vars.prev_velocidad = 0.0
        vars.prev_tiempo_lectura = 0.0
        vars.tiempo_inicio_grafica = time.time()
        vars.timer_plc.start(40) 
    except Exception as e:
        vars.plc_conectado = False
        vars.ventana_principal.actualizar_estado_conexion(False)
        vars.ventana_principal.agregar_a_log(f"ERROR PLC: {str(e)}")
        vars.ventana_principal.actualizar_lamparas_inicio(False)

def desconectar_plc(vars):
    vars.timer_plc.stop() 
    mensaje = vars.manejador_plc.desconectar()
    vars.plc_conectado = False
    vars.ventana_principal.actualizar_estado_conexion(False)
    vars.ventana_principal.agregar_a_log(f"PLC: {mensaje}")
    vars.ventana_principal.actualizar_lamparas_inicio(False)
    vars.ventana_principal.Lsensor1(False, False)
    vars.ventana_principal.Lsensor2(False, False)

def escribir_en_plc(vars, registro_str, valor_str):
    try:
        registro_num = int(registro_str.split('(')[1].replace(')', ''))
        valor_int = int(valor_str)
        mensaje_exito = vars.manejador_plc.escribir_registro_simple(registro_num, valor_int)
        vars.ventana_principal.agregar_a_log(f"PLC WRITE: {mensaje_exito}")
        vars.ventana_principal.limpiar_campo_escritura()
    except Exception as e:
        vars.ventana_principal.agregar_a_log(f"ERROR Escribir PLC: {str(e)}")

def ejecutar_calibracion_plc(vars):
    if not vars.plc_conectado:
        vars.ventana_principal.Linfoanadireliminardatos("Error: PLC no conectado. No se puede calibrar.")
        return
    try:
        vars.ventana_principal.agregar_a_log("CALIBRACIÓN: Iniciando secuencia...")
        vars.calibrando_activo = True
        vars.manejador_plc.escribir_registro_simple(40016, 1)
        vars.ventana_principal.agregar_a_log("CALIBRACIÓN: Orden enviada. Esperando sensor...")
    except Exception as e:
        vars.ventana_principal.agregar_a_log(f"ERROR Calibración: {str(e)}")

def actualizar_grafica_tendencia(vars, indice=-1):
    if indice == -1:
        idx = vars.ventana_principal.obtener_variable_tendencia_idx()
    else: 
        idx = indice
        
    if idx == 0: 
        vars.ventana_principal.limpiar_grafica_tendencia()
        return
        
    datos_serie_y = []
    titulo_eje_y = ""      
    titulo_grafica = ""
    titulo_eje_x = "Tiempo [s]" 
    
    if idx == 1: 
        datos_serie_y = list(vars.datos_grafica_posicion)
        titulo_grafica = "Evolución de Posición"
        titulo_eje_y = "Posición [mm]"
    elif idx == 2:
        datos_serie_y = list(vars.datos_grafica_velocidad)
        titulo_grafica = "Evolución de Velocidad"
        titulo_eje_y = "Velocidad [mm/s]"
    elif idx == 3:
        datos_serie_y = list(vars.datos_grafica_aceleracion)
        titulo_grafica = "Evolución de Aceleración"
        titulo_eje_y = "Aceleración [mm/s²]"
    elif idx == 4:
        datos_serie_y = list(vars.datos_grafica_sensor1)
        titulo_grafica = "Estado Sensor Superior"
        titulo_eje_y = "Lógico (0/1)"
    elif idx == 5:
        datos_serie_y = list(vars.datos_grafica_sensor2)
        titulo_grafica = "Estado Sensor Inferior"
        titulo_eje_y = "Lógico (0/1)"
    else:
        vars.ventana_principal.limpiar_grafica_tendencia()
        return

    vars.ventana_principal.actualizar_grafica_tendencia(
        list(vars.datos_grafica_eje_t), 
        datos_serie_y, 
        titulo_grafica, 
        titulo_eje_y,
        titulo_eje_x  
    )

def leer_datos_plc_en_bucle(vars):
    if not vars.plc_conectado:
        vars.ventana_principal.Lsensor1(False, False)
        vars.ventana_principal.Lsensor2(False, False)
        return

    try:
        datos = vars.manejador_plc.leer_registros_entrada(0, 11)
        
        vars.s_sup = bool(datos[1])
        vars.s_inf = bool(datos[2])

        if (vars.s_sup or vars.s_inf) and not vars.calibrando_activo:
            vars.ventana_principal.agregar_a_log("¡PELIGRO! Sensor final de carrera activado. PARADA DE EMERGENCIA.")
            if vars.movimiento_activo:
                vars.ventana_principal.BdetenermovimientoClick()
            vars.ventana_principal.Lsensor1(vars.s_sup, True)
            vars.ventana_principal.Lsensor2(vars.s_inf, True)
            desconectar_plc(vars) 
            return 

        raw_grados_real = datos[0]
        if raw_grados_real > 32767: raw_grados_real -= 65536
        posicion_mm_leida = (raw_grados_real / 10.0) * 0.2618

        salto = abs(posicion_mm_leida - vars.prev_posicion_mm)
        if salto > 40.0 and vars.prev_posicion_mm > 1.0:
            vars.contador_glitches += 1
            if vars.contador_glitches > 5:
                  posicion_mm_real = posicion_mm_leida
                  vars.contador_glitches = 0 
            else:
                  posicion_mm_real = vars.prev_posicion_mm 
        else:
            posicion_mm_real = posicion_mm_leida
            vars.contador_glitches = 0 
        
        vars.posicion_real_motor = posicion_mm_real

        raw_grados_consigna = datos[5]
        if raw_grados_consigna > 32767: raw_grados_consigna -= 65536
        nuevo_pos_consigna = (raw_grados_consigna / 10.0) * 0.2618
        vars.posicion_mm_consigna = nuevo_pos_consigna

        estado_marcha_plc = datos[10]
        
        # MONITORIZACIÓN ESTADO PLC 
        if vars.movimiento_activo and not vars.volviendo_a_inicio:
            if estado_marcha_plc == 0:
                vars.simulacion_finalizada_naturalmente = True 
                vars.ventana_principal.agregar_a_log("PLC: Ciclo finalizado por el autómata.")
                vars.ventana_principal.BdetenermovimientoClick() 

        # MONITORIZACIÓN DE RETORNO 
        if vars.volviendo_a_inicio:
            if posicion_mm_real < 1.0: 
                vars.volviendo_a_inicio = False
                vars.movimiento_activo = False 
                vars.ventana_principal.informacion_control_motor("Motor detenido en posición HOME.")
                vars.ventana_principal.agregar_a_log("CICLO: Completado. Motor en posición inicial.")
                vars.ventana_principal.restablecer_controles_motor()
                
                #NOMBRE AL FINALIZAR RETORNO PLC 
                nombre_base = vars.simulacion_actual_graficando if vars.modo_simulacion_iniciado else "Prueba_Manual"
                if not nombre_base or nombre_base == " ": nombre_base = "Prueba_Manual"
                
                sugerencia = generar_nombre_unico_prueba(vars, nombre_base)
                vars.ventana_principal.set_nombre_prueba_sugerido(sugerencia)
                vars.ventana_principal.activar_boton_guardar_prueba(True)
                vars.ventana_principal.Linfoanadireliminardatos("Ciclo PLC fin. Puede guardar.")

                try: resetear_video_ansys(vars) 
                except: pass
            
            elif estado_marcha_plc == 0 and posicion_mm_real >= 1.0:
                  try:
                    vars.manejador_plc.escribir_registro_simple(40011, 50)
                    vars.ventana_principal.informacion_control_motor("Enviando orden retorno (50)...")
                  except: pass

        if vars.movimiento_activo and not vars.volviendo_a_inicio:
            tiempo_desde_inicio = time.time() - vars.tiempo_inicio_movimiento_motor
            if tiempo_desde_inicio > TIEMPO_GRACIA_INICIAL_S:
                try:
                    vel_usuario = float(vars.ventana_principal.valorvelocidad())
                except:
                    vel_usuario = 10.0
                
                limite_dinamico = LIMITE_BASE_MM + (vel_usuario * 0.8)
                error_seguimiento = abs(vars.posicion_mm_consigna - posicion_mm_real)
                
                if error_seguimiento > limite_dinamico:
                    vars.contador_error_seguimiento += 1
                else:
                    vars.contador_error_seguimiento = 0
                
                if vars.contador_error_seguimiento > 5:
                    vars.ventana_principal.agregar_a_log(f"ALARMA: Desvío excesivo ({error_seguimiento:.1f}mm). Parando.")
                    vars.ventana_principal.BdetenermovimientoClick()
                    try:
                        vars.manejador_plc.escribir_registro_simple(40011, 0)
                    except: pass
                    vars.contador_error_seguimiento = 0
            else:
                vars.contador_error_seguimiento = 0

        tiempo_actual_absoluto = time.time()
        if vars.tiempo_inicio_grafica == 0:
            vars.tiempo_inicio_grafica = tiempo_actual_absoluto
        
        tiempo_grafica = tiempo_actual_absoluto - vars.tiempo_inicio_grafica
        dt = tiempo_actual_absoluto - vars.prev_tiempo_lectura
        
        if dt > 0.5: dt = 0.04 

        velocidad_inst = 0.0
        aceleracion_inst = 0.0
        flujo_real = 0.0
        flujo_consigna = 0.0

        if dt > 0 and vars.prev_tiempo_lectura > 0:
            velocidad_inst = (posicion_mm_real - vars.prev_posicion_mm) / dt
            aceleracion_inst = (velocidad_inst - vars.prev_velocidad) / dt
            
            vol_real_L = posicion_mm_real * FACTOR_MM_A_LITROS
            vol_consigna_L = vars.posicion_mm_consigna * FACTOR_MM_A_LITROS
            
            if dt > 0.001:
                flujo_real = (vol_real_L - vars.prev_volumen_real) / dt
                flujo_consigna = (vol_consigna_L - vars.prev_volumen_consigna) / dt
            
            vars.prev_volumen_real = vol_real_L
            vars.prev_volumen_consigna = vol_consigna_L

        vars.prev_tiempo_lectura = tiempo_actual_absoluto
        vars.prev_posicion_mm = posicion_mm_real
        vars.prev_velocidad = velocidad_inst
        
        t_ataque_real = 0.0
        
        if vars.tiempo_primer_movimiento_fisico is None:
            if abs(velocidad_inst) > 5.0: 
                vars.tiempo_primer_movimiento_fisico = tiempo_actual_absoluto
                t_ataque_real = 0.001 
            else:
                t_ataque_real = 0.0 
        else:
            t_ataque_real = tiempo_actual_absoluto - vars.tiempo_primer_movimiento_fisico
        
        diferencia = abs(flujo_real - vars.flujo_real_filtrado)

        if t_ataque_real > 0 and t_ataque_real < 0.25:
            alpha = 0.95 
        
        elif t_ataque_real >= 0.5 and t_ataque_real < 1:
            alpha = 0.2 + (diferencia * 0.15)
            if alpha > 0.5: alpha = 0.5

        else:
            if vars.tiempo_primer_movimiento_fisico is None:
                alpha = 1.0 
            else:
                alpha = 0.08 + (diferencia * 0.1)
                if alpha > 0.25: alpha = 0.25
        
        vars.flujo_real_filtrado = (vars.flujo_real_filtrado * (1 - alpha)) + (flujo_real * alpha)
        vars.flujo_consigna_filtrado = (vars.flujo_consigna_filtrado * (1 - alpha)) + (flujo_consigna * alpha)
        
        vars.datos_grafica_eje_t.append(tiempo_grafica)
        vars.datos_grafica_posicion.append(posicion_mm_real)
        vars.datos_grafica_velocidad.append(velocidad_inst)
        vars.datos_grafica_aceleracion.append(aceleracion_inst)
        vars.datos_grafica_sensor1.append(1 if vars.s_sup else 0)
        vars.datos_grafica_sensor2.append(1 if vars.s_inf else 0)

        vars.contador_refresco_ui += 1
        if vars.contador_refresco_ui >= 5:
            datos_tabla = [
                f"{posicion_mm_real:.1f} mm",
                "ON" if vars.s_sup else "OFF",
                "ON" if vars.s_inf else "OFF",
                "Moviendo" if datos[3] else "Parado",
                str(datos[4])
            ]
            vars.ventana_principal.actualizar_tabla_monitor(datos_tabla)
            
            estado_texto = "Retornando..." if vars.volviendo_a_inicio else f"Error: {abs(vars.posicion_mm_consigna - posicion_mm_real):.1f}mm"
            if vars.movimiento_activo and not vars.volviendo_a_inicio and (time.time() - vars.tiempo_inicio_movimiento_motor < TIEMPO_GRACIA_INICIAL_S):
                    estado_texto = "Alineando..."

            vars.ventana_principal.informacion_control_motor(
                f"T: {tiempo_grafica:.2f}s | Pos: {posicion_mm_real:.1f}mm | {estado_texto}")
            
            vars.contador_refresco_ui = 0
        
        vars.ventana_principal.Lsensor1(vars.s_sup, vars.plc_conectado)
        vars.ventana_principal.Lsensor2(vars.s_inf, vars.plc_conectado)
        
        actualizar_grafica_tendencia(vars)
        
        if vars.movimiento_activo:
            vars.contador_pintado_motor += 1
            
            if vars.contador_pintado_motor % 4 == 0:
                vars.ventana_principal.meteDatosGraficaMotor(tiempo_grafica, vars.posicion_mm_consigna, posicion_mm_real)
                vars.ventana_principal.movimientopistones(posicion_mm_real)
            
            if not vars.volviendo_a_inicio:
                vars.ventana_principal.meteDatosGraficaSimulacion_flujo_volumen(
                    vars.posicion_mm_consigna * FACTOR_MM_A_LITROS, vars.flujo_consigna_filtrado, 
                    posicion_mm_real * FACTOR_MM_A_LITROS, vars.flujo_real_filtrado
                )
                vars.ventana_principal.meteDatosGraficaSimulacion_volumen_tiempo(
                    tiempo_grafica, vars.posicion_mm_consigna * FACTOR_MM_A_LITROS,
                    tiempo_grafica, posicion_mm_real * FACTOR_MM_A_LITROS
                )

    except Exception as e:
        print(f"Error ciclo PLC: {e}")
        vars.ventana_principal.Lsensor1(False, False)
        vars.ventana_principal.Lsensor2(False, False)