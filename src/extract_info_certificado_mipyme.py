import pdfplumber


def extract_previous_periods_sales_from_pdf(ruta_completa_archivo: str, period: int):
    previous_period_sales = None
    previous_previous_period_sales = None

    txt_list = extract_text_from_pdf(ruta_completa_archivo)
    previous_period, previous_previous_period = get_previous_periods(period)

    for txt in txt_list:
        lines = txt.split('\n')
        for line in lines:
            if f"Período Fiscal {previous_period}" in line:
                values = line.split()  # Use a space as a delimiter
                if len(values) > 1:
                    # Convert the last value to a float
                    previous_period_sales = float(values[-1].strip())

            if f"Período Fiscal {previous_previous_period}" in line:
                values = line.split()  # Use a space as a delimiter
                if len(values) > 1:
                    # Convert the last value to a float
                    previous_previous_period_sales = float(values[-1].strip())

        return previous_period_sales, previous_previous_period_sales


def get_previous_periods(period):
    rounded_period = round(period)
    previous_period = rounded_period - 1
    previous_previous_period = rounded_period - 2

    return previous_period, previous_previous_period


def extract_text_from_pdf(file_path):
    """
    This function opens the PDF and stores all the text from each page in a list.
    ----------------------
    Args:
        file_path: A string representing the path where the PDF file is located.
    Returns:
        A list containing the text from each page.
    """
    texts = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            texts.append(page.extract_text())

    return texts


# test ruta_archivo = r'\\192.168.0.3\wns\Asesoramiento Contable\WNS\TXM S.A\LEY
# PYME\DJF1272V700-153914327-1680266319462.pdf'
# ejercicio = 2023 previous_period, previous_previous_period =
# extract_previous_periods_sales_from_pdf(ruta_archivo, ejercicio) print(previous_period) print(
# previous_previous_period)
