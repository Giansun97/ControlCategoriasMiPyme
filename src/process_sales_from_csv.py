import pandas as pd
import os
from models.SalesData import SalesData


def get_sales_data_from_csv(csv_file: str, folder: str) -> 'SalesData':
    df = pd.read_csv(csv_file, delimiter=';')

    # Replace , with .
    df['Importe Total'] = df['Importe Total'].str.replace(',', '.').astype(float)
    df['Total Neto Gravado'] = df['Total Neto Gravado'].str.replace(',', '.').astype(float)
    df['Total IVA'] = df['Total IVA'].str.replace(',', '.').astype(float)

    return SalesData(
        total_comprobante=df['Importe Total'].sum(),
        total_neto=df['Total Neto Gravado'].sum(),
        total_iva=df['Total IVA'].sum(),
        periodo=folder
    )


def get_sales_data_from_directory(directory: str) -> list['SalesData']:
    sales_data_list = []

    for folder in os.listdir(directory):
        folder_path = os.path.join(directory, folder)
        if os.path.isdir(folder_path):
            for file in os.listdir(folder_path):

                if 'ventas'.lower() in file and file.endswith('.csv'):
                    file_path = os.path.join(folder_path, file)
                    sales_data = get_sales_data_from_csv(
                        file_path,
                        folder
                    )

                    if sales_data:
                        sales_data_list.append(sales_data)

    return sales_data_list
