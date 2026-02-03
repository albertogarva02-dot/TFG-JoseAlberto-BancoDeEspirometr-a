#_____________________________________________________________________________________________________________________
#    Nombre del Script: widgetgrafico.py
#    Autor: José Alberto García Valiño
#    Fecha: 07-12-2025
#    Descripción:
#        Widget personalizado que hereda de QChartView para integrar gráficos
#        de QtCharts dentro de la interfaz de usuario PySide6. Sirve como contenedor
#        visual base para todas las representaciones gráficas (curvas F-V, V-T y tendencias).
#______________________________________________________________________________________________________________________

__author__ = "José Alberto García Valiño"
__copyright__ = "Copyright 2025, José Alberto García Valiño"
__credits__ = ["José Alberto García Valiño"]
__license__ = "MIT"
__version__ = "1.0"
__status__ = "Beta"

from PySide6.QtCharts import QChartView

class WidgetGrafico(QChartView):
    def __init__(self, parent=None):
        QChartView.__init__(self, parent)