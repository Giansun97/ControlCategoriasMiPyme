import pandas as pd
from utils import constants
from models.Contribuyente import Contribuyente


def get_contribuyentes_to_process():
    input_data_df = pd.read_excel(constants.INPUT_DATA_PATH)

    # Loop through each DataFrame row and create an Instance from Contribuyente
    contribuyentes = []
    for index, row in input_data_df.iterrows():
        contribuyente = Contribuyente(
            cuit=row['cuit'],
            contribuyente=row['contribuyente'],
            ruta_archivos=row['ruta archivos'],
            ruta_archivo_pdf=row['ruta archivo pdf'],
            ejercicio=row['ejercicio'],
            actividad=row['actividad'],
            filtro=row['filtro']
        )

        # Agrega la instancia solo si el filtro es igual al valor deseado
        if contribuyente.filtro == 'x':
            contribuyentes.append(contribuyente)

    return contribuyentes
