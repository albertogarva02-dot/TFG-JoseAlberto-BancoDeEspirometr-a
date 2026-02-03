#_____________________________________________________________________________________________________________________
#    Nombre del Script: logica_video.py
#    Autor: José Alberto García Valiño
#    Fecha: 07-12-2025
#    Descripción:
#        Módulo encargado de la sincronización y reproducción de secuencias de imágenes
#        de simulación de fluidos (CFD). Gestiona los bucles de animación de entrada
#        y salida de aire en la interfaz, coordinándolos con la velocidad del motor.
#______________________________________________________________________________________________________________________

__author__ = "José Alberto García Valiño"
__copyright__ = "Copyright 2025, José Alberto García Valiño"
__credits__ = ["José Alberto García Valiño"]
__license__ = "MIT"
__version__ = "1.0"
__status__ = "Beta"

from codigos.constantes import ANSYS_MAX_FRAME_IN, ANSYS_LOOP_START_IN, ANSYS_MAX_FRAME_OUT, ANSYS_LOOP_START_OUT

def resetear_video_ansys(vars):
    if vars.ansys_video_active:
        vars.ansys_video_timer.stop()
        vars.ansys_video_active = False
    
    vars.ansys_frame_index_in = 0
    vars.ansys_frame_index_out = 0
    vars.ventana_principal.mostrar_frame_ansys_in(0)
    vars.ventana_principal.mostrar_frame_ansys_out(0)

def actualizar_video_ansys_in(vars):
    vars.ventana_principal.mostrar_frame_ansys_in(vars.ansys_frame_index_in)
    vars.ansys_frame_index_in += 1
    if vars.ansys_frame_index_in > ANSYS_MAX_FRAME_IN:
        vars.ansys_frame_index_in = ANSYS_LOOP_START_IN

def actualizar_video_ansys_out(vars):
    vars.ventana_principal.mostrar_frame_ansys_out(vars.ansys_frame_index_out)
    vars.ansys_frame_index_out += 1
    if vars.ansys_frame_index_out > ANSYS_MAX_FRAME_OUT:
        vars.ansys_frame_index_out = ANSYS_LOOP_START_OUT