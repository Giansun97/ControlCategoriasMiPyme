from dataclasses import dataclass
import pandas as pd
from utils import constants


@dataclass
class Contribuyente:
    cuit: str
    contribuyente: str
    ruta_archivos: str
    ruta_archivo_pdf: str
    ejercicio: int
    actividad: str
    filtro: str


