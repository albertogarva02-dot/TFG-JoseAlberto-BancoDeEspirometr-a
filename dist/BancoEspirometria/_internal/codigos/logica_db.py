#_____________________________________________________________________________________________________________________
#    Nombre del Script: logica_db.py
#    Autor: José Alberto García Valiño
#    Fecha: 07-12-2025
#    Descripción:
#        Módulo intermedio que coordina la comunicación entre la interfaz gráfica
#        y la base de datos. Gestiona la lógica para guardar simulaciones,
#        actualizar tablas visuales, eliminar registros y procesar datos antes de
#        enviarlos a las gráficas o al exportador.
#______________________________________________________________________________________________________________________

__author__ = "José Alberto García Valiño"
__copyright__ = "Copyright 2025, José Alberto García Valiño"
__credits__ = ["José Alberto García Valiño"]
__license__ = "MIT"
__version__ = "1.0"
__email__ = "albertogarva02@gmail.com"
__status__ = "Beta"


import ast
import gc
from codigos.exportar_excel import exportar_a_excel, exportar_comparacion_excel

def actualizar_gui(vars):
    patologias_actualizadas = vars.base_datos.consultapatologias()
    simulaciones_actualizadas = vars.base_datos.consultanombressimulaciones()
    datos_actualizados = vars.base_datos.obtenerTodosLosDatos()

    vars.ventana_principal.mostrarCBnombrespatologias(patologias_actualizadas)
    vars.ventana_principal.mostrarCBnombresimulacion(simulaciones_actualizadas)
    vars.ventana_principal.mostrarDatosenTableWidget(datos_actualizados)
    vars.ventana_principal.actualizar_lamparas_inicio(vars.plc_conectado)

def guardar_datos(vars, *datos):
    if datos:
        try:
            resultado = vars.base_datos.registradatos(*datos)
            vars.ventana_principal.Linfoanadireliminardatos(resultado)
            vars.ventana_principal.agregar_a_log(f"INFO: Datos guardados. {resultado}")
            actualizar_gui(vars)
        except Exception as e:
            vars.ventana_principal.Linfoanadireliminardatos(f"Error al guardar: {str(e)}")
            vars.ventana_principal.agregar_a_log(f"ERROR: Al guardar datos: {e}")

def eliminar_datos(vars, nombre):
    if nombre:
        try:
            exito = vars.base_datos.eliminadatos(nombre)
            if exito:
                msg = f"Simulación '{nombre}' eliminada con éxito."
                vars.ventana_principal.Linfoanadireliminardatos(msg)
                vars.ventana_principal.agregar_a_log(f"INFO: {msg}")
                actualizar_gui(vars)
            else:
                vars.ventana_principal.Linfoanadireliminardatos(f"No se pudo eliminar '{nombre}'.")
        except Exception as e:
            vars.ventana_principal.Linfoanadireliminardatos(f"Error crítico al eliminar: {str(e)}")
            vars.ventana_principal.agregar_a_log(f"ERROR: Al eliminar datos: {e}")

def anadir_patologia(vars, nueva_patologia):
    if nueva_patologia:
        try:
            resultado = vars.base_datos.registrapatologia(nueva_patologia)
            vars.ventana_principal.Linfoanadireliminardatos(resultado)
            vars.ventana_principal.agregar_a_log(f"INFO: Patología añadida. {resultado}")
            actualizar_gui(vars)
        except Exception as e:
            vars.ventana_principal.Linfoanadireliminardatos(f"Error al añadir patología: {str(e)}")

def descargar_simulacion(vars, nombre_simulacion, ruta_archivo):
    datos_recibidos = vars.base_datos.consultadatos(nombre_simulacion)
    if not datos_recibidos or isinstance(datos_recibidos, str):
        mensaje_error = datos_recibidos if isinstance(datos_recibidos, str) else f"No se encontraron datos para '{nombre_simulacion}'."
        vars.ventana_principal.Linfosimulacion(mensaje_error)
        return
    try:
        datos_corregidos = (
            nombre_simulacion, datos_recibidos[1], datos_recibidos[2], datos_recibidos[3],
            datos_recibidos[4], datos_recibidos[5], datos_recibidos[6], datos_recibidos[7],
            datos_recibidos[8], datos_recibidos[0], datos_recibidos[9]
        )
    except IndexError:
        vars.ventana_principal.Linfosimulacion("Error: El formato de datos recibido de la BD es incorrecto.")
        return
    exito, mensaje = exportar_a_excel(datos_corregidos, ruta_archivo)
    vars.ventana_principal.Linfosimulacion(mensaje)
    vars.ventana_principal.agregar_a_log(f"EXPORTAR: {mensaje}")

def obtener_datos_completos_sim(vars, nombre_simulacion):
    datos_recibidos = vars.base_datos.consultadatos(nombre_simulacion)
    if not datos_recibidos or isinstance(datos_recibidos, str):
        return None
    try:
        return (
            nombre_simulacion, datos_recibidos[1], datos_recibidos[2], datos_recibidos[3],
            datos_recibidos[4], datos_recibidos[5], datos_recibidos[6], datos_recibidos[7],
            datos_recibidos[8], datos_recibidos[0], datos_recibidos[9]
        )
    except IndexError:
        return None

def descargar_comparativa(vars, lista_nombres_sims, ruta_archivo):
    lista_de_datos_completos = []
    for nombre in lista_nombres_sims:
        datos_completos = obtener_datos_completos_sim(vars, nombre)
        if datos_completos:
            lista_de_datos_completos.append(datos_completos)
    if not lista_de_datos_completos:
        return
    exito, mensaje = exportar_comparacion_excel(lista_de_datos_completos, ruta_archivo)
    vars.ventana_principal.agregar_a_log(f"COMPARATIVA: {mensaje}")

def obtener_datos_simulacion_por_nombre(vars, nombre_simulacion):
    if not nombre_simulacion or nombre_simulacion == " ":
        return None
    try:
        consultadatos = vars.base_datos.consultadatos(nombre_simulacion)
        if not consultadatos: return None
        valores_str = consultadatos[9] 
        if isinstance(valores_str, str):
            valores_lista = ast.literal_eval(valores_str)
            if isinstance(valores_lista, list): return valores_lista
        return None
    except Exception as e:
        return None

def generar_nombre_unico_prueba(vars, nombre_base):
    if not nombre_base or nombre_base == " " or nombre_base == "-":
        nombre_base = "Prueba_Manual"
    
    if not vars.base_datos: return nombre_base + "_1"

    lista_existentes = vars.base_datos.consultanombressimulaciones()
    contador = 1
    nuevo_nombre = f"{nombre_base}_{contador}"
    
    while nuevo_nombre in lista_existentes:
        contador += 1
        nuevo_nombre = f"{nombre_base}_{contador}"
        
    return nuevo_nombre

def guardar_prueba_realizada(vars):
    nombre_final = vars.ventana_principal.obtener_nombre_prueba_sugerido()
    if not nombre_final:
        vars.ventana_principal.Linfoanadireliminardatos("Error: Nombre de prueba vacío.")
        return

    if vars.base_datos:
        lista = vars.base_datos.consultanombressimulaciones()
        if nombre_final in lista:
            vars.ventana_principal.Linfoanadireliminardatos(f"Error: La simulación '{nombre_final}' ya existe.")
            return

    datos_grafica = vars.ventana_principal.obtener_datos_grafica_fv_actual()
    if not datos_grafica:
        vars.ventana_principal.Linfoanadireliminardatos("Error: No hay datos en la gráfica para guardar.")
        return
    
    datos_str = str(datos_grafica)

    nombre_p = "Manual"
    edad = 0
    peso = 0
    sexo = "_"
    dni = "00000000X"
    fumador = "NO"
    patologia = "Manual"
    altura = 0

    if vars.modo_simulacion_iniciado and vars.simulacion_actual_graficando:
        datos_origen = vars.base_datos.consultadatos(vars.simulacion_actual_graficando)
        if datos_origen and not isinstance(datos_origen, str):
            try:
                patologia = datos_origen[0]
                nombre_p = datos_origen[1]
                edad = datos_origen[2]
                peso = datos_origen[3]
                sexo = datos_origen[4]
                dni = datos_origen[5]
                fumador = datos_origen[6]
                altura = datos_origen[8]
            except: pass
    
    try:
        res = vars.base_datos.registradatos(nombre_p, edad, peso, sexo, dni, fumador, patologia, altura, datos_str, nombre_final)
        vars.ventana_principal.Linfoanadireliminardatos(f"Guardado exitosamente: {nombre_final}")
        vars.ventana_principal.agregar_a_log(f"BD: Prueba guardada como {nombre_final}")
        actualizar_gui(vars) 
    except Exception as e:
        vars.ventana_principal.Linfoanadireliminardatos(f"Error BD al guardar: {e}")

def consultaCBsimulacion(vars):
    if vars.parada_emergencia_activa:
        return

    if vars.movimiento_activo: return
    posiblesimulacion = vars.ventana_principal.devolversimulacionCB()
    
    if not posiblesimulacion or posiblesimulacion == " " or posiblesimulacion == vars.simulacion_actual_graficando:
        if posiblesimulacion == " ":
            vars.ventana_principal.Linfosimulacion("") 
            vars.ventana_principal.set_nombre_prueba_sugerido("")
            vars.ventana_principal.activar_boton_guardar_prueba(False)
        return

    vars.ventana_principal.limpiaGraficaSimulacion_flujo_volumen()
    vars.ventana_principal.limpiarGraficaSimulacion_volumen_tiempo()
    vars.ventana_principal.limpiarGraficaMotor() 
    
    gc.collect() 

    vars.simulacion_actual_graficando = posiblesimulacion
    vars.indice_datos_graficados = 0

    if posiblesimulacion and posiblesimulacion != " ":
        sugerencia = generar_nombre_unico_prueba(vars, posiblesimulacion)
        vars.ventana_principal.set_nombre_prueba_sugerido(sugerencia)
        vars.ventana_principal.activar_boton_guardar_prueba(True)
    else:
        vars.ventana_principal.set_nombre_prueba_sugerido("")
        vars.ventana_principal.activar_boton_guardar_prueba(False)

    consultadatos = vars.base_datos.consultadatos(vars.simulacion_actual_graficando)
    if not consultadatos: 
        vars.ventana_principal.Linfosimulacion("Error: No se encontraron datos.")
        return
    
    vars.ventana_principal.Linfosimulacion(consultadatos)

    valores_str = consultadatos[9]
    if isinstance(valores_str, str):
        try:
            valores = ast.literal_eval(valores_str)
            if isinstance(valores, list):
                tiempo_transcurrido = 0
                volumen_anterior = valores[0][0]
                datos_tiempo_volumen = [] 
                for volumen, flujo in valores:
                    if flujo != 0:
                        delta_tiempo = abs((volumen - volumen_anterior) / flujo)
                        if delta_tiempo > 1.0: delta_tiempo = 0.01 
                        tiempo_transcurrido += delta_tiempo
                    else:
                        delta_tiempo = 0.01
                        tiempo_transcurrido += delta_tiempo
                    datos_tiempo_volumen.append((tiempo_transcurrido, volumen))
                    vars.ventana_principal.meteDatosGraficaSimulacion_flujo_volumen(volumen, flujo, None, None) 
                    volumen_anterior = volumen
                for tiempo, volumen_tv in datos_tiempo_volumen:
                    vars.ventana_principal.meteDatosGraficaSimulacion_volumen_tiempo(tiempo, volumen_tv, None, None)
                vars.indice_datos_graficados = len(valores)
        except (SyntaxError, ValueError):
            vars.ventana_principal.Linfosimulacion("Error al procesar datos.")

def verificar_y_enviar_datos(vars):
    if vars.ventana_principal.RBgenerarsimulacionChecked():
        vars.ventana_principal.Linfoanadireliminardatos("Generando curva, esperando datos...")
        datos_paciente_actual = vars.ventana_principal.RBgenerarsimulacionTrue()
        if datos_paciente_actual:
            if datos_paciente_actual != vars.datos_paciente_previos:
                vars.simulador_curva.recibir_datos_paciente(*datos_paciente_actual)
                vars.ventana_principal.Linfoanadireliminardatos("Datos actualizados, calculando... ")
                vars.datos_paciente_previos = datos_paciente_actual
    else:
        vars.datos_paciente_previos = None