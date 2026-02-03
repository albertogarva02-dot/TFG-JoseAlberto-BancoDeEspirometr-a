#_____________________________________________________________________________________________________________________
#    Nombre del Script: db.py
#    Autor: José Alberto García Valiño
#    Fecha: 07-12-2025
#    Descripción:
#        Módulo de bajo nivel que gestiona la conexión directa con el servidor MySQL.
#        Contiene las sentencias SQL crudas para registrar pacientes, insertar valores
#        de simulaciones, consultar patologías y realizar limpiezas de datos.
#______________________________________________________________________________________________________________________

__author__ = "José Alberto García Valiño"
__copyright__ = "Copyright 2025, José Alberto García Valiño"
__credits__ = ["José Alberto García Valiño"]
__license__ = "MIT"
__version__ = "1.0"
__email__ = "albertogarva02@gmail.com"
__status__ = "Beta"


import mysql.connector

class DB:
    def __init__(self):
        self.__conexion = mysql.connector.connect(
            user='root', password='BANCOESPIROMETRIA?1357', host='127.0.0.1', database='bancoespirometria', use_pure=True)
        self.__cursor = self.__conexion.cursor()

    def registraDatos(self, nombre, edad, peso, sexo, dni, fumador, patologia, altura, matrizvalores, nombresimulacion):
        self.__cursor.execute("SELECT COUNT(*) FROM datossimulaciones WHERE nombresimulacion = %s", (nombresimulacion,))
        existe_simulacion = self.__cursor.fetchone()[0]

        if existe_simulacion > 0:
            return "La simulación con el nombre '{}' ya existe.".format(nombresimulacion)

        else:
            if patologia is None:
                patologia="Ninguna"
            self.__cursor.execute("SELECT idpatologias FROM patologias WHERE patologia= %s", (patologia,))
            idPatologia = self.__cursor.fetchone()

            if not idPatologia:
                return f"Error: La patología '{patologia}' no existe en la base de datos."

            self.__cursor.execute(
                "INSERT INTO datospacientes(nombre, edad, peso, sexo, dni, fumador, fecha, idpatologia, altura) "
                "VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s, %s)",
                (nombre, edad, peso, sexo, dni, fumador, idPatologia[0], altura))
            idDatosPaciente = self.__cursor.lastrowid
            self.__cursor.execute("INSERT INTO valores(matrizvalores) VALUES (%s)", (matrizvalores,))
            idMatrizValores = self.__cursor.lastrowid
            self.__cursor.execute(
                "INSERT INTO datossimulaciones(nombresimulacion, idPatologia, idDatosPaciente, idMatrizValores) "
                "VALUES (%s, %s, %s, %s)", (nombresimulacion, idPatologia[0], idDatosPaciente, idMatrizValores))
            self.__conexion.commit()

            return "Datos registrados correctamente."

    def registraPatologias(self, nuevapatologia):
        self.__cursor.execute("SELECT patologia FROM patologias ORDER BY idpatologias")
        patologias = self.__cursor.fetchall()

        if (nuevapatologia,) not in patologias:  
            self.__cursor.execute("INSERT INTO patologias(patologia) VALUES (%s)", (nuevapatologia,))
            self.__conexion.commit()
            return f"Patología '{nuevapatologia}' registrada exitosamente."
        else:
            return f"La patología '{nuevapatologia}' ya existe."

    def consultaPatologias(self):
        self.__cursor.execute("SELECT patologia FROM patologias ORDER BY idpatologias")
        patologiastotales = self.__cursor.fetchall()

        if not patologiastotales:
            return ["-"]
        patologiastotales = [fila[0] for fila in patologiastotales]
        if patologiastotales[0] is None:
            return ["-"]
        return patologiastotales

    def consultaNombresSimulaciones(self):
        self.__cursor.execute("SELECT nombresimulacion FROM datossimulaciones ORDER BY iddatossimulaciones")
        simulacionestotales = self.__cursor.fetchall()
        self.__conexion.commit()
        if not simulacionestotales or simulacionestotales[0][0] is None:
            simulacionestotales = ["-"]
        else:
            simulacionestotales = [fila[0] for fila in simulacionestotales]

        return simulacionestotales

    def consultaDatos(self, nombresimulacion):
        self.__cursor.execute(
            "SELECT idPatologia, idDatosPaciente, idMatrizValores FROM datossimulaciones WHERE nombresimulacion = %s",
            (nombresimulacion,))

        iddatos = self.__cursor.fetchall()
        if not iddatos:
            return "No se encuentran datos"

        self.__cursor.execute("SELECT patologia FROM patologias WHERE idpatologias = %s", (iddatos[0][0],))
        tupatologia = self.__cursor.fetchone()
        patologia = tupatologia[0]

        self.__cursor.execute(
            "SELECT nombre, edad, peso, sexo, dni, fumador, fecha, altura FROM datospacientes WHERE iddatospacientes = %s",
            (iddatos[0][1],))
        tudatospaciente = self.__cursor.fetchone()
        nombre=tudatospaciente[0]
        edad=tudatospaciente[1]
        peso=tudatospaciente[2]
        sexo=tudatospaciente[3]
        dni=tudatospaciente[4]
        fumador=tudatospaciente[5]
        fecha=tudatospaciente[6]
        altura=tudatospaciente[7]
        self.__cursor.execute("SELECT matrizvalores FROM valores WHERE idvalores = %s", (iddatos[0][2],))
        valoressimulacion = self.__cursor.fetchone()
        self.__conexion.commit()
        matrizvalores = valoressimulacion[0]
        return patologia, nombre, edad, peso, sexo, dni, fumador, fecha.strftime("%d/%m/%Y %H:%M:%S"), altura, matrizvalores

    def eliminaDatos(self, nombresimulacion):
        self.__cursor.execute(
            "SELECT idPatologia, idDatosPaciente, idMatrizValores FROM datossimulaciones WHERE nombresimulacion=%s",
            (nombresimulacion,))
        ids_simulacion = self.__cursor.fetchone()

        if ids_simulacion:
            self.__cursor.execute("DELETE FROM datossimulaciones WHERE nombresimulacion=%s", (nombresimulacion,))
            self.__cursor.execute("DELETE FROM datospacientes WHERE iddatospacientes=%s", (ids_simulacion[1],))
            self.__cursor.execute("DELETE FROM valores WHERE idvalores=%s", (ids_simulacion[2],))
            self.__conexion.commit()
            return True
        else:
            return False

    def obtenerTodosLosDatos(self):
        self.__cursor.execute("""SELECT 
            datossimulaciones.nombresimulacion,
            datospacientes.nombre, 
            datospacientes.edad, 
            datospacientes.peso, 
            datospacientes.altura,
            datospacientes.sexo, 
            datospacientes.dni, 
            datospacientes.fumador, 
            datospacientes.fecha, 
            patologias.patologia, 
            valores.matrizvalores
        FROM datospacientes 
        INNER JOIN patologias ON datospacientes.idpatologia = patologias.idpatologias
        INNER JOIN datossimulaciones ON datospacientes.iddatospacientes = datossimulaciones.idDatosPaciente
        INNER JOIN valores ON datossimulaciones.idMatrizValores = valores.idvalores
        ORDER BY datospacientes.fecha DESC""")
        datos = self.__cursor.fetchall()
        if not datos:
            return ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"]
        return datos
