#_____________________________________________________________________________________________________________________
#    Nombre del Script: logica_motor.py
#    Autor: José Alberto García Valiño
#    Fecha: 07-12-2025
#    Descripción:
#        Lógica que gobierna el comportamiento del motor.
#        Coordina la generación de trayectorias (manuales o basadas en simulaciones),
#        gestiona el bucle de control principal, supervisa errores de seguimiento,
#        maneja paradas de emergencia y sincroniza la animación visual con el movimiento físico.
#______________________________________________________________________________________________________________________

__author__ = "José Alberto García Valiño"
__copyright__ = "Copyright 2025, José Alberto García Valiño"
__credits__ = ["José Alberto García Valiño"]
__license__ = "MIT"
__version__ = "1.0"
__status__ = "Beta"


import time
import gc
from codigos.calculos_motor import gestionar_inyeccion_curva, FACTOR_MM_A_LITROS, convertir_fv_a_perfil_motor
from codigos.generadoronda import GENERADORONDA, GeneradorPerfil
from codigos.constantes import ANSYS_BASE_INTERVAL_MS
from codigos.logica_video import resetear_video_ansys
from codigos.logica_db import obtener_datos_simulacion_por_nombre, generar_nombre_unico_prueba

def generargraficamotor(vars):
    if vars.parada_emergencia_activa:
        return

    debe_realizar_movimiento = vars.ventana_principal.valor_realizar_movimiento()
    nombre_simulacion = vars.ventana_principal.devolversimulacionCB()

    velocidad_ref = float(vars.ventana_principal.valorvelocidad() or 10)
    if velocidad_ref <= 0: velocidad_ref = 1
    nuevo_intervalo_ms = int(ANSYS_BASE_INTERVAL_MS / (velocidad_ref / 10.0))
    if nuevo_intervalo_ms < 15: nuevo_intervalo_ms = 15

    if debe_realizar_movimiento and not vars.movimiento_activo:
        
        vars.simulacion_finalizada_naturalmente = False 
        
        vars.calibrando_activo = False
        vars.ventana_principal.limpiarGraficaMotor()
        vars.ventana_principal.limpiaGraficaSimulacion_flujo_volumen()
        vars.ventana_principal.limpiarGraficaSimulacion_volumen_tiempo()
        vars.ventana_principal.limpiar_grafica_tendencia() 
        vars.datos_grafica_eje_t.clear()                   
        vars.datos_grafica_posicion.clear()                
        vars.datos_grafica_velocidad.clear()
        vars.datos_grafica_aceleracion.clear()
        vars.datos_grafica_sensor1.clear()
        vars.datos_grafica_sensor2.clear()
        gc.collect() 
        
        vars.prev_posicion_mm = vars.posicion_real_motor 
        vars.prev_volumen_real = vars.posicion_real_motor * FACTOR_MM_A_LITROS
        
        vars.prev_volumen_consigna = vars.posicion_mm_consigna * FACTOR_MM_A_LITROS 
        
        vars.prev_tiempo_grafica_flujo = 0.0
        vars.flujo_real_filtrado = 0.0
        vars.flujo_consigna_filtrado = 0.0
        vars.tiempo_inicio_grafica = 0.0 
        
        vars.contador_pintado_motor = 0
        
        vars.modo_simulacion_iniciado = vars.ventana_principal.esta_en_modo_simulacion()

        if vars.plc_conectado:
            # Función auxiliar wrapper para pasar variables
            def _obtener_datos_wrapper(nombre):
                return obtener_datos_simulacion_por_nombre(vars, nombre)

            exito = gestionar_inyeccion_curva(
                vars.ventana_principal, 
                vars.manejador_plc, 
                vars.modo_simulacion_iniciado, 
                _obtener_datos_wrapper
            )
            if not exito:
                vars.ventana_principal.BdetenermovimientoClick()
                vars.ventana_principal.restablecer_controles_motor()
                vars.movimiento_activo = False
                vars.simulacion_actual_graficando = None
                return
            vars.ventana_principal.agregar_a_log(f"MOVIMIENTO: Iniciado (PLC). Simulación: {nombre_simulacion if vars.modo_simulacion_iniciado else 'Manual'}")
        
        else: 
            if vars.modo_simulacion_iniciado:
                vars.ventana_principal.agregar_a_log(f"MOVIMIENTO: Iniciado (Offline). Simulación: {nombre_simulacion}")
                vars.ventana_principal.Linfosimulacion(f"SIMULANDO (OFFLINE): {nombre_simulacion}")
                datos_fv = obtener_datos_simulacion_por_nombre(vars, nombre_simulacion)
                if datos_fv:
                    perfil_grados_x10, _ = convertir_fv_a_perfil_motor(datos_fv)
                    if not perfil_grados_x10 or (len(perfil_grados_x10) <= 2 and perfil_grados_x10[0] == 0):
                        vars.ventana_principal.Linfoanadireliminardatos("Error: Curva excede capacidad física o es inválida.")
                        vars.ventana_principal.BdetenermovimientoClick()
                        vars.ventana_principal.restablecer_controles_motor()
                        vars.movimiento_activo = False
                        return
                    
                    perfil_grados_reales = [val / 10.0 for val in perfil_grados_x10]
                    vars.generar_onda = GeneradorPerfil(perfil_grados_reales)
                else:
                    vars.ventana_principal.BdetenermovimientoClick()
                    return
            else:
                vars.ventana_principal.agregar_a_log("MOVIMIENTO: Iniciado (Offline). Manual.")
                vars.ventana_principal.Linfosimulacion("MANUAL (OFFLINE).")
                tipo_onda = vars.ventana_principal.tipomovimientomotor()
                try:
                    amplitud = float(vars.ventana_principal.valoramplitud())
                    velocidad = float(vars.ventana_principal.valorvelocidad())
                except: amplitud, velocidad = 0, 10
                ecuacion = vars.ventana_principal.valorecuacion()
                vars.generar_onda = GENERADORONDA(amplitud, velocidad, tipo_onda, ecuacion)

        vars.simulacion_actual_graficando = nombre_simulacion 
        vars.movimiento_activo = True
        vars.tiempo_acumulado = 0.0
        vars.volviendo_a_inicio = False 
        vars.tiempo_inicio_movimiento_motor = time.time()
        vars.tiempo_primer_movimiento_fisico = None
        
        if not vars.ansys_video_active:
            vars.ventana_principal.agregar_a_log("VIDEO: Iniciando reproducción Ansys.")
            vars.ansys_video_timer.setInterval(nuevo_intervalo_ms)
            vars.ansys_video_timer.start()
            vars.ansys_video_active = True
            
    elif debe_realizar_movimiento and vars.movimiento_activo:
        vars.tiempo_lampara += 1
        if vars.tiempo_lampara >= 25:
            vars.valor = not vars.valor
            vars.ventana_principal.Lcambiolampara(vars.valor, vars.plc_conectado)
            vars.tiempo_lampara = 0

        if not vars.plc_conectado and vars.generar_onda:
            tiempo_actual = vars.tiempo_acumulado
            
            if hasattr(vars.generar_onda, 'ha_terminado_perfil') and vars.generar_onda.ha_terminado_perfil():
                vars.simulacion_finalizada_naturalmente = True  
                vars.ventana_principal.BdetenermovimientoClick() 
                return 
            
            _, posicion_grados = vars.generar_onda.siguiente_valor(tiempo_actual)
            consigna_mm = posicion_grados * 0.2618
            
            vars.contador_pintado_motor += 1
            if vars.contador_pintado_motor % 4 == 0:
                vars.ventana_principal.meteDatosGraficaMotor(tiempo_actual, consigna_mm, consigna_mm)
                vars.ventana_principal.movimientopistones(consigna_mm)
            
            dt = 0.02 
            volumen_actual_L = consigna_mm * FACTOR_MM_A_LITROS
            flujo_calculado = (volumen_actual_L - vars.prev_volumen_real) / dt
            vars.prev_volumen_real = volumen_actual_L
            
            vars.ventana_principal.meteDatosGraficaSimulacion_flujo_volumen(
                volumen_actual_L, flujo_calculado, 
                volumen_actual_L, flujo_calculado
            )
            vars.ventana_principal.meteDatosGraficaSimulacion_volumen_tiempo(
                tiempo_actual, volumen_actual_L,
                tiempo_actual, volumen_actual_L
            )
            vars.tiempo_acumulado += 0.02

    elif not debe_realizar_movimiento and vars.movimiento_activo:
        
        if not vars.plc_conectado and vars.generar_onda:
            
            if vars.simulacion_finalizada_naturalmente and vars.modo_simulacion_iniciado:
                    vars.movimiento_activo = False
                    vars.generar_onda = None
                    vars.ventana_principal.informacion_control_motor("OFFLINE: Ciclo completo (Hold).")
                    vars.ventana_principal.restablecer_controles_motor()
                    resetear_video_ansys(vars)
                    return

            if not vars.generar_onda.esta_volviendo():
                vars.generar_onda.activar_retorno_a_cero()
                vars.ventana_principal.informacion_control_motor("OFFLINE: Retornando a 0...")
                vars.ventana_principal.agregar_a_log("MOVIMIENTO: Interrumpido. Retornando a 0.")
                resetear_video_ansys(vars)

            _, posicion_grados = vars.generar_onda.siguiente_valor(vars.tiempo_acumulado)
            consigna_mm = posicion_grados * 0.2618
            
            vars.contador_pintado_motor += 1
            if vars.contador_pintado_motor % 2 == 0:
                vars.ventana_principal.meteDatosGraficaMotor(vars.tiempo_acumulado, consigna_mm, consigna_mm)
                vars.ventana_principal.movimientopistones(consigna_mm) 
            
            vars.tiempo_acumulado += 0.02
            
            if vars.generar_onda.retorno_finalizado():
                vars.movimiento_activo = False
                vars.generar_onda = None
                vars.ventana_principal.informacion_control_motor("OFFLINE: Retorno completo.")
                vars.ventana_principal.restablecer_controles_motor()
                
                #SUGERIR NOMBRE AL FINALIZAR MANUAL OFFLINE 
                nombre_base = vars.simulacion_actual_graficando if vars.modo_simulacion_iniciado else "Prueba_Manual"
                if not nombre_base or nombre_base == " ": nombre_base = "Prueba_Manual"
                
                sugerencia = generar_nombre_unico_prueba(vars, nombre_base)
                vars.ventana_principal.set_nombre_prueba_sugerido(sugerencia)
                vars.ventana_principal.activar_boton_guardar_prueba(True)
                vars.ventana_principal.Linfoanadireliminardatos("Prueba finalizada. Puede guardar.")
            return 
        
        if vars.plc_conectado:
            
            if vars.modo_simulacion_iniciado:
                if vars.simulacion_finalizada_naturalmente:
                    vars.movimiento_activo = False
                    vars.volviendo_a_inicio = False 
                    vars.ventana_principal.informacion_control_motor("Simulación finalizada. Motor en espera.")
                    vars.ventana_principal.restablecer_controles_motor()
                    resetear_video_ansys(vars)
                else:
                    if not vars.volviendo_a_inicio:
                        vars.volviendo_a_inicio = True 
                        try:
                            vars.manejador_plc.escribir_registro_simple(40011, 0)
                        except: pass
                        vars.ventana_principal.informacion_control_motor("Interrumpido. Retornando a inicio...")
                        vars.ventana_principal.agregar_a_log("PLC: Abortado por usuario. Retornando a 0.")
                        resetear_video_ansys(vars)
            else:
                if not vars.volviendo_a_inicio:
                    vars.volviendo_a_inicio = True 
                    try:
                        vars.manejador_plc.escribir_registro_simple(40011, 0)
                    except: pass
                    vars.ventana_principal.informacion_control_motor("Manual fin. Retornando a inicio...")
                    vars.ventana_principal.agregar_a_log("PLC: Manual finalizado. Retornando a 0.")
                    resetear_video_ansys(vars)
            
            vars.ventana_principal.Lcambiolampara(False, vars.plc_conectado)

def ejecutar_parada_emergencia(vars):
    vars.ventana_principal.agregar_a_log("!!! SETA PULSADA: PARADA DE EMERGENCIA TOTAL !!!")
    vars.parada_emergencia_activa = True
    
    vars.movimiento_activo = False
    vars.volviendo_a_inicio = False
    vars.generar_onda = None
    vars.medida_activa = False
    
    resetear_video_ansys(vars)

    vars.datos_grafica_eje_t.clear()
    vars.datos_grafica_posicion.clear()
    vars.datos_grafica_velocidad.clear()
    vars.datos_grafica_aceleracion.clear()
    vars.datos_grafica_sensor1.clear()
    vars.datos_grafica_sensor2.clear()
    
    vars.ventana_principal.activar_modo_emergencia_gui()
    vars.ventana_principal.informacion_control_motor("EMERGENCIA: SISTEMA BLOQUEADO. PULSE 'OK' PARA REINICIO")
    if vars.plc_conectado:
        try:
            vars.manejador_plc.escribir_registro_simple(40011, 2) 
            vars.ventana_principal.agregar_a_log("PLC: COMANDO DE EMERGENCIA (VR10=2) ENVIADO.")
        except Exception as e:
            vars.ventana_principal.agregar_a_log(f"ERROR: Fallo al enviar Stop Emergencia PLC: {e}")

def ejecutar_rearme_emergencia(vars):
    vars.ventana_principal.agregar_a_log("SISTEMA: Rearmado. Restaurando controles.")
    vars.parada_emergencia_activa = False
    vars.ventana_principal.desactivar_modo_emergencia_gui()
    vars.ventana_principal.actualizar_estado_conexion(vars.plc_conectado)
    estado_bd = True if vars.base_datos else False
    vars.ventana_principal.actualizar_estado_db(estado_bd)
    vars.ventana_principal.actualizar_lamparas_inicio(vars.plc_conectado)
    vars.ventana_principal.Lsensor1(vars.s_sup if vars.s_sup is not None else False, vars.plc_conectado)
    vars.ventana_principal.Lsensor2(vars.s_inf if vars.s_inf is not None else False, vars.plc_conectado)
    
    if vars.plc_conectado:
            try:
                vars.manejador_plc.escribir_registro_simple(40011, 0)
                vars.manejador_plc.escribir_registro_simple(40002, 1) 
                vars.ventana_principal.agregar_a_log("PLC: Registros de control reseteados.")
            except Exception as e:
                vars.ventana_principal.agregar_a_log(f"ERROR: Al resetear PLC: {e}")