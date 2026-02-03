#_____________________________________________________________________________________________________________________
#    Nombre del Script: procesador_datos.py
#    Autor: José Alberto García Valiño
#    Fecha: 07-12-2025
#    Descripción:
#        Módulo de análisis de datos encargado de leer archivos externos (.csv, .xlsx).
#        Implementa lógica para detectar formatos médicos (Datospir),
#        normalizar columnas, inferir frecuencias de muestreo y reconstruir series de
#        tiempo/volumen a partir de datos crudos de flujo para su visualización.
#______________________________________________________________________________________________________________________

__author__ = "José Alberto García Valiño"
__copyright__ = "Copyright 2025, José Alberto García Valiño"
__credits__ = ["José Alberto García Valiño"]
__license__ = "MIT"
__version__ = "1.0"
__status__ = "Beta"


import pandas as pd

def cargar_datos_archivo(ruta_archivo):
    if not ruta_archivo:
        return None, "Error: No se proporcionó una ruta de archivo."

    try:
        df_raw = pd.DataFrame()
        if ruta_archivo.lower().endswith('.csv'):
            df_raw = pd.read_csv(ruta_archivo, sep=None, engine='python', header=None, dtype=str)
            
        elif ruta_archivo.lower().endswith(('.xls', '.xlsx')):
            try:
                df_raw = pd.read_excel(ruta_archivo, header=None, dtype=str)
            except Exception as e:
                return None, f"Error leyendo Excel: {e} (¿Falta instalar openpyxl?)"
        else:
            return None, f"Error: Formato no soportado."

        if df_raw.empty:
            return None, "Error: El archivo está vacío."

        col0_str = df_raw.iloc[:, 0].astype(str).str.lower()

        es_formato_medico = col0_str.str.contains("f. muestreo", na=False).any() or \
                            col0_str.str.contains("flujo", na=False).any()
        
        dt = 0.01 #datospiraira frecuencia = 100Hz
        mensaje_extra = ""

        #CASO A formato
        if es_formato_medico:
            fila_fs = df_raw[col0_str.str.contains("f. muestreo", na=False)].index
            if not fila_fs.empty:
                try:
                    #valor suele estar en columna 1
                    val_fs = str(df_raw.iloc[fila_fs[0], 1])
                    val_fs = val_fs.replace(',', '.').replace('"', '').strip()
                    fs = float(val_fs)
                    if fs > 0:
                        dt = 1.0 / fs
                        mensaje_extra = f"(Frecuencia detectada: {fs} Hz)"
                except:
                    pass

            #encontrar inicio de Flujo
            fila_datos = df_raw[col0_str.str.contains("flujo", na=False)].index
            
            if not fila_datos.empty:
                idx_inicio = fila_datos[0]
                col_datos_idx = 1 if len(df_raw.columns) > 1 else 0
                
                serie_datos = df_raw.iloc[idx_inicio:, col_datos_idx]
            else:
                #columna 0 si no 1
                col_datos_idx = 1 if len(df_raw.columns) > 1 else 0
                serie_datos = df_raw.iloc[:, col_datos_idx]

            #quito comillas, unifico punto decimal
            serie_datos = serie_datos.astype(str).str.replace('"', '').str.replace(';', '').str.replace(',', '.')
            
            #convierto y limpio no numéricos
            flujo_clean = pd.to_numeric(serie_datos, errors='coerce').dropna()
            
            df = pd.DataFrame({'flujo': flujo_clean})

        #CASO B (Solo números, 1 o 2 columnas)
        else:
            #limpio caracteres raros
            df_temp = df_raw.replace({'"': '', ';': ','}, regex=True)
            df_temp = df_temp.replace(',', '.', regex=True)
            
            #convierto todo a número
            df_temp = df_temp.apply(pd.to_numeric, errors='coerce')
            df_temp.dropna(inplace=True)

            if df_temp.empty:
                return None, "Error: No se encontraron datos numéricos válidos."

            cols = len(df_temp.columns)
            if cols == 1:
                df = pd.DataFrame({'flujo': df_temp.iloc[:, 0]})
                mensaje_extra = "(1 columna genérica detectada)"
            elif cols >= 2:
                df = pd.DataFrame({
                    'volumen': df_temp.iloc[:, 0],
                    'flujo': df_temp.iloc[:, 1]
                })
            else:
                 return None, "Error: Estructura de columnas no reconocida."

        #3.CALCULO DE VOLUMEN 
        if 'volumen' not in df.columns:
            df['volumen'] = df['flujo'].cumsum() * dt
            if not mensaje_extra:
                mensaje_extra = "(Volumen calculado a 100 Hz)"

        df = df[['volumen', 'flujo']].reset_index(drop=True)
        
        return df, f"Carga exitosa ({len(df)} muestras). {mensaje_extra}"

    except Exception as e:
        return None, f"Error crítico procesando archivo: {e}"