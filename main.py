#_____________________________________________________________________________________________________________________
#    Nombre del Script: main.py
#    Autor: José Alberto García Valiño
#    Fecha: 07-12-2025
#    Descripción:
#        Script principal que inicializa y coordina todos los módulos del
#        Banco de Espirometría. Sus responsabilidades incluyen:
#            1. Instanciar los objetos (GUI, Base de Datos, PLC, USB).
#            2. Configurar el contexto global (VariablesGlobales).
#            3. Establecer los temporizadores (QTimer) para los bucles de control y gráficos.
#            4. Vincular los eventos de la interfaz con la lógica de acción.
#______________________________________________________________________________________________________________________

__author__ = "José Alberto García Valiño"
__copyright__ = "Copyright 2025, José Alberto García Valiño"
__credits__ = ["José Alberto García Valiño"]
__license__ = "MIT"
__version__ = "1.0"
__email__ = "albertogarva02@gmail.com"
__status__ = "Beta"

import sys
import mysql.connector
from PySide6.QtCore import QTimer
from codigos.db_gui import DB_GUI
from codigos.gui import GUI
from codigos.simularcurvaflujo import SIMULARCURVAFLUJO
from codigos.plc_modbus import ControladorPLC
from codigos.usb import USB
from codigos.variables import VariablesGlobales
from codigos import logica_video
from codigos import logica_db
from codigos import logica_medida
from codigos import logica_plc
from codigos import logica_motor

def main():
    vars = VariablesGlobales()

    vars.base_datos = DB_GUI()
    vars.ventana_principal = GUI()
    vars.espirometro_usb = USB()
    vars.manejador_plc = ControladorPLC()

    # Timers
    timer_verificacion = QTimer()
    timer_simulacion = QTimer()
    vars.simulador_curva = SIMULARCURVAFLUJO(vars.ventana_principal, timer_simulacion)
    timer_simulacion.timeout.connect(vars.simulador_curva.simulargrafica)
    vars.ventana_principal.set_simulador(vars.simulador_curva)

    check_datos_timer = QTimer()
    grafica_motor_timer = QTimer()
    medida_timer = QTimer()
    vars.ansys_video_timer = QTimer()
    vars.timer_plc = QTimer()

    #Inicialización Base de Datos
    try:
        vars.base_datos = DB_GUI()
        vars.ventana_principal.actualizar_estado_db(True)
        vars.ventana_principal.agregar_a_log("INFO: Conexión con la base de datos establecida.")
    except mysql.connector.Error as e:
        vars.base_datos = None
        vars.ventana_principal.actualizar_estado_db(False)
        vars.ventana_principal.agregar_a_log(f"ERROR: Fallo conexión a BD: {e}")
    except Exception as e:
        vars.base_datos = None
        vars.ventana_principal.actualizar_estado_db(False)
        vars.ventana_principal.agregar_a_log(f"ERROR: Fallo inesperado BD: {e}")

    #Base de Datos y Archivos
    vars.ventana_principal.set_funcion_guardar(
        lambda *args: logica_db.guardar_datos(vars, *args))
    vars.ventana_principal.set_funcion_eliminar(
        lambda nombre: logica_db.eliminar_datos(vars, nombre))
    vars.ventana_principal.set_funcion_anadir_patologia(
        lambda pat: logica_db.anadir_patologia(vars, pat))
    vars.ventana_principal.set_funcion_descargar(
        lambda n, r: logica_db.descargar_simulacion(vars, n, r))
    vars.ventana_principal.set_funcion_obtener_datos_sim(
        lambda n: logica_db.obtener_datos_simulacion_por_nombre(vars, n))
    vars.ventana_principal.set_funcion_descargar_comparativa(
        lambda l, r: logica_db.descargar_comparativa(vars, l, r))
    vars.ventana_principal.set_funcion_guardar_prueba(
        lambda: logica_db.guardar_prueba_realizada(vars))

    #PLC
    vars.ventana_principal.set_funcion_conectar_plc(
        lambda ip, p: logica_plc.conectar_plc(vars, ip, p))
    vars.ventana_principal.set_funcion_desconectar_plc(
        lambda: logica_plc.desconectar_plc(vars))
    vars.ventana_principal.set_funcion_escribir_plc(
        lambda r, v: logica_plc.escribir_en_plc(vars, r, v))
    vars.ventana_principal.set_funcion_calibrar(
        lambda: logica_plc.ejecutar_calibracion_plc(vars))
    vars.ventana_principal.set_funcion_cambio_variable_grafica(
        lambda idx=-1: logica_plc.actualizar_grafica_tendencia(vars, idx))

    #Emergencia
    vars.ventana_principal.set_funciones_emergencia(
        lambda: logica_motor.ejecutar_parada_emergencia(vars),
        lambda: logica_motor.ejecutar_rearme_emergencia(vars)
    )

    # Timers Connect
    grafica_motor_timer.timeout.connect(lambda: logica_motor.generargraficamotor(vars))
    grafica_motor_timer.start(20)

    check_datos_timer.timeout.connect(lambda: logica_db.consultaCBsimulacion(vars))
    check_datos_timer.start(100)

    timer_verificacion.timeout.connect(lambda: logica_db.verificar_y_enviar_datos(vars))
    timer_verificacion.start(500)

    medida_timer.timeout.connect(lambda: logica_medida.iniciar_detener_medida(vars))
    medida_timer.start(500)

    vars.ansys_video_timer.timeout.connect(lambda: logica_video.actualizar_video_ansys_in(vars))
    vars.ansys_video_timer.timeout.connect(lambda: logica_video.actualizar_video_ansys_out(vars))

    vars.timer_plc.timeout.connect(lambda: logica_plc.leer_datos_plc_en_bucle(vars))
    logica_plc.configurar_defaults_plc(vars)

    logica_db.actualizar_gui(vars)
   
    vars.ventana_principal.ventana.show()
    sys.exit(vars.ventana_principal.aplicacion.exec())

if __name__ == "__main__":
    main()