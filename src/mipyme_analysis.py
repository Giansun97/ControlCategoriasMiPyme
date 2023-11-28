from models.SalesData import SalesData
from utils import constants
import pandas as pd
from models.Contribuyente import Contribuyente
from src.extract_info_certificado_mipyme import extract_previous_periods_sales_from_pdf


def data_analisis_mipyme(contribuyente: Contribuyente, sales_data_list: list):
    """
    Analyzes the MiPyme (Micro, Small, and Medium-sized Enterprises) category of a given taxpayer based on their
    activity and projected average total sales. The function reads MiPyme category data from an Excel file,
    calculates the average total sales, assigns a MiPyme category to the taxpayer, and generates a summary of the
    analysis.

    Parameters:
    - contribuyente (Contribuyente): An instance of the Contribuyente class representing the taxpayer.
    - sales_data_list (list): A list of sales data used to calculate the projected average total sales.

    Returns:
    - result_dict (dict): A dictionary containing the analysis results, including the taxpayer's details,
      projected average total sales, MiPyme category, sales limit, and the difference between sales limit and
      projected average total sales.
    """

    # Read excel with mipyme categories
    df_mipyme_categories = pd.read_excel(constants.TABLA_CATEGORIAS_MIPYME)

    # Calculate the projected average from the total sales
    projected_average_total_sales = calculate_current_year_sales_average(sales_data_list)

    # Extract sales from DJ miPyme
    previous_period_sales, previous_previous_sales = extract_previous_periods_sales_from_pdf(
        fr'{contribuyente.ruta_archivo_pdf}',
        contribuyente.ejercicio
    )

    # Calculate average from previous periods
    previous_periods_sales_average = (previous_previous_sales + previous_previous_sales) / 2

    # Calculate average sales
    sales_average = previous_periods_sales_average + projected_average_total_sales

    # Get contribuyente activity
    activity = contribuyente.actividad

    # Assign a MiPyme category to the contribuyente in base to activity and average total sales.
    category, sales_limit = assign_contribuyente_category(
        activity,
        sales_average,
        df_mipyme_categories
    )

    # Calculate difference between sales limit and projected average total sales
    difference = sales_limit - sales_average

    percentage_consumed = ((sales_limit / difference) - 1) * 100

    # Show a resume from the analisis in the console.
    print_mipyme_analysis_summary(contribuyente, sales_average, category, sales_limit, difference, percentage_consumed)

    # Append results to a dictionary
    result_dict = append_results_to_dict(
        contribuyente,
        sales_average,
        category,
        sales_limit,
        difference,
        percentage_consumed
    )

    return result_dict


def append_results_to_dict(contribuyente, average_total_sales, category, sales_limit, difference, percentage_consumed):
    # Create a dictionary with the results
    result_dict = {
        'Nombre': contribuyente.contribuyente,
        'Actividad': contribuyente.actividad,
        'CategoriaAsignada': category,
        'PromedioVentas': average_total_sales,
        'LimiteVentas': sales_limit,
        'Diferencia': difference,
        'PorcentajeConsumido': percentage_consumed
    }

    return result_dict


def print_mipyme_analysis_summary(contribuyente, average_total_sales, category,
                                  sales_limit, difference, percentage_consumed):
    print(f"Resumen del análisis MiPyme para el contribuyente {contribuyente.contribuyente}:")
    print(f"Actividad del contribuyente: {contribuyente.actividad}")
    print(f"Categoría asignada: {category}")
    print(f"Promedio de ventas actual: {average_total_sales:,.2f}")

    if sales_limit is not None:
        print(f"Límite de ventas para la categoría: {sales_limit:,.2f}")
        print(f"Hasta pasarse de categoria restan: {difference:,.2f}")
        print(f"Porcentaje Consumido de la categoria: {percentage_consumed:,.2f}%")
    else:
        print("No se encontró categoría adecuada.")


def assign_contribuyente_category(actividad: str, average_total_sales: float, df_mipyme_categories: pd.DataFrame):
    # Filter df_mipyme_categories by activity
    df_actividad = df_mipyme_categories[df_mipyme_categories['nombre_actividad'] == actividad]

    # for each row of df_actividad compare average_total_sales vs limite_ventas
    for _, row in df_actividad.iterrows():
        sales_limit = row['limite_ventas']
        categoria = row['Categoria']
        if average_total_sales <= sales_limit:  # if average <= to sales limit
            return categoria, sales_limit  # return category and sales limit

    return "No se encontró categoría adecuada"


def calculate_current_year_sales_average(sales_data_list: list):
    # Get total sales from current year
    total_sales_year = SalesData.sum_all_sales_data(sales_data_list)

    # Get number of periods
    periods_in_sales_data_list = len(sales_data_list)

    # Calculate sales average
    average_total_sales = total_sales_year.total_neto / periods_in_sales_data_list

    projected_average_total_sales = average_total_sales * 12

    return projected_average_total_sales
