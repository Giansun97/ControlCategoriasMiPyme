from dataclasses import dataclass


@dataclass
class SalesData:
    periodo: str
    total_comprobante: float
    total_neto: float
    total_iva: float

    @classmethod
    def sum_all_sales_data(cls, sales_data_list: list['SalesData']) -> 'SalesData':
        # Initialize totals
        total_comprobante = 0
        total_neto = 0
        total_iva = 0

        # Sum up totals
        for data in sales_data_list:
            total_comprobante += data.total_comprobante
            total_neto += data.total_neto
            total_iva += data.total_iva

        # Choose any period from the list since they should be the same
        period = sales_data_list[0].periodo if sales_data_list else "Unknown Period"

        return cls(
            total_comprobante=total_comprobante,
            total_neto=total_neto,
            total_iva=total_iva,
            periodo=period
        )

    def print_summary(self):
        """Prints a summary of the sales data."""

        print(f'Total: {self.periodo}')
        print(f'Total: {self.total_comprobante}')
        print(f'No Gravado: {self.total_neto}')
        print(f'Neto 105: {self.total_iva}')

    def print_unified_summary(self):
        """Prints a summary of the sales data."""

        print(f'Total: {self.total_comprobante}')
        print(f'No Gravado: {self.total_neto}')
        print(f'Neto 105: {self.total_iva}')
