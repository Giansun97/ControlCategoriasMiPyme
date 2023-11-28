from src.process_input_file import get_contribuyentes_to_process
from src.process_sales_from_csv import get_sales_data_from_directory
from src.mipyme_analysis import data_analisis_mipyme
from src.export_results_to_excel import export_results_to_excel


def main():
    contribuyentes = get_contribuyentes_to_process()
    results_list = []

    for contribuyente in contribuyentes:
        print(f"procesando {contribuyente.contribuyente}")

        # Get list of sales from directory
        sales_data_list = get_sales_data_from_directory(fr'{contribuyente.ruta_archivos}')

        # Analyze MiPyme situation
        data_analisis_mipyme_result_dict = data_analisis_mipyme(contribuyente, sales_data_list)

        # Append contribuyente results to results list
        results_list.append(data_analisis_mipyme_result_dict)

    export_results_to_excel(results_list)


if __name__ == '__main__':
    main()
