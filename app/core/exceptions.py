"""
Custom Exceptions.

Todas las excepciones de negocio del proyecto deben heredar de
SalesAnalyticsException.

Ejemplo:

raise CsvFormatException(
    message="La columna FACTURA no existe."
)
"""

from http import HTTPStatus
from typing import Optional


class SalesAnalyticsException(Exception):
    """
    Excepción base del proyecto.

    Todas las excepciones personalizadas deben heredar de esta clase.
    """

    status_code: HTTPStatus = HTTPStatus.BAD_REQUEST
    error_code: str = "APPLICATION_ERROR"
    default_message: str = "Ocurrió un error en la aplicación."

    def __init__(self, message: Optional[str] = None):
        self.message = message or self.default_message
        super().__init__(self.message)


# ==========================================================
# Upload
# ==========================================================

class InvalidFileException(SalesAnalyticsException):
    status_code = HTTPStatus.BAD_REQUEST
    error_code = "INVALID_FILE"
    default_message = "El archivo recibido no es válido."


class FileTooLargeException(SalesAnalyticsException):
    status_code = HTTPStatus.REQUEST_ENTITY_TOO_LARGE
    error_code = "FILE_TOO_LARGE"
    default_message = "El archivo excede el tamaño máximo permitido."


class FileAlreadyImportedException(SalesAnalyticsException):
    status_code = HTTPStatus.CONFLICT
    error_code = "FILE_ALREADY_IMPORTED"
    default_message = "El archivo ya fue importado anteriormente."


# ==========================================================
# CSV
# ==========================================================

class CsvFormatException(SalesAnalyticsException):
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY
    error_code = "CSV_INVALID_FORMAT"
    default_message = "El formato del archivo CSV no es válido."


class CsvValidationException(SalesAnalyticsException):
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY
    error_code = "CSV_VALIDATION_ERROR"
    default_message = "Los datos del CSV contienen errores."


# ==========================================================
# Database
# ==========================================================

class DatabaseInsertException(SalesAnalyticsException):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    error_code = "DATABASE_INSERT_ERROR"
    default_message = "No fue posible guardar la información."


class RecordNotFoundException(SalesAnalyticsException):
    status_code = HTTPStatus.NOT_FOUND
    error_code = "RECORD_NOT_FOUND"
    default_message = "No se encontró el registro solicitado."


# ==========================================================
# Reports
# ==========================================================

class ReportGenerationException(SalesAnalyticsException):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    error_code = "REPORT_GENERATION_ERROR"
    default_message = "No fue posible generar el reporte."


class ExcelGenerationException(SalesAnalyticsException):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    error_code = "EXCEL_GENERATION_ERROR"
    default_message = "No fue posible generar el archivo Excel."