#_____________________________________________________________________________________________________________________
#    Nombre del Script: db_gui.py
#    Autor: José Alberto García Valiño
#    Fecha: 07-12-2025
#    Descripción:
#        Clase que simplifica las llamadas a la base de datos.
#        Actúa como intermediario para desacoplar la lógica visual de las consultas SQL.
#______________________________________________________________________________________________________________________

__author__ = "José Alberto García Valiño"
__copyright__ = "Copyright 2025, José Alberto García Valiño"
__credits__ = ["José Alberto García Valiño"]
__license__ = "MIT"
__version__ = "1.0"
__status__ = "Beta"


from codigos.db import DB

class DB_GUI:
    def __init__(self):
        self.__ODB_GUI=DB()

    def registradatos(self, nombre, edad, peso, sexo, dni, fumador, patologia, altura, matrizvalores, nombresimulacion):
        texto=self.__ODB_GUI.registraDatos(nombre, edad, peso, sexo, dni, fumador, patologia, altura, matrizvalores, nombresimulacion)
        return texto

    def registrapatologia(self, patologia):
        texto=self.__ODB_GUI.registraPatologias(patologia)
        return texto

    def consultapatologias(self):
        patologias=self.__ODB_GUI.consultaPatologias()
        return patologias

    def consultanombressimulaciones(self):
        simulaciones=self.__ODB_GUI.consultaNombresSimulaciones()
        return simulaciones

    def consultadatos(self, nombresimulacion):
        datos=self.__ODB_GUI.consultaDatos(nombresimulacion)
        return datos

    def eliminadatos(self, nombresimulacion):
        texto=self.__ODB_GUI.eliminaDatos(nombresimulacion)
        return texto

    def obtenerTodosLosDatos(self):
        datos=self.__ODB_GUI.obtenerTodosLosDatos()
        return datos