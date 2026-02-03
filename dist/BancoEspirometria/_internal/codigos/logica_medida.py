#_____________________________________________________________________________________________________________________
#    Nombre del Script: logica_medida.py
#    Autor: José Alberto García Valiño
#    Fecha: 07-12-2025
#    Descripción:
#        Lógica para la gestión de medición con el espirómetro físico.
#        Coordina el inicio/fin de la captura de datos, procesa los flujos de entrada en
#        tiempo real y actualiza la interfaz gráfica con las curvas medidas del paciente.
#______________________________________________________________________________________________________________________

__author__ = "José Alberto García Valiño"
__copyright__ = "Copyright 2025, José Alberto García Valiño"
__credits__ = ["José Alberto García Valiño"]
__license__ = "MIT"
__version__ = "1.0"
__email__ = "albertogarva02@gmail.com"
__status__ = "Beta"


def recibir_datos_espirometro(vars, flujo, volumen):
    if flujo is not None and volumen is not None:
        vars.datos_flujo_volumen.append((flujo, volumen))
        vars.ventana_principal.meteDatosGraficaMedidas(volumen, flujo)
        vars.ventana_principal.Linfoanadireliminardatos(f"Flujo: {flujo:.2f} L/s | Vol: {volumen:.2f} L")

def iniciar_detener_medida(vars):
    tomar_medida = vars.ventana_principal.tomarmedida()
    if tomar_medida and not vars.medida_activa:
        vars.medida_activa = True
        vars.ventana_principal.agregar_a_log("MEDIDA: Iniciando lectura espirómetro...")
        vars.ventana_principal.Linfoanadireliminardatos("Iniciando toma de medida...")
        vars.ventana_principal.limpiarGraficaMedidas()
        vars.datos_flujo_volumen = []
        if not vars.espirometro_usb.conectar_y_empezar_lectura():
            vars.ventana_principal.Linfoanadireliminardatos("Error al conectar con el espirómetro")
            vars.ventana_principal.agregar_a_log("ERROR: Espirómetro no detectado.")
            vars.ventana_principal.fallo_comenzar_medida()
            vars.medida_activa = False
        else:
            vars.espirometro_usb.add_data_listener(lambda f, v: recibir_datos_espirometro(vars, f, v))
            vars.ventana_principal.Linfoanadireliminardatos("Espirómetro conectado. Respirar ahora.")
    elif not tomar_medida and vars.medida_activa:
        vars.medida_activa = False
        vars.ventana_principal.Linfoanadireliminardatos("Medida finalizada.")
        vars.ventana_principal.agregar_a_log("MEDIDA: Finalizada.")
        vars.espirometro_usb.detener_lectura()
        vars.espirometro_usb.cerrar_conexion()
    elif vars.medida_activa and not vars.espirometro_usb.conectado():
        vars.ventana_principal.Linfoanadireliminardatos("¡Conexión Perdida!")
        vars.ventana_principal.agregar_a_log("ERROR: Conexión espirómetro perdida.")
        vars.medida_activa = False
        vars.espirometro_usb.cerrar_conexion()