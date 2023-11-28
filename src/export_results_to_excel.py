import pandas as pd


def export_results_to_excel(results_list: list):
    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(results_list)
    df = df.sort_values(by='PorcentajeConsumido', ascending=False)
    # Export the DataFrame to Excel
    excel_filename = 'output.xlsx'
    df.to_excel(excel_filename, index=False, sheet_name='MiPyme Analisis')
