#_____________________________________________________________________________________________________________________
#    Nombre del Script: gui.py
#    Autor: José Alberto García Valiño
#    Fecha: 07-12-2025
#    Descripción:
#        Clase principal que inicializa y gestiona la interfaz gráfica de usuario.
#        Se encarga de cargar el archivo .ui, conectar señales, gestionar
#        los eventos de los botones, actualizar las gráficas en tiempo real y coordinar
#        los diferentes módulos del sistema (PLC, BD, Motor).
#______________________________________________________________________________________________________________________

__author__ = "José Alberto García Valiño"
__copyright__ = "Copyright 2025, José Alberto García Valiño"
__credits__ = ["José Alberto García Valiño"]
__license__ = "MIT"
__version__ = "1.0"
__email__ = "albertogarva02@gmail.com"
__status__ = "Beta"

import sys
import os
from PySide6.QtWidgets import QApplication, QLabel, QComboBox, QCheckBox, QPushButton, QLineEdit, \
    QTableWidget, QTableWidgetItem, QRadioButton, QFileDialog, QMessageBox, QListWidget, QListWidgetItem, QPlainTextEdit, QWidget, QTabWidget, QVBoxLayout
from PySide6.QtCore import QFile, Qt
from PySide6.QtGui import QPixmap, QColor, QPainter, QTransform
from PySide6.QtUiTools import QUiLoader
from codigos.widgetgrafico import WidgetGrafico
from codigos.cgraficas import CGraficas
from codigos.procesador_datos import cargar_datos_archivo
from datetime import datetime
from PySide6.QtCore import QTimer
from PySide6.QtPdf import QPdfDocument                  
from PySide6.QtPdfWidgets import QPdfView

def ruta_recurso(ruta_relativa):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, ruta_relativa)

class GUI:
    def __init__(self):
        super().__init__()
        cargador=QUiLoader()
        cargador.registerCustomWidget(WidgetGrafico)
        self.__aplicacion=QApplication(sys.argv)
        archivoUi=QFile(ruta_recurso("interfaz/bancoespirometria.ui"))
        archivoUi.open(QFile.ReadOnly)
        self.__ventana=cargador.load(archivoUi)
        archivoUi.close()

        #Labels
        self.__Leei=self.__ventana.findChild(QLabel, "Leei")
        self.__Luvigo=self.__ventana.findChild(QLabel, "Luvigo")
        self.__Lsensor1=self.__ventana.findChild(QLabel, "Lsensor1")
        self.__Lsensor2=self.__ventana.findChild(QLabel, "Lsensor2")
        self.__Lmovimiento_2=self.__ventana.findChild(QLabel, "Lmovimiento_2")
        self.__Lmovimiento_3=self.__ventana.findChild(QLabel, "Lmovimiento_3")
        self.__Lmovimiento_4=self.__ventana.findChild(QLabel, "Lmovimiento_4")
        self.__Lmovimiento_5=self.__ventana.findChild(QLabel, "Lmovimiento_5")
        self.__Lmovimiento_6=self.__ventana.findChild(QLabel, "Lmovimiento_6")
        self.__Lmovimiento_7=self.__ventana.findChild(QLabel, "Lmovimiento_7")
        self.__Lmovimiento_8=self.__ventana.findChild(QLabel, "Lmovimiento_8")
        self.__Lmovimiento_superior_izq=self.__ventana.findChild(QLabel, "Lmovimiento_superior_izq")
        self.__Lmovimiento_superior_derch=self.__ventana.findChild(QLabel, "Lmovimiento_superior_derch")
        self.__Lcontrolinformacion=self.__ventana.findChild(QLabel, "Lcontrolinformacion")
        self.__Linfoanadireliminardatos=self.__ventana.findChild(QLabel, "Linfoanadireliminardatos")
        self.__Lcfd=self.__ventana.findChild(QLabel, "Lcfd")
        self.__Lfvc=self.__ventana.findChild(QLabel, "Lfvc")
        self.__Lfev1=self.__ventana.findChild(QLabel, "Lfev1")
        self.__Lpef=self.__ventana.findChild(QLabel, "Lpef")
        self.__Lfev1_fvc=self.__ventana.findChild(QLabel, "Lfev1_fvc")
        self.__Lic=self.__ventana.findChild(QLabel, "Lic")
        self.__Linfosimulacion=self.__ventana.findChild(QLabel, "Linfosimulacion")
        self.__Lpistones=self.__ventana.findChild(QLabel, "Lpistones")
        self.__LImagenInfoDatos=self.__ventana.findChild(QLabel, "LImagenInfoDatos")
        self.__LImagenInfoDatos_2=self.__ventana.findChild(QLabel, "LImagenInfoDatos_2")
        self.__LImagenInfoDatos_3=self.__ventana.findChild(QLabel, "LImagenInfoDatos_3")
        self.__LImagenInfoMotor=self.__ventana.findChild(QLabel, "LImagenInfoMotor")
        self.__Lflujo1=self.__ventana.findChild(QLabel, "Lflujo1")
        self.__Lflujo2=self.__ventana.findChild(QLabel, "Lflujo2")
        self.__Lflujo3=self.__ventana.findChild(QLabel, "Lflujo3")
        self.__Linfodatos=self.__ventana.findChild(QLabel, "Linfodatos")
        self.__LinfoEcuacion=self.__ventana.findChild(QLabel, "LinfoEcuacion")
        self.__Lsuperior_actuador=self.__ventana.findChild(QLabel, "Lsuperior_actuador")
        self.__Lsuperior_actuador_2=self.__ventana.findChild(QLabel, "Lsuperior_actuador_2")
        self.__Lactuador=self.__ventana.findChild(QLabel, "Lactuador")
        self.__Lactuador_2=self.__ventana.findChild(QLabel, "Lactuador_2")
        self.__Lvastago=self.__ventana.findChild(QLabel, "Lvastago")
        self.__Lvastago_2=self.__ventana.findChild(QLabel, "Lvastago_2")
        self.__Lfin_vastago=self.__ventana.findChild(QLabel, "Lfin_vastago")
        self.__Lfin_vastago_2=self.__ventana.findChild(QLabel, "Lfin_vastago_2")
        self.__Linferior_actuador=self.__ventana.findChild(QLabel, "Linferior_actuador")
        self.__Linferior_actuador_2=self.__ventana.findChild(QLabel, "Linferior_actuador_2")
        self.__Ltubo=self.__ventana.findChild(QLabel, "Ltubo")
        self.__Lfin_tubo=self.__ventana.findChild(QLabel, "Lfin_tubo")
        self.__Lout=self.__ventana.findChild(QLabel, "Lout")
        self.__Lin=self.__ventana.findChild(QLabel, "Lin")
        self.__Lsensor_npn_1=self.__ventana.findChild(QLabel, "Lsensor_npn_1")
        self.__Lsensor_npn_2=self.__ventana.findChild(QLabel, "Lsensor_npn_2")
        self.__Lvistafrontal_plc=self.__ventana.findChild(QLabel, "Lvistafrontal_plc")
        self.__Lvistageneral_plc=self.__ventana.findChild(QLabel, "Lvistageneral_plc")
        self.__Lestado_lampara=self.__ventana.findChild(QLabel, "Lestado_lampara")
        self.__Lestado_texto=self.__ventana.findChild(QLabel, "Lestado_texto")
        self.__Llampara_controlador_1=self.__ventana.findChild(QLabel, "Llampara_controlador_1")
        self.__Llampara_controlador_2=self.__ventana.findChild(QLabel, "Llampara_controlador_2")
        self.__Llampara_controlador_3=self.__ventana.findChild(QLabel, "Llampara_controlador_3")
        self.__Llampara_controlador_4=self.__ventana.findChild(QLabel, "Llampara_controlador_4")
        self.__Llampara_controlador_5=self.__ventana.findChild(QLabel, "Llampara_controlador_5")
        self.__Llampara_controlador_6=self.__ventana.findChild(QLabel, "Llampara_controlador_6")
        self.__Llampara_controlador_7=self.__ventana.findChild(QLabel, "Llampara_controlador_7")
        self.__Llampara_controlador_8=self.__ventana.findChild(QLabel, "Llampara_controlador_8")
        self.__Lesquinero=self.__ventana.findChild(QLabel, "Lesquinero")
        self.__Lsensor_npn_3=self.__ventana.findChild(QLabel, "Lsensor_npn_3")
        self.__Lsensor_npn_4=self.__ventana.findChild(QLabel, "Lsensor_npn_4")
        self.__Lsensor1_2=self.__ventana.findChild(QLabel, "Lsensor1_2")
        self.__Lsensor2_2=self.__ventana.findChild(QLabel, "Lsensor2_2")
        self.__Lcremallera=self.__ventana.findChild(QLabel, "Lcremallera")
        self.__Lesquinero_2=self.__ventana.findChild(QLabel, "Lesquinero_2")
        self.__Lengranaje=self.__ventana.findChild(QLabel, "Lengranaje")
        self.__Lmotor=self.__ventana.findChild(QLabel, "Lmotor")
        self.__Ldriver=self.__ventana.findChild(QLabel, "Ldriver")
        self.__Lplc_inicio=self.__ventana.findChild(QLabel, "Lplc_inicio")
        self.__Lsql=self.__ventana.findChild(QLabel, "Lsql")
        self.__Ltubo_2=self.__ventana.findChild(QLabel, "Ltubo_2")
        self.__Lsuperior_actuador_3=self.__ventana.findChild(QLabel, "Lsuperior_actuador_3")
        self.__Lsuperior_actuador_4=self.__ventana.findChild(QLabel, "Lsuperior_actuador_4")
        self.__Lactuador_3=self.__ventana.findChild(QLabel, "Lactuador_3")
        self.__Lactuador_4=self.__ventana.findChild(QLabel, "Lactuador_4")
        self.__Linferior_actuador_3=self.__ventana.findChild(QLabel, "Linferior_actuador_3")
        self.__Linferior_actuador_4=self.__ventana.findChild(QLabel, "Linferior_actuador_4")
        self.__Lvastago_3=self.__ventana.findChild(QLabel, "Lvastago_3")
        self.__Lvastago_4=self.__ventana.findChild(QLabel, "Lvastago_4")
        self.__Lfin_vastago_3=self.__ventana.findChild(QLabel, "Lfin_vastago_3")
        self.__Lfin_vastago_4=self.__ventana.findChild(QLabel, "Lfin_vastago_4")
        self.__Llampara_datos_inicio=self.__ventana.findChild(QLabel, "Llampara_datos_inicio")
        self.__Limagen_inicio=self.__ventana.findChild(QLabel, "Limagen_inicio")
        self.__Lordenador=self.__ventana.findChild(QLabel, "Lordenador")
        self.__Llampara_plc_inicio=self.__ventana.findChild(QLabel, "Llampara_plc_inicio")
        self.__Llampara_configurar_conexion=self.__ventana.findChild(QLabel, "Llampara_configurar_conexion")
        self.__Lcremallera_2=self.__ventana.findChild(QLabel, "Lcremallera_2")
        self.__Limagen_comparacion_inicio=self.__ventana.findChild(QLabel, "Limagen_comparacion_inicio")
        self.__Llampara_configurar_realizarsimulacion=self.__ventana.findChild(QLabel, "Llampara_configurar_realizarsimulacion")
        self.__Llampara_configurar_compararsimulaciones=self.__ventana.findChild(QLabel, "Llampara_configurar_compararsimulaciones")
        self.__L_contenido_acerca_de=self.__ventana.findChild(QLabel, "L_contenido_acerca_de")

        #ComboBox
        self.__CBvelocidad=self.__ventana.findChild(QComboBox, "CBvelocidad")
        self.__CBmovimientospredefinidos=self.__ventana.findChild(QComboBox, "CBmovimientospredefinidos")
        self.__CBseleccionsimulacion=self.__ventana.findChild(QComboBox, "CBseleccionsimulacion")
        self.__CBedad=self.__ventana.findChild(QComboBox, "CBedad")
        self.__CBpeso=self.__ventana.findChild(QComboBox, "CBpeso")
        self.__CBsexo=self.__ventana.findChild(QComboBox, "CBsexo")
        self.__CBfumador=self.__ventana.findChild(QComboBox, "CBfumador")
        self.__CBpatologia=self.__ventana.findChild(QComboBox, "CBpatologia")
        self.__CBnombresimulacion=self.__ventana.findChild(QComboBox, "CBnombresimulacion")
        self.__CBaltura=self.__ventana.findChild(QComboBox, "CBaltura")
        self.__CBamplitud=self.__ventana.findChild(QComboBox, "CBamplitud")
        self.__CBvariable=self.__ventana.findChild(QComboBox, "CBvariable")
        self.__CBregistro=self.__ventana.findChild(QComboBox, "CBregistro")


        #CheckBox
        self.__Cdatospaciente=self.__ventana.findChild(QCheckBox, "Cdatospaciente")

        #Botones
        self.__Brealizarmovimiento=self.__ventana.findChild(QPushButton, "Brealizarmovimiento")
        self.__Bdetenermovimiento = self.__ventana.findChild(QPushButton, "Bdetenermovimiento")
        self.__Bejecutarsimulacion=self.__ventana.findChild(QPushButton, "Bejecutarsimulacion")
        self.__Bdetenersimulacion=self.__ventana.findChild(QPushButton, "Bdetenersimulacion")
        self.__Banadirdatos=self.__ventana.findChild(QPushButton, "Banadirdatos")
        self.__Beliminardatos=self.__ventana.findChild(QPushButton, "Beliminardatos")
        self.__Banadirpatologia=self.__ventana.findChild(QPushButton, "Banadirpatologia")
        self.__Bcomenzarmedida=self.__ventana.findChild(QPushButton, "Bcomenzarmedida")
        self.__Bfinalizarmedida=self.__ventana.findChild(QPushButton, "Bfinalizarmedida")
        self.__Bguardarprueba=self.__ventana.findChild(QPushButton, "Bguardarprueba")
        self.__Bseleccionararchivo=self.__ventana.findChild(QPushButton, "Bseleccionararchivo")
        self.__Bdescargar=self.__ventana.findChild(QPushButton, "Bdescargar")
        self.__Bdescargar_2=self.__ventana.findChild(QPushButton, "Bdescargar_2")
        self.__Bescribir=self.__ventana.findChild(QPushButton, "Bescribir")
        self.__Bconectar=self.__ventana.findChild(QPushButton, "Bconectar")
        self.__Bdesconectar=self.__ventana.findChild(QPushButton, "Bdesconectar")
        self.__Bconfigurar_conexion_inicio=self.__ventana.findChild(QPushButton, "Bconfigurar_conexion_inicio")
        self.__Bcontrol_manual_motor_inicio=self.__ventana.findChild(QPushButton, "Bcontrol_manual_motor_inicio")
        self.__Brealizar_simulacion_inicio=self.__ventana.findChild(QPushButton, "Brealizar_simulacion_inicio")
        self.__Bdatos_inicio=self.__ventana.findChild(QPushButton, "Bdatos_inicio")
        self.__Bcomparar_simulaciones_inicio=self.__ventana.findChild(QPushButton, "Bcomparar_simulaciones_inicio")
        self.__Banadir_simulacion_inicio=self.__ventana.findChild(QPushButton, "Banadir_simulacion_inicio")
        self.__Bacerca_de_inicio=self.__ventana.findChild(QPushButton, "Bacerca_de_inicio")
        self.__Bayuda_inicio=self.__ventana.findChild(QPushButton, "Bayuda_inicio")
        self.__Bseta_inicio=self.__ventana.findChild(QPushButton, "Bseta_inicio")
        self.__Bseta_superior_izquierda=self.__ventana.findChild(QPushButton, "Bseta_superior_izquierda")
        self.__Bseta_superior_derecha=self.__ventana.findChild(QPushButton, "Bseta_superior_derecha")
        self.__Bseta_ok=self.__ventana.findChild(QPushButton, "Bseta_ok")
        self.__Bmodo_oscuro= self.__ventana.findChild(QPushButton, "Bmodo_oscuro")
        self.__Bcalibrar=self.__ventana.findChild(QPushButton, "Bcalibrar")
        self.__Bcalibrar_2=self.__ventana.findChild(QPushButton, "Bcalibrar_2")
        self.__Bcalibrar_3=self.__ventana.findChild(QPushButton, "Bcalibrar_3")

        #RadioButton
        self.__RBgenerarsimulacion=self.__ventana.findChild(QRadioButton, "RBgenerarsimulacion")
        self.__RBtomarmedidas=self.__ventana.findChild(QRadioButton, "RBtomarmedidas")
        self.__RBcargarvalores=self.__ventana.findChild(QRadioButton, "RBcargarvalores")

        #LineEdit
        self.__Enombrepaciente=self.__ventana.findChild(QLineEdit, "Enombrepaciente")
        self.__Edni=self.__ventana.findChild(QLineEdit, "Edni")
        self.__Epatologia=self.__ventana.findChild(QLineEdit, "Epatologia")
        self.__Enombresimulacion=self.__ventana.findChild(QLineEdit, "Enombresimulacion")
        self.__Eecuacion=self.__ventana.findChild(QLineEdit, "Eecuacion")
        self.__Enombreprueba=self.__ventana.findChild(QLineEdit, "Enombreprueba")
        self.__Efiltrar_simulaciones=self.__ventana.findChild(QLineEdit, "Efiltrar_simulaciones")
        self.__Edireccion_ip=self.__ventana.findChild(QLineEdit, "Edireccion_ip")
        self.__Epuerto=self.__ventana.findChild(QLineEdit, "Epuerto")
        self.__Evalor_registro=self.__ventana.findChild(QLineEdit, "Evalor_registro")

        #TableWidget
        self.__datos=self.__ventana.findChild(QTableWidget, "datos")
        self.__monitor=self.__ventana.findChild(QTableWidget, "monitor")
        self.__monitor.setColumnWidth(0, 150)

        #QListWidget
        self.__LW_comparar_simulaciones=self.__ventana.findChild(QListWidget, "LW_comparar_simulaciones")

        #Qplaintextedit
        self.__TE_registro_eventos=self.__ventana.findChild(QPlainTextEdit, "TE_registro_eventos")

        #QTabWidgets
        self.__tab_pestanas=self.__ventana.findChild(QTabWidget, "pestanas")

        #QWidgets
        self.__pagina_comunicacion=self.__ventana.findChild(QWidget, "comunicacionplc")
        self.__pagina_controlmotor=self.__ventana.findChild(QWidget, "controlmotor")
        self.__pagina_realizarsimulacion=self.__ventana.findChild(QWidget, "realizarsimulacion")
        self.__pagina_mostrardatos=self.__ventana.findChild(QWidget, "mostrardatos")
        self.__pagina_compararsimulaciones=self.__ventana.findChild(QWidget, "compararsimulaciones")
        self.__pagina_anadirsimulacion=self.__ventana.findChild(QWidget, "anadirsimulacion")
        self.__pagina_ayuda=self.__ventana.findChild(QWidget, "ayuda")
        self.__pagina_acerca_de=self.__ventana.findChild(QWidget, "acerca_de")
        self.__contenedor_pdf = self.__ventana.findChild(QWidget, "pdf")

        #Imagenes
        self.__eei=QPixmap(ruta_recurso("imagenes/eei.png"))
        self.__uvigo=QPixmap(ruta_recurso("imagenes/uvigo.png"))
        self.__banco=QPixmap(ruta_recurso("imagenes/esquemabanco_sin_pist.PNG"))
        self.__LamparaAmbar=QPixmap(ruta_recurso("imagenes/LamparaAmbar.png"))
        self.__LamparaGris=QPixmap(ruta_recurso("imagenes/LamparaGris.png"))
        self.__LamparaRoja=QPixmap(ruta_recurso("imagenes/LamparaRoja.png"))
        self.__LamparaVerde=QPixmap(ruta_recurso("imagenes/LamparaVerde.png"))
        self.__pistones=QPixmap(ruta_recurso("imagenes/esquemabanco_pist.png"))
        self.__ejeposicion=QPixmap(ruta_recurso("imagenes/Eje_posicion.png"))
        self.__eje_flujo=QPixmap(ruta_recurso("imagenes/Eje_flujo.png"))
        self.__Imagen_info=QPixmap(ruta_recurso("imagenes/info_imagen.png"))
        self.__actuador_superior=QPixmap(ruta_recurso("imagenes/actuador_superior.png"))
        self.__cuerpo_actuador=QPixmap(ruta_recurso("imagenes/cuerpo_actuador.png"))
        self.__final_tubo_pvc=QPixmap(ruta_recurso("imagenes/final_tubo_pvc.png"))
        self.__final_vastago=QPixmap(ruta_recurso("imagenes/final_vastago.png"))
        self.__inferior_actuador_=QPixmap(ruta_recurso("imagenes/inferior_actuador_.png"))
        self.__tubo_pvc=QPixmap(ruta_recurso("imagenes/tubo_pvc.png"))
        self.__vastago=QPixmap(ruta_recurso("imagenes/vastago.png"))
        self.__sensor_npn=QPixmap(ruta_recurso("imagenes/sensor_npn.png"))
        self.__vistafrontal_plc=QPixmap(ruta_recurso("imagenes/vistafrontal_plc.png"))
        self.__vistageneral_plc=QPixmap(ruta_recurso("imagenes/vistageneral_plc.png"))
        self.__esquinero=QPixmap(ruta_recurso("imagenes/esquinero.png"))
        self.__driver=QPixmap(ruta_recurso("imagenes/driver.png"))
        self.__sql=QPixmap(ruta_recurso("imagenes/base_datos_icono.png"))
        self.__motor=QPixmap(ruta_recurso("imagenes/motor.png"))
        self.__engranaje_1=QPixmap(ruta_recurso("imagenes/engranaje_1.png"))
        self.__engranaje_2=QPixmap(ruta_recurso("imagenes/engranaje_2.png"))
        self.__engranaje_3=QPixmap(ruta_recurso("imagenes/engranaje_3.png"))
        self.__plc_inicio=QPixmap(ruta_recurso("imagenes/controlador.png"))
        self.__cremallera=QPixmap(ruta_recurso("imagenes/cremallera.png"))
        self.__ordenador=QPixmap(ruta_recurso("imagenes/ordenador.png"))
        self.__imagen_inicio=QPixmap(ruta_recurso("imagenes/imagen_inicio.png"))
        self.__comparar_simulacion=QPixmap(ruta_recurso("imagenes/comparar_simulaciones.png"))

        self.__engranaje_images=[self.__engranaje_1, self.__engranaje_2, self.__engranaje_3]
        self.__indice_engranaje=0        
        self.__posicion_anterior=0

        self.__Leei.setPixmap(self.__eei)
        self.__Luvigo.setPixmap(self.__uvigo)
        self.__LImagenInfoDatos.setPixmap(self.__Imagen_info)
        self.__LImagenInfoDatos_2.setPixmap(self.__Imagen_info)
        self.__LImagenInfoDatos_3.setPixmap(self.__Imagen_info)
        self.__LImagenInfoMotor.setPixmap(self.__Imagen_info)
        self.__LinfoEcuacion.setPixmap(self.__Imagen_info)

        self.__transparente=QPixmap(self.__final_tubo_pvc.size())
        self.__transparente.fill(Qt.transparent)
        self.__pinto=QPainter(self.__transparente)
        self.__pinto.setOpacity(0.55)  
        self.__pinto.drawPixmap(0, 0, self.__final_tubo_pvc)
        self.__pinto.end()
        self.__Lfin_tubo.setPixmap(self.__transparente)

        self.__Lsensor_npn_2.setPixmap(self.__sensor_npn)
        self.__Lsensor_npn_4.setPixmap(self.__sensor_npn)
        self.__roto_sensor=QTransform().rotate(180)
        self.__sensor_npn_rotado=self.__sensor_npn.transformed(self.__roto_sensor)
        self.__Lsensor_npn_1.setPixmap(self.__sensor_npn_rotado)
        self.__Lsensor_npn_3.setPixmap(self.__sensor_npn_rotado)
         
        self.__Lsuperior_actuador.setPixmap(self.__actuador_superior)
        self.__Lsuperior_actuador_2.setPixmap(self.__actuador_superior)
        self.__Lsuperior_actuador_3.setPixmap(self.__actuador_superior)
        self.__Lsuperior_actuador_4.setPixmap(self.__actuador_superior)

        self.__Lactuador.setPixmap(self.__cuerpo_actuador)
        self.__Lactuador_2.setPixmap(self.__cuerpo_actuador)
        self.__Lactuador_3.setPixmap(self.__cuerpo_actuador)
        self.__Lactuador_4.setPixmap(self.__cuerpo_actuador)

        self.__Lvastago.setPixmap(self.__vastago)
        self.__Lvastago_2.setPixmap(self.__vastago)
        self.__Lvastago_3.setPixmap(self.__vastago)
        self.__Lvastago_4.setPixmap(self.__vastago)

        self.__Lfin_vastago.setPixmap(self.__final_vastago)
        self.__Lfin_vastago_2.setPixmap(self.__final_vastago)
        self.__Lfin_vastago_3.setPixmap(self.__final_vastago)
        self.__Lfin_vastago_4.setPixmap(self.__final_vastago)

        self.__Linferior_actuador.setPixmap(self.__inferior_actuador_)
        self.__Linferior_actuador_2.setPixmap(self.__inferior_actuador_)
        self.__Linferior_actuador_3.setPixmap(self.__inferior_actuador_)
        self.__Linferior_actuador_4.setPixmap(self.__inferior_actuador_)

        self.__Lesquinero.setPixmap(self.__esquinero)
        self.__Lesquinero_2.setPixmap(self.__esquinero)

        self.__Ltubo.setPixmap(self.__tubo_pvc)
        self.__Ltubo_2.setPixmap(self.__tubo_pvc)

        self.__Lsensor1.setPixmap(self.__LamparaRoja)
        self.__Lsensor2.setPixmap(self.__LamparaRoja)
        self.__Lsensor1_2.setPixmap(self.__LamparaRoja)
        self.__Lsensor2_2.setPixmap(self.__LamparaRoja)

        self.__Lvistafrontal_plc.setPixmap(self.__vistafrontal_plc)
        self.__Lvistageneral_plc.setPixmap(self.__vistageneral_plc)

        self.__Lcremallera.setPixmap(self.__cremallera)
        self.__Lcremallera_2.setPixmap(self.__cremallera)

        self.__Lmotor.setPixmap(self.__motor)

        self.__Ldriver.setPixmap(self.__driver)

        self.__Lplc_inicio.setPixmap(self.__plc_inicio)

        self.__Lsql.setPixmap(self.__sql)

        self.__Lengranaje.setPixmap(self.__engranaje_1)

        self.__Limagen_inicio.setPixmap(self.__imagen_inicio)

        self.__Lordenador.setPixmap(self.__ordenador)

        self.__Llampara_datos_inicio.setPixmap(self.__LamparaRoja)

        self.__Limagen_comparacion_inicio.setPixmap(self.__comparar_simulacion)

        self.__Lmovimiento_2.setPixmap(self.__LamparaGris)
        self.__Lmovimiento_3.setPixmap(self.__LamparaGris)
        self.__Lmovimiento_5.setPixmap(self.__LamparaGris)
        self.__Lmovimiento_6.setPixmap(self.__LamparaGris)
        self.__Lmovimiento_7.setPixmap(self.__LamparaGris)
        self.__Lmovimiento_8.setPixmap(self.__LamparaGris)

        #Instrucciones
        self.__instrucciones = """
        <b>Instrucciones para la Ecuación:</b><br>
        Las ecuaciones definen la posición en milímetros (mm) a lo largo del tiempo.<br>
        <ul>
            <li><b>t</b>: Tiempo actual (segundos).</li>
            <li><b>A</b>: Amplitud configurada (ej: 345). Es el valor máximo deseado.</li>
            <li><b>V</b>: Factor de velocidad (Velocidad% / 100). Ej: 0.15</li>
        </ul>
         
        <b>Funciones Disponibles:</b><br>
        <tt>sin, cos, tan, abs, exp, log10, sqrt, pow, pi</tt><br><br>

        <b>Ejemplos Recomendados :</b><br>
        <ul>
            <li><b>Onda Senoidal Suave (0 a A):</b><br>
            <i>Sube y baja suavemente usando todo el recorrido.</i><br>
            <tt>(A/2) * (1 - cos(2*pi*V*t))</tt></li>
             
            <li><b>Rebote Amortiguado (Empieza en 0):</b><br>
            <i>Saltos que pierden altura con el tiempo.</i><br>
            <tt>A * abs(sin(t*pi*V)) * exp(-t*0.1)</tt></li>
             
            <li><b>Tren de Pulsos (Burbujas):</b><br>
            <i>Picos suaves separados por pausas.</i><br>
            <tt>A * exp(-(((t*V)%1) - 0.5)**2 * 30)</tt></li>
        </ul>
        """

        self.__LinfoEcuacion.setToolTip(self.__instrucciones)
        self.__Eecuacion.setToolTip(self.__instrucciones)

        #acerca de
        self.__html_acerca_de = """
        <div style="margin: 10px;">
            <h2 style="color: #0078D4;">Banco de Ensayos para Espirometría</h2>
            <p><b>Versión:</b> 1.0 <br>
            <b>Licencia:</b> MIT License (Código Abierto)</p>

            <hr>

            <h3>Autor</h3>
            <p><b>Ing. José Alberto García Valiño</b><br>
            Contacto: <a href="mailto:albertogarva02@gmail.com">albertogarva02@gmail.com</a><br>
            LinkedIn: <a href="https://www.linkedin.com/in/josealbertogarciavalino">Ver Perfil Profesional</a><br>
            Escuela de Ingeniería Industrial - Universidad de Vigo</p>

            <h3>Descripción del Sistema</h3>
            <p align="justify">
            Software de control para banco de pruebas de espirometría. 
            El sistema permite la generación de perfiles de movimiento basados en curvas 
            fisiológicas (NHANES III), control del servomotor vía Modbus TCP, adquisición 
            de señales de flujo en tiempo real y reproducibilidad, así como análisis comparativo de datos médicos.
            </p>

            <h3>Tecnologías Utilizadas</h3>
            <ul>
                <li><b>Core:</b> Python 3 + PySide6 (Qt)</li>
                <li><b>Comunicación Industrial:</b> PyModbusTCP & PyWinUSB</li>
                <li><b>Análisis de Datos:</b> Pandas, NumPy, SciPy</li>
                <li><b>Base de Datos:</b> MySQL</li>
            </ul>

            <p style="font-size: 15px; color: gray;">
            Copyright © 2025 José Alberto García Valiño. Todos los derechos reservados.
            </p>
        </div>
        """

        self.__L_contenido_acerca_de.setText(self.__html_acerca_de)
        self.__L_contenido_acerca_de.setWordWrap(True)        
        self.__L_contenido_acerca_de.setOpenExternalLinks(True)  

        #SETAS EMERGENCIA; 
        self.__botones_seta = [
            self.__Bseta_inicio,
            self.__Bseta_superior_izquierda,
            self.__Bseta_superior_derecha
        ]
        for boton in self.__botones_seta:
                boton.clicked.connect(self._manejar_parada_emergencia)
        self.__Bseta_ok.clicked.connect(self._manejar_rearme)

        #llamada a funciones
        self.__Brealizarmovimiento.clicked.connect(self.BrealizarmovimientoClick)
        self.__Bdetenermovimiento.clicked.connect(self.BdetenermovimientoClick)
        self.__Bejecutarsimulacion.clicked.connect(self.BejecutarsimulacionClick)
        self.__Bdetenersimulacion.clicked.connect(self.BdetenersimulacionClick)
        self.__Banadirdatos.clicked.connect(self.BanadirdatosClick)
        self.__Beliminardatos.clicked.connect(self.BeliminardatosClick)
        self.__Banadirpatologia.clicked.connect(self.BanadirpatologiaClick)
        self.__Cdatospaciente.stateChanged.connect(self.CheckCdatospaciente)
        self.__RBtomarmedidas.clicked.connect(self.RBtomarmedidasTrue)
        self.__Bcomenzarmedida.clicked.connect(self.BcomenzarmedidasClick)
        self.__Bfinalizarmedida.clicked.connect(self.BfinalizarmedidaClick)
        self.__RBgenerarsimulacion.clicked.connect(self.RBgenerarsimulacionTrue)
        self.__RBcargarvalores.clicked.connect(self.RBcargarvaloresClick)
        self.__Bseleccionararchivo.clicked.connect(self.BseleccionararchivoClick)
        self.__Bconfigurar_conexion_inicio.clicked.connect(lambda: self.__tab_pestanas.setCurrentWidget(self.__pagina_comunicacion))
        self.__Bcontrol_manual_motor_inicio.clicked.connect(lambda: self.__tab_pestanas.setCurrentWidget(self.__pagina_controlmotor))
        self.__Brealizar_simulacion_inicio.clicked.connect(lambda: self.__tab_pestanas.setCurrentWidget(self.__pagina_realizarsimulacion))
        self.__Bdatos_inicio.clicked.connect(lambda: self.__tab_pestanas.setCurrentWidget(self.__pagina_mostrardatos))
        self.__Bcomparar_simulaciones_inicio.clicked.connect(lambda: self.__tab_pestanas.setCurrentWidget(self.__pagina_compararsimulaciones))
        self.__Banadir_simulacion_inicio.clicked.connect(lambda: self.__tab_pestanas.setCurrentWidget(self.__pagina_anadirsimulacion))
        self.__Bayuda_inicio.clicked.connect(lambda: self.__tab_pestanas.setCurrentWidget(self.__pagina_ayuda))
        self.__Bacerca_de_inicio.clicked.connect(lambda: self.__tab_pestanas.setCurrentWidget(self.__pagina_acerca_de))
        self.__Bcalibrar.clicked.connect(self.__on_calibrar_click)
        self.__Bcalibrar_2.clicked.connect(self.__on_calibrar_click)
        self.__Bcalibrar_3.clicked.connect(self.__on_calibrar_click)
        self.__Bguardarprueba.clicked.connect(self.__guardar_prueba_click)

        #inicializo graficas
        self.__graficamedidas=CGraficas(self.__ventana, 0, 10, -10, 15, "graficamedidas", "Volumen [L]", "Flujo [L/s]", "Curva Flujo-Volumen")
        self.__graficamedidas.otraGrafica(QColor(50, 100, 255, 255))

        self.__graficasimulacion_flujo_volumen=CGraficas(self.__ventana, 0, 7, -10, 10, "graficasimulacion_flujo_volumen", "Volumen [L]", "Flujo [L/s]", "Curva Flujo-Volumen")
        self.__graficasimulacion_flujo_volumen.otraGrafica(QColor(0, 201, 87, 255))
        self.__graficasimulacion_flujo_volumen.otraGrafica(QColor(178, 34, 34, 255))

        self.__graficamotor=CGraficas(self.__ventana, 0, 10, -10, 350, "graficamotor", "Tiempo [s]", "Amplitud [mm]", "Curva Posición-Tiempo")
        self.__graficamotor.otraGrafica(QColor(0, 201, 87, 255))
        self.__graficamotor.otraGrafica(QColor(178, 34, 34, 255))

        self.__graficasimulacion_volumen_tiempo=CGraficas(self.__ventana, 0, 15, -1, 15, "graficasimulacion_volumen_tiempo", "Tiempo [s]", "Volumen [L]", "Curva Volumen-Tiempo")
        self.__graficasimulacion_volumen_tiempo.otraGrafica(QColor(0, 201, 87, 255))
        self.__graficasimulacion_volumen_tiempo.otraGrafica(QColor(178, 34, 34, 255))

        self.__graficacomparacion_flujo_volumen = CGraficas(self.__ventana, 0, 7, -10, 15, "graficacomparacion_flujo_volumen", "Volumen [L]", "Flujo [L/s]", "Comparación Curvas Flujo-Volumen")
         
        self.__graficavariable=CGraficas(self.__ventana, 0, 10, -10, 10, "graficavariable", "" , "", "Gráfica de Variable")

        #Precargo gráfica 
        self.__MAX_SIMS_COMPARACION=100 
         
        for i in range(self.__MAX_SIMS_COMPARACION):
            color = self.__generar_color_distinto(i, self.__MAX_SIMS_COMPARACION)
            self.__graficacomparacion_flujo_volumen.otraGrafica(color)

        self.__mapa_indices_comparacion = {}

        #inicializo 
        self.__CBedad.setEnabled(False)
        self.__CBpeso.setEnabled(False)
        self.__CBsexo.setEnabled(False)
        self.__CBpatologia.setEnabled(False)
        self.__CBfumador.setEnabled(False)
        self.__CBaltura.setEnabled(False)

        self.__Enombrepaciente.setEnabled(False)
        self.__Eecuacion.setEnabled(False)
        self.__Edni.setEnabled(False)

        self.__LinfoEcuacion.setVisible(False)

        self.__Bcomenzarmedida.setEnabled(True)
        self.__Bfinalizarmedida.setEnabled(False)
        self.__Banadirdatos.setEnabled(True)
        self.__Bdetenersimulacion.setEnabled(False)
        self.__Bdetenermovimiento.setEnabled(False)
        self.__Bseleccionararchivo.setEnabled(False)
         
        self.__RBgenerarsimulacion.setEnabled(False)
        self.__RBtomarmedidas.setAutoExclusive(False)
        self.__RBtomarmedidas.setChecked(True)
        self.__RBtomarmedidas.setAutoExclusive(True)

        self.__Bguardarprueba.setEnabled(False)

        #matriz de valores para edad
        self.__edad=[]
        for i in range(18, 90):
            self.__edad.append(i+1)

        #matriz de valores para peso
        self.__peso=[]
        for i in range(40,200):
            self.__peso.append(i+1)

        #matriz de valores para altura
        self.__altura=[]
        for i in range(140, 210):
            self.__altura.append(i+1)

        #matriz de valores para % de velocidad
        self.__velocidad=[]
        for i in range(5, 100):
            self.__velocidad.append(i+1)

        # matriz de valores para amplitud
        self.__amplitud=[]
        for i in range(345):
            self.__amplitud.append(i + 1)

        #valores Combox;
        self.__CBedad.addItems([str(i) for i in self.__edad])
        self.__CBpeso.addItems([str(i) for i in self.__peso])
        self.__CBaltura.addItems([str(i) for i in self.__altura])
        self.__CBvelocidad.addItems([str(i) for i in self.__velocidad])
        self.__CBamplitud.addItems([str(i) for i in self.__amplitud])
        self.__CBsexo.addItems(["Hombre", "Mujer"])
        self.__CBmovimientospredefinidos.addItems(["Onda Senoidal", "Onda Respiración (Rect 1/2 Onda)", "Onda Rectificada", "-"])
        self.__CBfumador.addItems(["NO", "SI"])

        #valores predefinidos en la tabla de datos
        self.__datos.setColumnCount(11)
        self.__datos.setHorizontalHeaderLabels(["Simulación", "Nombre Paciente", "Edad [años]", "Peso [Kg]", "Altura [cm]",
                                                                "Sexo [Hombre / Mujer]", "DNI", "Fumador [SI / NO]", "Fecha Creación",
                                                                "Patología", "Valores"])

        #inicializar sin valores CB
        self.__CBedad.setCurrentIndex(-1)
        self.__CBpeso.setCurrentIndex(-1)
        self.__CBsexo.setCurrentIndex(-1)
        self.__CBpatologia.setCurrentIndex(0)
        self.__CBfumador.setCurrentIndex(-1)
        self.__CBaltura.setCurrentIndex(-1)

        self.__Edireccion_ip.setText("192.168.0.250")

        self.__Epuerto.setText("502")
         
        #para saber cuando utilizar nueva ecuación y no una ya definida
        self.__CBmovimientospredefinidos.currentIndexChanged.connect(self.__controlar_estado_ecuacion)

        # Variables para almacenar las funciones externas
        self.__funcion_guardar=None
        self.__funcion_eliminar=None
        self.__funcion_anadir_patologia=None
        self.__realizar_movimiento=False
        self.__Posicioninicial=False
        self.__toma_medida=False
        self.__posicion=None
        self.__bajada=None
        self.__reinicio_motor_solicitado=False
        self.__datos_cargados_desde_archivo = None
        self.__funcion_descargar = None
        self.__funcion_obtener_datos_sim = None
        self.__funcion_descargar_comparativa = None
        self.__funcion_conectar_plc = None
        self.__funcion_desconectar_plc = None
        self.__funcion_escribir_plc = None
        self.__funcion_cambio_variable_grafica = None
        self.__numero_simulaciones=0
        self.__funcion_calibrar = None
        self.__max_vol_fv = 1.0
        self.__max_flujo_fv = 1.0
        self.__min_flujo_fv = -1.0
        self.__funcion_parada_emergencia = None
        self.__funcion_rearme_emergencia = None
        self.__funcion_guardar_prueba = None
         
        self.__max_tiempo_vt = 1.0
        self.__max_vol_vt = 1.0

        self.historial_fv_consigna = [] 
        self.historial_fv_real = []     
         
        self.historial_vt_consigna = [] 
        self.historial_vt_real = []       

        self.__cache_ansys_in = {}
        self.__cache_ansys_out = {}

        self.__precargar_imagenes_ansys()

        self.__todas_las_lamparas = [
            self.__Lmovimiento_2, self.__Lmovimiento_3, self.__Lmovimiento_4,
            self.__Lmovimiento_5, self.__Lmovimiento_6, self.__Lmovimiento_7,
            self.__Lmovimiento_8, self.__Lmovimiento_superior_izq,
            self.__Lmovimiento_superior_derch, self.__Lsensor1, self.__Lsensor2,
            self.__Lsensor1_2, self.__Lsensor2_2, self.__Lestado_lampara,
            self.__Llampara_controlador_1, self.__Llampara_controlador_2,
            self.__Llampara_controlador_3, self.__Llampara_controlador_4,
            self.__Llampara_controlador_5, self.__Llampara_controlador_6,
            self.__Llampara_controlador_7, self.__Llampara_controlador_8,
            self.__Llampara_datos_inicio, self.__Llampara_plc_inicio,
            self.__Llampara_configurar_conexion, self.__Llampara_configurar_realizarsimulacion,
            self.__Llampara_configurar_compararsimulaciones]
        
        self.__timer_emergencia_gui = QTimer(self.__ventana)
        self.__timer_emergencia_gui.setInterval(250) 
        self.__timer_emergencia_gui.timeout.connect(self.__parpadeo_rojo_alarma)
        self.__estado_parpadeo = False

        # Variable para controlar el modo
        self.__es_modo_simulacion = False

        # Conectar botones a las funciones correspondientes
        self.__Banadirdatos.clicked.connect(self.__guardar_datos_click)
        self.__Beliminardatos.clicked.connect(self.__eliminar_datos_click)
        self.__Banadirpatologia.clicked.connect(self.__anadir_patologia_click)
        self.__Bdescargar.clicked.connect(self.__descargar_click)
        self.__Bdescargar_2.clicked.connect(self.__descargar_comparativa_click)
        self.__Bconectar.clicked.connect(self.__on_conectar_plc_click)
        self.__Bdesconectar.clicked.connect(self.__on_desconectar_plc_click)
        self.__Bescribir.clicked.connect(self.__on_escribir_plc_click)
         

        #Conexion con funciones
        self.__Efiltrar_simulaciones.textChanged.connect(self.__filtrar_lista_comparacion)
        self.__LW_comparar_simulaciones.itemSelectionChanged.connect(self.__actualizar_grafica_comparacion)
        self.__CBvariable.currentIndexChanged.connect(self.__on_variable_grafica_change)

        # Ayuda_pdf
        self.__diseno_pdf = QVBoxLayout(self.__contenedor_pdf)
        self.__diseno_pdf.setContentsMargins(0, 0, 0, 0)
        self.__contenedor_pdf.setLayout(self.__diseno_pdf)
        self.__visor_pdf = QPdfView()
        self.__documento_pdf = QPdfDocument(self.__ventana)
        self.__visor_pdf.setPageMode(QPdfView.PageMode.MultiPage)
        self.__visor_pdf.setDocument(self.__documento_pdf)
        self.__ruta_pdf = ruta_recurso("documentos/MANUAL_USUARIO_BANCO_ESPIROMETRIA.pdf")
        self.__documento_pdf.load(self.__ruta_pdf)
        self.__diseno_pdf.addWidget(self.__visor_pdf)

#------------Botones emergencia-------------------------
    def activar_modo_emergencia_gui(self):
        self.limpiarGraficaMedidas()
        self.limpiaGraficaSimulacion_flujo_volumen()
        self.limpiarGraficaMotor()
        self.limpiarGraficaSimulacion_volumen_tiempo()
        self.limpiar_grafica_tendencia()
        self.__graficacomparacion_flujo_volumen.limpiar_datos2()
        
        botones = self.__ventana.findChildren(QPushButton)
        for boton in botones:
            boton.setEnabled(False)
        
        self.__Bseta_ok.setEnabled(True)
        
        for seta in self.__botones_seta:
            seta.setEnabled(False) 
            seta.setChecked(True)

        texto_emergencia = "!!! PARADA DE EMERGENCIA !!!"
        
        estilo_emergencia = """
            background-color: red; 
            color: white; 
            font-weight: bold; 
            font-size: 14px; 
            border-radius: 4px;
            padding: 5px;
        """
        
        labels_a_alertar = [
            self.__Lcontrolinformacion,
            self.__Linfoanadireliminardatos,
            self.__Linfodatos,
            self.__Lestado_texto,
            self.__Linfosimulacion 
        ]

        for label in labels_a_alertar:
            label.setText(texto_emergencia)
            label.setAlignment(Qt.AlignCenter) 
            label.setStyleSheet(estilo_emergencia)

        if not self.__timer_emergencia_gui.isActive():
            self.__timer_emergencia_gui.start()

    def desactivar_modo_emergencia_gui(self):
        self.__timer_emergencia_gui.stop()
        
        botones = self.__ventana.findChildren(QPushButton)
        for boton in botones:
            boton.setEnabled(True)

        for seta in self.__botones_seta:
            seta.setChecked(False)
        self.__Bseta_ok.setEnabled(False)

        labels_a_restaurar = [
            self.__Lcontrolinformacion,
            self.__Linfoanadireliminardatos,
            self.__Linfodatos,
            self.__Linfosimulacion 
        ]
        
        for label in labels_a_restaurar:
            label.setText("")       
            label.setStyleSheet("") 
            label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter) 
            
        self.__Lestado_texto.setStyleSheet("") 
        if self.__funcion_conectar_plc: 
            self.__Lestado_texto.setText("Sistema Rearmado. Listo.")

    def __parpadeo_rojo_alarma(self):
        self.__estado_parpadeo = not self.__estado_parpadeo
        
        pixmap_actual = self.__LamparaRoja if self.__estado_parpadeo else self.__LamparaGris
        
        for lampara in self.__todas_las_lamparas:
            lampara.setPixmap(pixmap_actual)

    def _manejar_parada_emergencia(self):
        if self.__funcion_parada_emergencia:
            self.__funcion_parada_emergencia()

    def _manejar_rearme(self):
        if self.__funcion_rearme_emergencia:
            self.__funcion_rearme_emergencia()

    def set_funciones_emergencia(self, funcion_stop, funcion_rearme):
        self.__funcion_parada_emergencia = funcion_stop
        self.__funcion_rearme_emergencia = funcion_rearme

    def __precargar_imagenes_ansys(self):
        ruta_in = "imagenes_in_simetria"
        ruta_out = "imagenes_out_simetria"
        max_in = 200  
        max_out = 100
        
        for i in range(max_in + 1):
            nombre = ruta_recurso( f"{ruta_in}/velocidad_in_{i:04d}_recortada_reflejo.png")
            if QFile.exists(nombre):
                pix = self.__procesar_imagen_ansys(nombre)
                self.__cache_ansys_in[i] = pix

        for i in range(max_out + 1):
            nombre = ruta_recurso(f"{ruta_out}/velocidad_{i:04d}_recortada_reflejo.png")
            if QFile.exists(nombre):
                pix = self.__procesar_imagen_ansys(nombre)
                self.__cache_ansys_out[i] = pix
                
        print("Caché de imágenes cargada.")

    def __procesar_imagen_ansys(self, ruta):
        pixmap_original = QPixmap(ruta)
        if pixmap_original.isNull(): return QPixmap()
        
        transform = QTransform().rotate(270)
        pixmap_rotado = pixmap_original.transformed(transform, Qt.SmoothTransformation)
        
        pixmap_final = QPixmap(pixmap_rotado.size())
        pixmap_final.fill(Qt.transparent)
        
        painter = QPainter(pixmap_final)
        painter.setOpacity(0.5) 
        painter.drawPixmap(0, 0, pixmap_rotado)
        painter.end()
        
        return pixmap_final

    def mostrar_frame_ansys_in(self, indice_frame):
        if indice_frame in self.__cache_ansys_in:
            self.__Lin.setPixmap(self.__cache_ansys_in[indice_frame])

    def mostrar_frame_ansys_out(self, indice_frame):
        if indice_frame in self.__cache_ansys_out:
            self.__Lout.setPixmap(self.__cache_ansys_out[indice_frame])

    
#---------------------------------------------------------------------------------------------------------------------------

    @property
    def ventana(self):
        return self.__ventana
    @property
    def aplicacion(self):
        return self.__aplicacion

    def cambiovalor(self, valor):
        nuevo_valor=not valor
        return nuevo_valor

    def Lcambiolampara(self, valor, conectado):
        if valor:
            self.__Lmovimiento_2.setPixmap(self.__LamparaAmbar)
            self.__Lmovimiento_3.setPixmap(self.__LamparaAmbar)
            self.__Lmovimiento_4.setPixmap(self.__LamparaAmbar)
            self.__Lmovimiento_5.setPixmap(self.__LamparaAmbar)
            self.__Lmovimiento_6.setPixmap(self.__LamparaAmbar)
            self.__Lmovimiento_7.setPixmap(self.__LamparaAmbar)
            self.__Lmovimiento_8.setPixmap(self.__LamparaAmbar)
            self.__Lmovimiento_superior_izq.setPixmap(self.__LamparaAmbar)
            self.__Lmovimiento_superior_derch.setPixmap(self.__LamparaAmbar)
        else:
            if conectado:
                self.__Lmovimiento_superior_derch.setPixmap(self.__LamparaVerde)
                self.__Lmovimiento_superior_izq.setPixmap(self.__LamparaVerde)
                self.__Lmovimiento_4.setPixmap(self.__LamparaVerde)
            else:
                self.__Lmovimiento_superior_derch.setPixmap(self.__LamparaRoja)
                self.__Lmovimiento_superior_izq.setPixmap(self.__LamparaRoja)
                self.__Lmovimiento_4.setPixmap(self.__LamparaRoja)
            self.__Lmovimiento_2.setPixmap(self.__LamparaGris)
            self.__Lmovimiento_3.setPixmap(self.__LamparaGris)
            self.__Lmovimiento_5.setPixmap(self.__LamparaGris)
            self.__Lmovimiento_6.setPixmap(self.__LamparaGris)
            self.__Lmovimiento_7.setPixmap(self.__LamparaGris)
            self.__Lmovimiento_8.setPixmap(self.__LamparaGris)


    def Lsensor1(self, estado, conectado):
        if not conectado:
            self.__Lsensor1.setPixmap(self.__LamparaRoja)
            self.__Lsensor1_2.setPixmap(self.__LamparaRoja)
        elif estado:
            self.__Lsensor1.setPixmap(self.__LamparaVerde)
            self.__Lsensor1_2.setPixmap(self.__LamparaVerde)
        else:
            self.__Lsensor1.setPixmap(self.__LamparaGris)
            self.__Lsensor1_2.setPixmap(self.__LamparaGris)

    def Lsensor2(self, estado, conectado):
        if not conectado:
            self.__Lsensor2.setPixmap(self.__LamparaRoja)
            self.__Lsensor2_2.setPixmap(self.__LamparaRoja)
        elif estado:
            self.__Lsensor2.setPixmap(self.__LamparaVerde)
            self.__Lsensor2_2.setPixmap(self.__LamparaVerde)
        else:
            self.__Lsensor2.setPixmap(self.__LamparaGris)
            self.__Lsensor2_2.setPixmap(self.__LamparaGris)


#-------------------------------------VENTANA_CONTROL_MOTOR--------------------------------------------------------------

    def set_funcion_calibrar(self, funcion):
        self.__funcion_calibrar = funcion

    def __on_calibrar_click(self):
        if self.__funcion_calibrar:
            dialogo = QMessageBox(self.__ventana)
            dialogo.setWindowTitle("Atención: Calibración de Motor")
            dialogo.setText("El motor se moverá hacia abajo buscando el sensor.")
            dialogo.setInformativeText("Asegúrese de que no hay obstrucciones.\n¿Desea continuar?")
            dialogo.setIcon(QMessageBox.Warning)
            
            bt_si = dialogo.addButton("Sí, Calibrar", QMessageBox.YesRole)
            bt_no = dialogo.addButton("Cancelar", QMessageBox.NoRole)
             
            dialogo.exec()
             
            if dialogo.clickedButton() == bt_si:
                self.__funcion_calibrar()
            else:
                self.agregar_a_log("Calibración cancelada por el usuario.")

    def movimientopistones(self, posicion):
        y_min=120 
        y_max=325 
        y_min_fin=335 
        y_max_fin=540 
        y_min_esquinero=331 
        y_max_esquinero=536 
        y_min_cremallera_2=335 
        y_max_cremallera_2=540 
        
        y_min_inicio=340 
        y_max_inicio=490 
        y_min_fin_inicio=493 
        y_max_fin_inicio=643
        y_min_esquinero_inicio=490 
        y_max_esquinero_inicio=640
        y_min_cremallera=493 
        y_max_cremallera=643  
        self.__imagenes_engranaje=self.__engranaje_images
        cantidad_imagenes=len(self.__imagenes_engranaje)
         
        x_1=self.__Lvastago.x()
        x_2=self.__Lvastago_2.x()
        x_3=self.__Lvastago_3.x()
        x_4=self.__Lvastago_4.x()
        x_1_fin=self.__Lfin_vastago.x()
        x_2_fin=self.__Lfin_vastago_2.x()
        x_3_fin=self.__Lfin_vastago_3.x()
        x_4_fin=self.__Lfin_vastago_4.x()
        x_esquinero=self.__Lesquinero.x()
        x_esquinero_2=self.__Lesquinero_2.x()
        x_cremallera=self.__Lcremallera.x()
        x_cremallera_2=self.__Lcremallera_2.x()

        ancho_1=self.__Lvastago.width()
        ancho_2=self.__Lvastago_2.width()
        ancho_3=self.__Lvastago_3.width()
        ancho_4=self.__Lvastago_4.width()
        ancho_1_fin=self.__Lfin_vastago.width()
        ancho_2_fin=self.__Lfin_vastago_2.width()
        ancho_3_fin=self.__Lfin_vastago_3.width()
        ancho_4_fin=self.__Lfin_vastago_4.width()
        ancho_esquinero=self.__Lesquinero.width()
        ancho_esquinero_2=self.__Lesquinero_2.width()
        ancho_cremallera=self.__Lcremallera.width()
        ancho_cremallera_2=self.__Lcremallera_2.width()

        alto_1=self.__Lvastago.height()
        alto_2=self.__Lvastago_2.height()
        alto_3=self.__Lvastago_3.height()
        alto_4=self.__Lvastago_4.height()
        alto_1_fin=self.__Lfin_vastago.height()
        alto_2_fin=self.__Lfin_vastago_2.height()
        alto_3_fin=self.__Lfin_vastago_3.height()
        alto_4_fin=self.__Lfin_vastago_4.height()
        alto_esquinero=self.__Lesquinero.height()
        alto_esquinero_2=self.__Lesquinero_2.height()
        alto_cremallera=self.__Lcremallera.height()
        alto_cremallera_2=self.__Lcremallera_2.height()

        y_1=y_max-(posicion/330)*(y_max-y_min)
        y_1=max(min(y_1, y_max), y_min)

        y_2=y_max-(posicion/330)*(y_max-y_min)
        y_2=max(min(y_2, y_max), y_min)

        y_3=y_max_inicio-(posicion/330)*(y_max_inicio-y_min_inicio)
        y_3=max(min(y_3, y_max_inicio), y_min_inicio)

        y_4=y_max_inicio-(posicion/330)*(y_max_inicio-y_min_inicio)
        y_4=max(min(y_4, y_max_inicio), y_min_inicio)

        y_1_fin=y_max_fin-(posicion/330)*(y_max_fin-y_min_fin)
        y_1_fin=max(min(y_1_fin, y_max_fin), y_min_fin)

        y_2_fin=y_max_fin-(posicion/330)*(y_max_fin-y_min_fin)
        y_2_fin=max(min(y_2_fin, y_max_fin), y_min_fin)

        y_3_fin=y_max_fin_inicio-(posicion/330)*(y_max_fin_inicio-y_min_fin_inicio)
        y_3_fin=max(min(y_3_fin, y_max_fin_inicio), y_min_fin_inicio)

        y_4_fin=y_max_fin_inicio-(posicion/330)*(y_max_fin_inicio-y_min_fin_inicio)
        y_4_fin=max(min(y_4_fin, y_max_fin_inicio), y_min_fin_inicio)
         
        y_esquinero=y_max_esquinero-(posicion/330)*(y_max_esquinero-y_min_esquinero)
        y_esquinero=max(min(y_esquinero, y_max_esquinero), y_min_esquinero)

        y_esquinero_2=y_max_esquinero_inicio-(posicion/330)*(y_max_esquinero_inicio-y_min_esquinero_inicio)
        y_esquinero_2=max(min(y_esquinero_2, y_max_esquinero_inicio), y_min_esquinero_inicio)

        y_cremallera=y_max_cremallera-(posicion/330)*(y_max_cremallera-y_min_cremallera)
        y_cremallera=max(min(y_cremallera, y_max_cremallera), y_min_cremallera)

        y_cremallera_2=y_max_cremallera_2-(posicion/330)*(y_max_cremallera_2-y_min_cremallera_2)
        y_cremallera_2=max(min(y_cremallera_2, y_max_cremallera_2), y_min_cremallera_2)
         
        if posicion>self.__posicion_anterior:
            direccion_movimiento=1
        elif posicion<self.__posicion_anterior:
            direccion_movimiento=-1
        else:
            direccion_movimiento=0

        if direccion_movimiento!=0:
            self.__indice_engranaje=(self.__indice_engranaje+direccion_movimiento)%cantidad_imagenes
             
            if self.__indice_engranaje<0:
                self.__indice_engranaje+=cantidad_imagenes
             
            self.__Lengranaje.setPixmap(self.__imagenes_engranaje[self.__indice_engranaje])
             
        self.__posicion_anterior=posicion

        self.__Lvastago.setGeometry(x_1, int(y_1), ancho_1, alto_1)
        self.__Lvastago_2.setGeometry(x_2, int(y_2), ancho_2, alto_2)
        self.__Lvastago_3.setGeometry(x_3, int(y_3), ancho_3, alto_3)
        self.__Lvastago_4.setGeometry(x_4, int(y_4), ancho_4, alto_4)

        self.__Lfin_vastago.setGeometry(x_1_fin, int(y_1_fin), ancho_1_fin, alto_1_fin)
        self.__Lfin_vastago_2.setGeometry(x_2_fin, int(y_2_fin), ancho_2_fin, alto_2_fin)
        self.__Lfin_vastago_3.setGeometry(x_3_fin, int(y_3_fin), ancho_3_fin, alto_3_fin)
        self.__Lfin_vastago_4.setGeometry(x_4_fin, int(y_4_fin), ancho_4_fin, alto_4_fin)

        self.__Lesquinero.setGeometry(x_esquinero, int(y_esquinero), ancho_esquinero, alto_esquinero)
        self.__Lesquinero_2.setGeometry(x_esquinero_2, int(y_esquinero_2), ancho_esquinero_2, alto_esquinero_2)

        self.__Lcremallera.setGeometry(x_cremallera, int(y_cremallera), ancho_cremallera, alto_cremallera)
        self.__Lcremallera_2.setGeometry(x_cremallera_2, int(y_cremallera_2), ancho_cremallera_2, alto_cremallera_2)

    def informacion_control_motor(self, texto):
        self.__Lcontrolinformacion.setText(texto)

    def posicioninicial(self):
        return self.__Posicioninicial

    def BrealizarmovimientoClick(self):
        self.__CBseleccionsimulacion.setCurrentIndex(0)
        self.__Brealizarmovimiento.setEnabled(False)
        self.__Bejecutarsimulacion.setEnabled(False)
        self.__Bcalibrar.setEnabled(False)
        self.__Bcalibrar_2.setEnabled(False)
        self.__Bcalibrar_3.setEnabled(False)
        self.__Bdetenermovimiento.setEnabled(True)
        self.__Bdetenersimulacion.setEnabled(True)
        self.__CBmovimientospredefinidos.setEnabled(False)
        self.__Eecuacion.setEnabled(False)
        self.__CBamplitud.setEnabled(False) 
        self.__CBvelocidad.setEnabled(False)
        self.__realizar_movimiento=True
        self.__es_modo_simulacion = False 
        
        return

    def tipomovimientomotor(self):
        tipomovimiento=self.__CBmovimientospredefinidos.currentText()
        return tipomovimiento

    def valoramplitud(self):
        amplitud=self.__CBamplitud.currentText()
        return amplitud

    def valorvelocidad(self):
        velocidad=self.__CBvelocidad.currentText()
        return velocidad

    def BdetenermovimientoClick(self):
        self.__Bdetenermovimiento.setEnabled(False)
        self.__Bdetenersimulacion.setEnabled(False)
        self.__realizar_movimiento=False
        return

    def valor_realizar_movimiento(self):
        return self.__realizar_movimiento

    def fallo_comenzar_medida(self):
        self.__Bcomenzarmedida.setEnabled(True)
        self.__Bfinalizarmedida.setEnabled(False)

    def restablecer_controles_motor(self):
        self.__Brealizarmovimiento.setEnabled(True)
        self.__Bejecutarsimulacion.setEnabled(True)
        self.__Bcalibrar.setEnabled(True)
        self.__Bcalibrar_2.setEnabled(True)
        self.__Bcalibrar_3.setEnabled(True)
        self.__Bdetenermovimiento.setEnabled(False)
        self.__Bdetenersimulacion.setEnabled(False)
        self.__CBmovimientospredefinidos.setEnabled(True)
        self.__CBamplitud.setEnabled(True)   
        self.__CBvelocidad.setEnabled(True)
        if self.__CBmovimientospredefinidos.currentText() == "-":
            self.__Eecuacion.setEnabled(True)
        self.__realizar_movimiento=False

    def verificar_reinicio_motor(self):
        if self.__reinicio_motor_solicitado:
            self.__reinicio_motor_solicitado=False
            return True
        return False
     
    def valorecuacion(self):
        return self.__Eecuacion.text()

    def __controlar_estado_ecuacion(self):
        if self.__CBmovimientospredefinidos.currentText() == "-":
            self.__Eecuacion.setEnabled(True)
            self.__LinfoEcuacion.setVisible(True)
            self.informacion_control_motor("Modo ecuación: Introduce una fórmula usando 't', 'A' (amplitud) y 'V' (velocidad).")
        else:
            self.__Eecuacion.setEnabled(False)
            self.__LinfoEcuacion.setVisible(False)
            self.__Eecuacion.clear()

    def esta_en_modo_simulacion(self):
        return self.__es_modo_simulacion

#-------------------------------------VENTANA_SIMULACIÓN-----------------------------------------------------------------
    def limpiarSeleccionSimulacion(self):
        self.__CBseleccionsimulacion.setCurrentIndex(-1)

    def BejecutarsimulacionClick(self):
        self.__Bejecutarsimulacion.setEnabled(False)
        self.__Brealizarmovimiento.setEnabled(False)
        self.__Bcalibrar.setEnabled(False)
        self.__Bcalibrar_2.setEnabled(False)
        self.__Bcalibrar_3.setEnabled(False)
        self.__Bdetenersimulacion.setEnabled(True)
        self.__Bdetenermovimiento.setEnabled(True)
        self.__realizar_movimiento = True
        self.__es_modo_simulacion = True
        return

    def BdetenersimulacionClick(self):
        self.BdetenermovimientoClick()
        self.__Bejecutarsimulacion.setEnabled(True)
        self.__Brealizarmovimiento.setEnabled(True)
        self.__Bcalibrar.setEnabled(True)
        self.__Bcalibrar_2.setEnabled(True)
        self.__Bcalibrar_3.setEnabled(True)

    def Linfosimulacion(self, datos):
        if not datos:
            self.__Linfosimulacion.setText("")
            return

        if isinstance(datos, str):
            self.__Linfosimulacion.setText(datos)
            return
        try:
            texto = (f"Patologia: {str(datos[0])} | Nombre: {str(datos[1])} | Edad: {str(datos[2])} Años "
                     f"| Peso: {str(datos[3])} Kg | Altura: {str(datos[8])} cm | Sexo: {str(datos[4])} | DNI: {str(datos[5])} "
                     f"| Fumador: {str(datos[6])} | Fecha creación: {str(datos[7])}")
            self.__Linfosimulacion.setText(texto)
        except IndexError:
            self.__Linfosimulacion.setText("Error en formato de datos.")

    def devolversimulacionCB(self):
        simulacion = self.__CBseleccionsimulacion.currentText()
        return simulacion
    
    def set_funcion_guardar_prueba(self, funcion):
        self.__funcion_guardar_prueba = funcion

    def __guardar_prueba_click(self):
        if self.__funcion_guardar_prueba:
            self.__funcion_guardar_prueba()

    def obtener_nombre_prueba_sugerido(self):
        return self.__Enombreprueba.text()

    def set_nombre_prueba_sugerido(self, nombre):
        self.__Enombreprueba.setText(nombre)

    def obtener_datos_grafica_fv_actual(self):
        if self.historial_fv_real:
            return self.historial_fv_real
        return self.historial_fv_real

    def activar_boton_guardar_prueba(self, estado):
        self.__Bguardarprueba.setEnabled(estado)

#--------------------------VENTANA_AÑADIR----------------------------------------------------------
    def Linfoanadireliminardatos(self, parrafo):
        self.__Linfoanadireliminardatos.setText(parrafo)
     
    def set_funcion_guardar(self, funcion):
        self.__funcion_guardar=funcion

    def set_funcion_anadir_patologia(self, funcion):
        self.__funcion_anadir_patologia=funcion

    def __guardar_datos_click(self):
        if self.__funcion_guardar is not None:
            datos=self.BanadirdatosClick()
            if datos:
                self.__funcion_guardar(*datos)

    def __anadir_patologia_click(self):
        if self.__funcion_anadir_patologia is not None:
            anadir, patologia = self.BanadirpatologiaClick()
            if anadir and patologia:
                self.__funcion_anadir_patologia(patologia)

    def mostrarCBnombresimulacion(self, simulaciones):
        self.__CBnombresimulacion.clear()
        self.__CBseleccionsimulacion.clear()
        self.__CBseleccionsimulacion.addItem(" ")

        if self.__LW_comparar_simulaciones:
            self.__LW_comparar_simulaciones.clear()

        self.__mapa_indices_comparacion.clear()

        if simulaciones:
            simulaciones_a_mostrar = simulaciones[:self.__MAX_SIMS_COMPARACION]

            self.__CBnombresimulacion.addItems([str(i) for i in simulaciones])
            self.__CBseleccionsimulacion.addItems([str(i) for i in simulaciones])

            if self.__LW_comparar_simulaciones:
                for index, nombre_sim in enumerate(simulaciones_a_mostrar):
                    self.__mapa_indices_comparacion[str(nombre_sim)] = index
                      
                    color = self.__generar_color_distinto(index, self.__MAX_SIMS_COMPARACION)
                    item = QListWidgetItem(str(nombre_sim))
                    item.setForeground(color) 
                    self.__LW_comparar_simulaciones.addItem(item)

         
        else:
            self.__Linfoanadireliminardatos.setText("Error: No hay simulaciones disponibles.")
            self.__Linfosimulacion.setText("Error: No hay simulaciones disponibles.")

    def mostrarCBnombrespatologias(self, patologias):
        self.__CBpatologia.clear()
        if patologias:
            self.__CBpatologia.addItems([str(i) for i in patologias])
        else:
            self.__Linfoanadireliminardatos.setText("Error: No hay patologías disponibles.")

    def set_simulador(self, simulador):
        self.__simulador_curva=simulador

    def BanadirdatosClick(self):
        self.__Linfoanadireliminardatos.setText("")

        nombresimulacion = self.__Enombresimulacion.text()
        if not nombresimulacion:
            self.__Linfoanadireliminardatos.setText("Error: Simulación sin nombre")
            return None
         
        matriz_datos = "[]" 

        if self.__RBgenerarsimulacion.isChecked():
            # Modo 1: Generar simulación
            if self.__simulador_curva:
                sim_data = self.__simulador_curva.obtener_datos_simulacion()
                matriz_datos = str(sim_data)
            else:
                self.Linfoanadireliminardatos("Error: Datos no conseguidos.")
                return None

        elif self.__RBcargarvalores.isChecked():
            # Modo 2: Cargar desde archivo
            if self.__datos_cargados_desde_archivo:
                matriz_datos = self.__datos_cargados_desde_archivo
            else:
                self.Linfoanadireliminardatos("Error: No hay datos de archivo cargados para guardar.")
                return None

        elif self.__RBtomarmedidas.isChecked():
            # Modo 3: Tomar medidas en tiempo real
            if self.__datos_medidos_en_tiempo_real:
                matriz_datos = self.__datos_medidos_en_tiempo_real
            else:
                self.Linfoanadireliminardatos("Error: No se han tomado medidas para guardar.")
                return None
                  
        if self.__Cdatospaciente.isChecked():
            edad = self.__CBedad.currentText() or None
            peso = self.__CBpeso.currentText() or None
            sexo = self.__CBsexo.currentText() or None
            patologia = self.__CBpatologia.currentText() or None
            altura = self.__CBaltura.currentText() or None
            nombre = self.__Enombrepaciente.text() or None
            dni = self.__Edni.text() or None
            fumador = self.__CBfumador.currentText() or None
        else:
            edad, peso, sexo, patologia, altura, nombre, dni, fumador = (None,) * 8

        return (nombre, edad, peso, sexo, dni, fumador, patologia, altura, matriz_datos, nombresimulacion)

    def RBcargarvaloresClick(self):
        if self.__RBcargarvalores.isChecked():
            self.__Bseleccionararchivo.setEnabled(True)
            self.__Bcomenzarmedida.setEnabled(False)
            self.__Bfinalizarmedida.setEnabled(False)
            self.__Banadirdatos.setEnabled(True)

    def BseleccionararchivoClick(self):
        ruta_archivo, _ = QFileDialog.getOpenFileName()
        if ruta_archivo:
            datos_df, mensaje = cargar_datos_archivo(ruta_archivo)
            self.Linfoanadireliminardatos(mensaje)

            if datos_df is not None:
                lista_de_datos = [(float(volumen), float(flujo)) for volumen, flujo in datos_df.to_numpy()]
                self.__datos_cargados_desde_archivo=str(lista_de_datos)
                self.limpiarGraficaMedidas()
                for volumen, flujo in lista_de_datos:
                    self.meteDatosGraficaMedidas(volumen, flujo)
            else:
                self.__datos_cargados_desde_archivo=None

    def BanadirpatologiaClick(self):
        patologia=self.__Epatologia.text()
        if not patologia:
            self.__Linfoanadireliminardatos.setText("Error: Patología no especificada.")
            return None, None
        anadir=True
        return anadir, patologia

    def CheckCdatospaciente(self):
        if self.__Cdatospaciente.isChecked():
            self.__CBedad.setEnabled(True)
            self.__CBpeso.setEnabled(True)
            self.__CBsexo.setEnabled(True)
            self.__CBpatologia.setEnabled(True)
            self.__Enombrepaciente.setEnabled(True)
            self.__Edni.setEnabled(True)
            self.__CBfumador.setEnabled(True)
            self.__CBaltura.setEnabled(True)
            self.__RBgenerarsimulacion.setEnabled(True)

        else:
            self.__CBedad.setEnabled(False)
            self.__CBpeso.setEnabled(False)
            self.__CBsexo.setEnabled(False)
            self.__CBpatologia.setEnabled(False)
            self.__Enombrepaciente.setEnabled(False)
            self.__Edni.setEnabled(False)
            self.__CBfumador.setEnabled(False)
            self.__CBaltura.setEnabled(False)
            self.__RBgenerarsimulacion.setEnabled(False)

            self.__CBedad.setCurrentIndex(-1)
            self.__CBpeso.setCurrentIndex(-1)
            self.__CBsexo.setCurrentIndex(-1)
            self.__CBpatologia.setCurrentIndex(0)
            self.__CBfumador.setCurrentIndex(-1)
            self.__CBaltura.setCurrentIndex(-1)
            self.__RBgenerarsimulacion.setAutoExclusive(False)
            self.__RBgenerarsimulacion.setChecked(False)
            self.__RBgenerarsimulacion.setAutoExclusive(True)
            self.__RBtomarmedidas.setAutoExclusive(False)
            self.__RBtomarmedidas.setChecked(True)
            self.__RBtomarmedidas.setAutoExclusive(True)
            self.__RBcargarvalores.setAutoExclusive(False)
            self.__RBcargarvalores.setChecked(False)
            self.__RBcargarvalores.setAutoExclusive(True)
            self.__Edni.setText("")
            self.__Enombrepaciente.setText("")

    def RBtomarmedidasTrue(self):
        self.__Bcomenzarmedida.setEnabled(True)
        self.__Bfinalizarmedida.setEnabled(False)
        self.__Banadirdatos.setEnabled(True)
        self.__Bseleccionararchivo.setEnabled(False)

    def RBgenerarsimulacionTrue(self):
        self.__Bseleccionararchivo.setEnabled(False)
        if self.__RBgenerarsimulacion.isChecked():
            self.__toma_medida=False
            self.__Banadirdatos.setEnabled(True)
            
            edad_texto=self.__CBedad.currentText() or None
            altura_texto=self.__CBaltura.currentText() or None
            fumador_texto=self.__CBfumador.currentText() or None
            sexo_texto=self.__CBsexo.currentText() or None
            peso_texto=self.__CBpeso.currentText() or None
            
            patologia_texto = self.__CBpatologia.currentText() or "Ninguna" 

            edad=int(edad_texto) if edad_texto and edad_texto.isdigit() else None
            altura=int(altura_texto) if altura_texto and altura_texto.isdigit() else None
            peso=int(peso_texto) if peso_texto and peso_texto.isdigit() else None

            if (edad is not None and altura is not None and fumador_texto is not None and sexo_texto is not None
                    and peso is not None):
                
                return (edad, altura, fumador_texto, sexo_texto, peso, patologia_texto)
            else:
                return None
        else:
            self.__Linfoanadireliminardatos.setText("")
            return None

    def RBgenerarsimulacionChecked(self):
        if self.__RBgenerarsimulacion.isChecked():
            return True
        return False
     
    def BcomenzarmedidasClick(self):
        self.__Bcomenzarmedida.setEnabled(False)
        self.__Bfinalizarmedida.setEnabled(True)
        self.__toma_medida=True

    def tomarmedida(self):
        return self.__toma_medida

    def BfinalizarmedidaClick(self):
        self.__Bcomenzarmedida.setEnabled(True)
        self.__Bfinalizarmedida.setEnabled(False)
        self.__toma_medida=False

    def valorLfvc(self, fvc):
        self.__Lfvc.setText(str(fvc))

    def valorLfev1(self, Lfev1):
        self.__Lfev1.setText(str(Lfev1))

    def valorLpef(self, pef):
        self.__Lpef.setText(str(pef))

    def valorLfev1_fvc(self, Lfev1_fvc):
        self.__Lfev1_fvc.setText(str(Lfev1_fvc))

    def valorLic(self, Lic):
        self.__Lic.setText(str(Lic))

#------------------------------------VENTANA_MOSTRAR_DATOS---------------------------------------------------------------
    def set_funcion_eliminar(self, funcion):
        self.__funcion_eliminar=funcion
     
    def __eliminar_datos_click(self):
        if self.__funcion_eliminar is None:
            print("Advertencia: función de eliminación no conectada.")
            return

        eliminar, nombre_simulacion = self.BeliminardatosClick()

        if not nombre_simulacion or nombre_simulacion == "-":
            self.Linfoanadireliminardatos("Error: No hay ninguna simulación seleccionada para eliminar.")
            return
         
        dialogo = QMessageBox(self.__ventana)
        dialogo.setWindowTitle("Confirmar Eliminación")
        dialogo.setText(f"¿Seguro que quieres eliminar la simulación '{nombre_simulacion}'?")
        dialogo.setInformativeText("Esta acción es irreversible y todos los datos asociados se perderán permanentemente.")
        dialogo.setIcon(QMessageBox.Warning) 

        dialogo.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        dialogo.button(QMessageBox.Ok).setText("Confirmar")
        dialogo.button(QMessageBox.Cancel).setText("Cancelar")

        respuesta = dialogo.exec()

        if respuesta == QMessageBox.Ok:
            self.__funcion_eliminar(nombre_simulacion)
        else:
            self.Linfoanadireliminardatos("Eliminación cancelada por el usuario.")

    def BeliminardatosClick(self):
        valoreliminar=self.__CBnombresimulacion.currentText()
        eliminar=True
        return eliminar, valoreliminar
     
    def mostrarDatosenTableWidget(self, todoslosdatos):
        if todoslosdatos:
            self.__numero_simulaciones = len(todoslosdatos)
        else:
            self.__numero_simulaciones = 0

        if todoslosdatos:
            self.__datos.setRowCount(len(todoslosdatos))
            for i, fila in enumerate(todoslosdatos):
                for j, dato in enumerate(fila):
                    item=QTableWidgetItem(str(dato))
                    self.__datos.setItem(i, j, item)
            self.__datos.resizeColumnsToContents()

    def Linfodatos(self, texto):
        self.__Linfodatos.setText(texto)

    def set_funcion_descargar(self, funcion):
        self.__funcion_descargar = funcion

    def __descargar_click(self):
        if self.__funcion_descargar:
            nombre_simulacion = self.__CBnombresimulacion.currentText()
             
            if not nombre_simulacion or nombre_simulacion == "-":
                self.Linfosimulacion("Selecciona una simulación para descargar.")
                return

            opciones = QFileDialog.Options()
            opciones |= QFileDialog.DontUseNativeDialog
            ruta_archivo, _ = QFileDialog.getSaveFileName(
                self.__ventana,
                "Guardar simulación como...",
                f"{nombre_simulacion}.xlsx", 
                "Archivos de Excel (*.xlsx);;Todos los archivos (*)",
                options=opciones
            )

            if ruta_archivo:
                self.__funcion_descargar(nombre_simulacion, ruta_archivo)

#------------------------------------------------------------------------------------------------------------------------
    def meteDatosGraficaMedidas(self, volumen, flujo):
            self.__graficamedidas.mete(0, volumen, flujo)

    def limpiarGraficaMedidas(self):
        if self.__graficamedidas:
            self.__graficamedidas.limpiar_datos()

    def limpiaGraficaSimulacion_flujo_volumen(self):
        if self.__graficasimulacion_flujo_volumen:
            self.__graficasimulacion_flujo_volumen.limpiar_datos2()

            self.__max_vol_fv = 1.0
            self.__max_flujo_fv = 1.0
            self.__min_flujo_fv = -1.0
            self.__graficasimulacion_flujo_volumen.setRangoX(0, 1)
            self.__graficasimulacion_flujo_volumen.setRangoY(-1, 1)

            self.historial_fv_consigna = []
            self.historial_fv_real = []

    def limpiarGraficaSimulacion_volumen_tiempo(self):
        if self.__graficasimulacion_volumen_tiempo:
            self.__graficasimulacion_volumen_tiempo.limpiar_datos2()

            self.__max_tiempo_vt = 1.0
            self.__max_vol_vt = 1.0
            self.__graficasimulacion_volumen_tiempo.setRangoX(0, 1)
            self.__graficasimulacion_volumen_tiempo.setRangoY(0, 1)

            self.historial_vt_consigna = []
            self.historial_vt_real = []

    def limpiarGraficaMotor(self):
        if self.__graficamotor:
            self.__graficamotor.limpiar_datos2()

    def meteDatosGraficaSimulacion_flujo_volumen(self, consignavolumen, consignaflujo, volumenmedido=None, flujomedido=None):
        self.historial_fv_consigna.append((consignavolumen, consignaflujo))
        if volumenmedido is not None and flujomedido is not None:
            self.historial_fv_real.append((volumenmedido, flujomedido))

        self.__graficasimulacion_flujo_volumen.mete2(0, consignavolumen, consignaflujo)
        if volumenmedido is not None and flujomedido is not None:
            self.__graficasimulacion_flujo_volumen.mete2(1, volumenmedido, flujomedido)

        cambio_escala = False
         
        vals_volumen = [consignavolumen]
        vals_flujo = [consignaflujo]
        if volumenmedido is not None: 
            vals_volumen.append(volumenmedido)
            vals_flujo.append(flujomedido)
         
        max_v = max(vals_volumen)
        max_f = max(vals_flujo)
        min_f = min(vals_flujo)

        if max_v > (self.__max_vol_fv * 0.95):
            self.__max_vol_fv = max_v * 1.2
            self.__graficasimulacion_flujo_volumen.setRangoX(0, self.__max_vol_fv)
            cambio_escala = True 
             
        if max_f > (self.__max_flujo_fv * 0.95):
            self.__max_flujo_fv = max_f * 1.2
            cambio_escala = True
         
        if min_f < (self.__min_flujo_fv * 0.95):
            self.__min_flujo_fv = min_f * 1.2
            cambio_escala = True
             
        if cambio_escala:
            self.__graficasimulacion_flujo_volumen.setRangoY(self.__min_flujo_fv, self.__max_flujo_fv)
             
            self.__graficasimulacion_flujo_volumen.limpiar_datos2() 
             
            for v, f in self.historial_fv_consigna:
                self.__graficasimulacion_flujo_volumen.mete2(0, v, f)
            for v, f in self.historial_fv_real:
                self.__graficasimulacion_flujo_volumen.mete2(1, v, f)


    def meteDatosGraficaSimulacion_volumen_tiempo(self, consignatiempo, consignavolumen, tiempomedido=None, volumenmedido=None):

        self.historial_vt_consigna.append((consignatiempo, consignavolumen))
        if tiempomedido is not None and volumenmedido is not None:
            self.historial_vt_real.append((tiempomedido, volumenmedido))

        self.__graficasimulacion_volumen_tiempo.mete2(0, consignatiempo, consignavolumen)
        if tiempomedido is not None and volumenmedido is not None:
            self.__graficasimulacion_volumen_tiempo.mete2(1, tiempomedido, volumenmedido)

        cambio_escala = False
         
        t_actual = consignatiempo
        max_v = max([consignavolumen] + ([volumenmedido] if volumenmedido is not None else []))
         
        if t_actual > (self.__max_tiempo_vt * 0.95):
            self.__max_tiempo_vt = t_actual + 5.0 
            self.__graficasimulacion_volumen_tiempo.setRangoX(0, self.__max_tiempo_vt)
            cambio_escala = True

        if max_v > (self.__max_vol_vt * 0.95):
            self.__max_vol_vt = max_v * 1.2
            self.__graficasimulacion_volumen_tiempo.setRangoY(0, self.__max_vol_vt)
            cambio_escala = True
             
        if cambio_escala:
            self.__graficasimulacion_volumen_tiempo.limpiar_datos2()
            for t, v in self.historial_vt_consigna:
                self.__graficasimulacion_volumen_tiempo.mete2(0, t, v)
            for t, v in self.historial_vt_real:
                self.__graficasimulacion_volumen_tiempo.mete2(1, t, v)


    def meteDatosGraficaMotor(self, tiempo ,consignaposicion, posicionreal):
            self.__graficamotor.mete2(0, tiempo, consignaposicion)
            self.__graficamotor.mete2(1, tiempo, posicionreal)
            if consignaposicion is not None and self.__posicion is not None:
                if consignaposicion<self.__posicion:
                    self.__bajada=True
                elif consignaposicion > self.__posicion:
                    self.__bajada=False
                else:
                    self.__bajada=None
            elif consignaposicion is None or consignaposicion==self.__posicion:
                self.__bajada=None
            self.__posicion=consignaposicion
            if tiempo>10:
                self.__graficamotor.setRangoX(tiempo-10, tiempo)

#-------------------COMPARACION SIMULACIONES--------------------------------------------------------------------------------------------------  
     
    def __generar_color_distinto(self, indice, total_elementos):
        if total_elementos == 0 or indice < 0:
            return QColor(100, 100, 100)
        CONSTANTE_PROPORCION = 0.05
        INICIO_MATIZ = 0.5 
         
        matiz_flotante = (INICIO_MATIZ + (indice * CONSTANTE_PROPORCION)) % 1.0
        matiz = int(matiz_flotante * 255)
        saturacion = 200 + (indice % 2) * 20 
        valor = 150 + (indice % 3) * 30      
         
        return QColor.fromHsv(matiz, saturacion, valor)
     
    def __filtrar_lista_comparacion(self, texto_filtro):
        for i in range(self.__LW_comparar_simulaciones.count()):
            elemento = self.__LW_comparar_simulaciones.item(i) 
            nombre_simulacion = elemento.text()
             
            if texto_filtro.lower() in nombre_simulacion.lower():
                elemento.setHidden(False)
            else:
                elemento.setHidden(True)

    def __actualizar_grafica_comparacion(self):
        self.__graficacomparacion_flujo_volumen.limpiar_datos2()
         
        elementos_seleccionados = self.__LW_comparar_simulaciones.selectedItems() 
         
        for elemento in elementos_seleccionados: 
            nombre_simulacion = elemento.text()
            indice_grafica = self.__mapa_indices_comparacion.get(nombre_simulacion)

            if indice_grafica is not None:
                 
                datos_simulacion = None
                if self.__funcion_obtener_datos_sim:
                    datos_simulacion = self.__funcion_obtener_datos_sim(nombre_simulacion)
                 
                if datos_simulacion:
                    for volumen, flujo in datos_simulacion:
                        self.__graficacomparacion_flujo_volumen.mete2(indice_grafica, volumen, flujo)
                else:
                    print(f"Advertencia: No se pudieron obtener datos para '{nombre_simulacion}'")
            else:
                print(f"Advertencia: No se encontró índice para la simulación '{nombre_simulacion}'")

    def set_funcion_obtener_datos_sim(self, funcion):
        self.__funcion_obtener_datos_sim = funcion

    def set_funcion_descargar_comparativa(self, funcion):
        self.__funcion_descargar_comparativa = funcion

    def __descargar_comparativa_click(self):
        elementos_seleccionados = self.__LW_comparar_simulaciones.selectedItems() 
        if not elementos_seleccionados:
            print("No hay simulaciones seleccionadas para descargar.")
            return
         
        nombres_simulaciones = [elemento.text() for elemento in elementos_seleccionados] 

        opciones = QFileDialog.Options()
        opciones |= QFileDialog.DontUseNativeDialog
        ruta_archivo, _ = QFileDialog.getSaveFileName(
            self.__ventana,
            "Guardar Informe Comparativo como...",
            "Informe_Comparativo.xlsx",
            "Archivos de Excel (*.xlsx);;Todos los archivos (*)",
            options=opciones
        )
         
        if ruta_archivo:
            self.__funcion_descargar_comparativa(nombres_simulaciones, ruta_archivo)


#------------------------------COMUNICACION PLC---------------------------------------------------------------------------------------------
    def set_funcion_conectar_plc(self, funcion):
        self.__funcion_conectar_plc = funcion
         
    def set_funcion_desconectar_plc(self, funcion):
        self.__funcion_desconectar_plc = funcion
         
    def set_funcion_escribir_plc(self, funcion):
        self.__funcion_escribir_plc = funcion

    def set_funcion_cambio_variable_grafica(self, funcion):
        self.__funcion_cambio_variable_grafica = funcion
     
    def obtener_conteo_variable_tendencia(self):
        return self.__CBvariable.count()

    def __on_conectar_plc_click(self):
        if self.__funcion_conectar_plc:
            ip = self.__Edireccion_ip.text()
            puerto = self.__Epuerto.text()
            self.__funcion_conectar_plc(ip, puerto)

    def __on_desconectar_plc_click(self):
        if self.__funcion_desconectar_plc:
            self.__funcion_desconectar_plc()
             
    def __on_variable_grafica_change(self, index):
        if self.__funcion_cambio_variable_grafica:
            self.__funcion_cambio_variable_grafica(index)

    def actualizar_tabla_monitor(self, datos_lista):
        for fila, valor in enumerate(datos_lista):
            if fila < self.__monitor.rowCount():
                self.__monitor.setItem(fila, 2, QTableWidgetItem(str(valor)))

    def obtener_variable_tendencia_idx(self):
        return self.__CBvariable.currentIndex()

    def configurar_tabla_monitor_defaults(self):
        nombres = [
            "Posición Motor",     
            "Sensor Superior",   
            "Sensor Inferior",    
            "Estado",     
            "Código de Error"           
        ]

        registros = [
            "30001", 
            "30002",
            "30003",
            "30004", 
            "30005"  
        ]
        
        self.__monitor.setRowCount(len(nombres))
        
        for i, (nombre, reg) in enumerate(zip(nombres, registros)):
            self.__monitor.setItem(i, 0, QTableWidgetItem(nombre))
            self.__monitor.setItem(i, 1, QTableWidgetItem(reg))
            self.__monitor.setItem(i, 2, QTableWidgetItem("-")) 
        
        self.__CBregistro.clear()
        
        self.__CBregistro.addItem("Control Motor - VR10 (40011)")       
        self.__CBregistro.addItem("Calibrar - VR15 (40016)")      
        self.__CBregistro.addItem("Reset Errores - VR2 (40003)")
        self.__CBregistro.addItem("Longitud Curva (40012)")
        self.__CBregistro.addItem("Duración Curva (40013)")

        self.__CBvariable.clear()
        self.__CBvariable.addItem("Seleccionar Variable...") 
        self.__CBvariable.addItem("Posición [mm]")           
        self.__CBvariable.addItem("Velocidad [mm/s]")        
        self.__CBvariable.addItem("Aceleración [mm/s²]")    
        self.__CBvariable.addItem("Sensor Superior")         
        self.__CBvariable.addItem("Sensor Inferior")    

    def agregar_a_log(self, mensaje):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.__TE_registro_eventos.appendPlainText(f"[{timestamp}] {mensaje}")

    def actualizar_estado_conexion(self, conectado):
        if conectado:
            self.__Lestado_texto.setText("Estado: CONECTADO")
            self.__Lestado_lampara.setPixmap(self.__LamparaVerde)
            self.__Llampara_controlador_1.setPixmap(self.__LamparaVerde)
            self.__Llampara_controlador_2.setPixmap(self.__LamparaVerde)
            self.__Llampara_controlador_3.setPixmap(self.__LamparaVerde)
            self.__Llampara_controlador_4.setPixmap(self.__LamparaVerde)
            self.__Llampara_controlador_5.setPixmap(self.__LamparaVerde)
            self.__Llampara_controlador_6.setPixmap(self.__LamparaVerde)
            self.__Llampara_controlador_7.setPixmap(self.__LamparaVerde)
            self.__Llampara_controlador_8.setPixmap(self.__LamparaVerde)
            self.__Lmovimiento_superior_izq.setPixmap(self.__LamparaVerde)
            self.__Lmovimiento_superior_derch.setPixmap(self.__LamparaVerde)
            self.__Lmovimiento_4.setPixmap(self.__LamparaVerde)
            self.__Llampara_plc_inicio.setPixmap(self.__LamparaVerde)
            self.__Llampara_configurar_conexion.setPixmap(self.__LamparaVerde)
            self.__Bconectar.setEnabled(False)
            self.__Bdesconectar.setEnabled(True)
            self.__Bescribir.setEnabled(True)
            self.__Edireccion_ip.setEnabled(False)
            self.__Epuerto.setEnabled(False)
        else:
            self.__Lestado_texto.setText("Estado: DESCONECTADO")
            self.__Lestado_lampara.setPixmap(self.__LamparaRoja)
            self.__Llampara_controlador_1.setPixmap(self.__LamparaRoja)
            self.__Llampara_controlador_2.setPixmap(self.__LamparaRoja)
            self.__Llampara_controlador_3.setPixmap(self.__LamparaRoja)
            self.__Llampara_controlador_4.setPixmap(self.__LamparaRoja)
            self.__Llampara_controlador_5.setPixmap(self.__LamparaRoja)
            self.__Llampara_controlador_6.setPixmap(self.__LamparaRoja)
            self.__Llampara_controlador_7.setPixmap(self.__LamparaRoja)
            self.__Llampara_controlador_8.setPixmap(self.__LamparaRoja)
            self.__Lmovimiento_superior_izq.setPixmap(self.__LamparaRoja)
            self.__Lmovimiento_superior_derch.setPixmap(self.__LamparaRoja)
            self.__Lmovimiento_4.setPixmap(self.__LamparaRoja)
            self.__Llampara_plc_inicio.setPixmap(self.__LamparaRoja)
            self.__Llampara_configurar_conexion.setPixmap(self.__LamparaRoja)
            self.__Bconectar.setEnabled(True)
            self.__Bdesconectar.setEnabled(False)
            self.__Bescribir.setEnabled(False)
            self.__Edireccion_ip.setEnabled(True)
            self.__Epuerto.setEnabled(True)
             
            for fila in range(self.__monitor.rowCount()):
                item = self.__monitor.item(fila, 2)
                if item:
                    item.setText("-")
                else:
                    self.__monitor.setItem(fila, 2, QTableWidgetItem("-"))

    def limpiar_campo_escritura(self):
        self.__Evalor_registro.clear()
         
    def actualizar_grafica_tendencia(self, eje_t, datos_serie_y):
        if not eje_t or not datos_serie_y or len(eje_t) != len(datos_serie_y):
            return
        self.__graficavariable.limpiar_datos()
        
        tiempo_actual = eje_t[-1]
        tiempo_inicio_visible = max(0, tiempo_actual - 10)
        
        idx_inicio = 0
        total_puntos = len(eje_t)
        
        if total_puntos > 20: 
            for i in range(total_puntos - 1, -1, -5): 
                if eje_t[i] < tiempo_inicio_visible:
                    idx_inicio = i
                    break
        
        visibles_y = datos_serie_y[idx_inicio:]
        
        if visibles_y:
            y_min_vis = min(visibles_y)
            y_max_vis = max(visibles_y)
            
            if y_min_vis == y_max_vis:
                margen = 1.0
            else:
                margen = (y_max_vis - y_min_vis) * 0.1 
            
            self.__graficavariable.setRangoY(y_min_vis - margen, y_max_vis + margen)

        if tiempo_actual < 10:
             self.__graficavariable.setRangoX(0, 10)
        else:
             self.__graficavariable.setRangoX(tiempo_actual - 10, tiempo_actual)

        puntos_a_pintar = 800
        salto = 1
        if total_puntos > puntos_a_pintar:
            salto = total_puntos // puntos_a_pintar

        for i in range(0, total_puntos, salto):
            self.__graficavariable.mete(0, eje_t[i], datos_serie_y[i])
            
        if (total_puntos - 1) % salto != 0:
            self.__graficavariable.mete(0, eje_t[-1], datos_serie_y[-1])

    def limpiar_grafica_tendencia(self):
        self.__graficavariable.limpiar_datos()

     
    def __on_escribir_plc_click(self):
        if self.__funcion_escribir_plc:
            registro_str = self.__CBregistro.currentText()
            valor_str = self.__Evalor_registro.text()
            self.__funcion_escribir_plc(registro_str, valor_str)
            self.limpiar_campo_escritura()

#-----------------------------INICIO------------------------------------------------------------------------------------
    def actualizar_estado_db(self, conectado):
        if conectado:
            self.__Llampara_datos_inicio.setPixmap(self.__LamparaVerde)
        else:
            self.__Llampara_datos_inicio.setPixmap(self.__LamparaRoja)
    
    def actualizar_grafica_tendencia(self, eje_t, datos_serie_y, titulo_grafica="", titulo_eje_y="", titulo_eje_x="Tiempo [s]"):
        
        try:
            if titulo_grafica:
                self.__graficavariable.cambiarTituloGrafica(titulo_grafica)
            if titulo_eje_y:
                self.__graficavariable.cambiarTituloEjeY(titulo_eje_y)
            if titulo_eje_x:
                self.__graficavariable.cambiarTituloEjeX(titulo_eje_x)
        except AttributeError:
            pass 
        if not eje_t or not datos_serie_y or len(eje_t) != len(datos_serie_y):
            return
        
        self.__graficavariable.limpiar_datos()
        
        tiempo_actual = eje_t[-1]
        tiempo_inicio_visible = max(0, tiempo_actual - 10)
        
        idx_inicio = 0
        total_puntos = len(eje_t)
        
        if total_puntos > 20: 
            for i in range(total_puntos - 1, -1, -5): 
                if eje_t[i] < tiempo_inicio_visible:
                    idx_inicio = i
                    break
        
        visibles_y = datos_serie_y[idx_inicio:]
        
        if visibles_y:
            y_min_vis = min(visibles_y)
            y_max_vis = max(visibles_y)
            
            if y_min_vis == y_max_vis:
                margen = 1.0
            else:
                margen = (y_max_vis - y_min_vis) * 0.1 
            
            self.__graficavariable.setRangoY(y_min_vis - margen, y_max_vis + margen)

        if tiempo_actual < 10:
             self.__graficavariable.setRangoX(0, 10)
        else:
             self.__graficavariable.setRangoX(tiempo_actual - 10, tiempo_actual)

        puntos_a_pintar = 800
        salto = 1
        if total_puntos > puntos_a_pintar:
            salto = total_puntos // puntos_a_pintar

        for i in range(0, total_puntos, salto):
            self.__graficavariable.mete(0, eje_t[i], datos_serie_y[i])
            
        if (total_puntos - 1) % salto != 0:
            self.__graficavariable.mete(0, eje_t[-1], datos_serie_y[-1])


    def actualizar_lamparas_inicio(self, plc_conectado):
        if self.__numero_simulaciones >= 1 and plc_conectado:
            self.__Llampara_configurar_realizarsimulacion.setPixmap(self.__LamparaVerde)
        else:
            self.__Llampara_configurar_realizarsimulacion.setPixmap(self.__LamparaRoja)

        if self.__numero_simulaciones >= 2:
            self.__Llampara_configurar_compararsimulaciones.setPixmap(self.__LamparaVerde)
        else:
            self.__Llampara_configurar_compararsimulaciones.setPixmap(self.__LamparaRoja)