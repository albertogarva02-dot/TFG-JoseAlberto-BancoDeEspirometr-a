#_____________________________________________________________________________________________________________________
#    Nombre del Script: plc_modbus.py
#    Autor: José Alberto García Valiño
#    Fecha: 07-12-2025
#    Descripción:
#        Controlador para la comunicación vía protocolo Modbus TCP.
#        Gestiona la conexión, lectura de registros de entrada,
#        escritura de consignas y la transferencia de bloques de datos (arrays)
#        para la inyección de perfiles de movimiento en la memoria del PLC.
#______________________________________________________________________________________________________________________

__author__ = "José Alberto García Valiño"
__copyright__ = "Copyright 2025, José Alberto García Valiño"
__credits__ = ["José Alberto García Valiño"]
__license__ = "MIT"
__version__ = "1.0"
__status__ = "Beta"


from pymodbus.client import ModbusTcpClient

class ControladorPLC:
    def __init__(self):
        self.cliente_modbus = None
        self.conectado = False

    def conectar(self, ip, puerto_str):
        try:
            puerto = int(puerto_str)
        except ValueError:
            raise ValueError("El puerto debe ser un número.")   

        try:
            self.cliente_modbus = ModbusTcpClient(ip, port=puerto, timeout=2)
            self.conectado = self.cliente_modbus.connect()
        except Exception as e:
            self.conectado = False
            raise Exception(f"Error crítico al crear cliente: {e}")

        if not self.conectado:
            raise Exception("Falló la conexión. Revise IP y cableado.")
        return "¡Conexión exitosa!" 

    def desconectar(self):
        if self.cliente_modbus:
            self.cliente_modbus.close()
        self.cliente_modbus = None
        self.conectado = False
        return "Desconectado."

    def leer_registros_entrada(self, direccion_inicio, cantidad):
        if not self.conectado or not self.cliente_modbus:
            raise Exception("No conectado.")
        
        resultado = self.cliente_modbus.read_holding_registers(address=direccion_inicio, count=cantidad, slave=1)

        if resultado.isError():
            raise Exception("Error de lectura Modbus.")

        return resultado.registers 

    def escribir_registro_simple(self, registro_holding, valor_int):
        if not self.conectado or not self.cliente_modbus:
            raise Exception("No conectado.")

        direccion_modbus = registro_holding - 40001
        resultado = self.cliente_modbus.write_register(address=direccion_modbus, value=int(valor_int), slave=1)

        if resultado.isError():
            raise Exception("Error de escritura Modbus.")
        return "¡Escritura completada!"
    
    def escribir_perfil_db(self, direccion_modbus_inicio, lista_de_puntos):
        if not self.conectado or not self.cliente_modbus:
            raise Exception("No conectado.")

        try:
            valores_enteros = [int(punto) for punto in lista_de_puntos]
        except ValueError:
            raise Exception("Error: Todos los puntos deben ser numéricos.")
        
        direccion_base = direccion_modbus_inicio - 1 
        
        #(limite seuridad)
        CHUNK_SIZE = 100 
        total_puntos = len(valores_enteros)
        
        print(f"Iniciando carga de {total_puntos} puntos en bloques de {CHUNK_SIZE}...")

        for i in range(0, total_puntos, CHUNK_SIZE):
            chunk = valores_enteros[i : i + CHUNK_SIZE]
            direccion_actual = direccion_base + i
            
            resultado = self.cliente_modbus.write_registers(
                address=direccion_actual, 
                values=chunk, 
                slave=1
            )
            
            if resultado.isError():
                raise Exception(f"Error escribiendo bloque en dirección {direccion_actual}")
                
        return "¡Perfil cargado exitosamente en la TABLA del PLC!"