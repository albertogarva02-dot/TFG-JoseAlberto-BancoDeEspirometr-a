#_____________________________________________________________________________________________________________________
#    Nombre del Script: cgraficas.py
#    Autor: José Alberto García Valiño
#    Fecha: 07-12-2025
#    Descripción:
#        Clase personalizada para la creación y manipulación de gráficos en PySide6.
#        Configura estilos, ejes, series de datos y renderizado.
#        Facilita la actualización en tiempo real de curvas de flujo, volumen y posición.
#______________________________________________________________________________________________________________________

__author__ = "José Alberto García Valiño"
__copyright__ = "Copyright 2025, José Alberto García Valiño"
__credits__ = ["José Alberto García Valiño"]
__license__ = "MIT"
__version__ = "1.0"
__email__ = "albertogarva02@gmail.com"
__status__ = "Beta"


from PySide6.QtCharts import QLineSeries, QValueAxis
from PySide6.QtCore import Qt, QMargins
from PySide6.QtGui import QColor, QPainter, QBrush, QPen, QFont
from codigos.widgetgrafico import WidgetGrafico

class CGraficas:
    def __init__(self, ventana, xmin, xmax, yLmin, yLmax, rcs, titulo_eje_x, titulo_eje_y, titulo_grafico):
        self.__graficaEnVentana = ventana.findChild(WidgetGrafico, rcs)
        self.__grafica = self.__graficaEnVentana.chart()

        # FONDO
        color_fondo = QColor("#1E1E1E")
        self.__grafica.setBackgroundBrush(QBrush(color_fondo))
        self.__grafica.setPlotAreaBackgroundVisible(False)

        # REJILLA 
        pen_rejilla = QPen(QColor("#2E2E2E")) 
        pen_rejilla.setWidthF(1.0)
        pen_rejilla.setStyle(Qt.SolidLine) 

        # FUENTES Y TÍTULOS
        fuente_titulo = QFont("Segoe UI", 10, QFont.Bold)
        fuente_titulo_principal = QFont("Segoe UI", 12, QFont.Bold)
        
        self.__grafica.setTitle(titulo_grafico)
        self.__grafica.setTitleFont(fuente_titulo_principal)
        self.__grafica.setTitleBrush(QBrush(QColor("#61AFEF")))

        # CONFIGURACIÓN EJES
        
        # === EJE X ===
        self.__ejeX = QValueAxis()
        self.__ejeX.setRange(xmin, xmax)
        self.__ejeX.setTitleText(titulo_eje_x)
        self.__ejeX.setTitleFont(fuente_titulo)
        self.__ejeX.setTitleBrush(QBrush(QColor("#61AFEF")))

        self.__xmin_inicial = xmin
        self.__xmax_inicial = xmax
        
        self.__ejeX.setTickCount(12)       
        self.__ejeX.setMinorTickCount(0)
        
        self.__ejeX.setGridLinePen(pen_rejilla)
        self.__ejeX.setLabelsColor(QColor("#A0A0A0")) 
        self.__ejeX.setLinePenColor(QColor("#404040")) 

        self.__grafica.addAxis(self.__ejeX, Qt.AlignBottom)

        # === EJE Y ===
        self.__ejeYIzquierdo = QValueAxis()
        self.__ejeYIzquierdo.setRange(yLmin, yLmax)
        self.__ejeYIzquierdo.setTitleText(titulo_eje_y)
        self.__ejeYIzquierdo.setTitleFont(fuente_titulo)
        self.__ejeYIzquierdo.setTitleBrush(QBrush(QColor("#61AFEF")))

        self.__ejeYIzquierdo.setTickCount(12)    
        self.__ejeYIzquierdo.setMinorTickCount(0) 
        
        self.__ejeYIzquierdo.setGridLinePen(pen_rejilla)
        self.__ejeYIzquierdo.setLabelsColor(QColor("#A0A0A0"))
        self.__ejeYIzquierdo.setLinePenColor(QColor("#404040"))

        self.__grafica.addAxis(self.__ejeYIzquierdo, Qt.AlignLeft)

        # RESTO CONFIGURACIÓN
        self.__graficaEnVentana.setRenderHint(QPainter.Antialiasing)
        self.__grafica.setMargins(QMargins(0, 0, 0, 0))
        self.__grafica.layout().setContentsMargins(0, 0, 0, 0)
        self.__grafica.legend().hide()
        self.__ejes = []

    def otraGrafica(self, color):
        puntos = QLineSeries()
        pen_linea = QPen(color)
        pen_linea.setWidth(2)
        puntos.setPen(pen_linea)
        
        self.__grafica.addSeries(puntos)
        puntos.attachAxis(self.__ejeX);
        puntos.attachAxis(self.__ejeYIzquierdo)
        self.__ejes.append(puntos)

    def mete(self, eje, x, y):
        if eje < len(self.__ejes):
            self.__ejes[eje].append(x, y)
        else:
            nueva_serie = QLineSeries()
            nueva_serie.append(x, y)
            self.__grafica.addSeries(nueva_serie)
            nueva_serie.attachAxis(self.__ejeX)
            nueva_serie.attachAxis(self.__ejeYIzquierdo)
            self.__ejes.append(nueva_serie)

    def mete2(self, eje, x, y):
        self.__ejes[eje].append(x, y)

    def setRangoX(self, min_val, max_val):
        self.__ejeX.setRange(min_val, max_val)
        for i in self.__ejes:
            if i.count() > 0:
                i.remove(0)

    def setRangoY(self, min_val, max_val):
        """Ajusta dinámicamente el rango vertical de la gráfica"""
        self.__ejeYIzquierdo.setRange(min_val, max_val)

    def cambiarTituloEjeY(self, titulo):
        """Cambia el texto del título del eje Y"""
        self.__ejeYIzquierdo.setTitleText(titulo)

    def resetear_rango_ejes(self):
        self.__ejeX.setRange(self.__xmin_inicial, self.__xmax_inicial)

    def limpiar_datos(self):
        for serie in self.__grafica.series():
            serie.clear()
        self.resetear_rango_ejes()

    def limpiar_datos2(self):
        for serie in self.__ejes:
            serie.clear()
        self.resetear_rango_ejes()

    def cambiarTituloGrafica(self, titulo):
        self.__grafica.setTitle(titulo)

    def cambiarTituloEjeX(self, titulo):
        self.__ejeX.setTitleText(titulo)