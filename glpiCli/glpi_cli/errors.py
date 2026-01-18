# -*- coding: utf-8 -*-
"""Error handling and translation for GLPI API errors."""
from typing import Optional


class GLPIError(Exception):
    """Base exception for GLPI CLI errors."""

    def __init__(self, message: str, glpi_error: Optional[str] = None, status_code: Optional[int] = None):
        """Initialize GLPI error.

        Args:
            message: Translated error message in PT-BR
            glpi_error: Original GLPI error code
            status_code: HTTP status code
        """
        self.message = message
        self.glpi_error = glpi_error
        self.status_code = status_code
        super().__init__(self.message)

    def __str__(self):
        """Format error message."""
        parts = []
        if self.glpi_error:
            parts.append(f"Erro GLPI: {self.glpi_error}")
            if self.status_code:
                parts.append(f"({self.status_code})")
        if self.message:
            parts.append(f"\nTradu\u00e7\u00e3o: {self.message}")
        return " ".join(parts) if parts else "Erro desconhecido"


# Error code to PT-BR message mapping
ERROR_MESSAGES = {
    # Authentication errors
    "ERROR_GLPI_LOGIN_USER_TOKEN": "Token de usu\u00e1rio inv\u00e1lido ou n\u00e3o autorizado",
    "ERROR_GLPI_LOGIN": "Falha na autentica\u00e7\u00e3o. Verifique suas credenciais",
    "ERROR_LOGIN_PARAMETERS_MISSING": "Par\u00e2metros de login ausentes",
    "ERROR_GLPI_APP_TOKEN_INVALID": "App-Token inv\u00e1lido",
    "ERROR_SESSION_TOKEN_INVALID": "Token de sess\u00e3o inv\u00e1lido ou expirado",
    "ERROR_SESSION_TOKEN_MISSING": "Token de sess\u00e3o n\u00e3o fornecido",

    # Item errors
    "ERROR_ITEM_NOT_FOUND": "Item n\u00e3o encontrado no sistema",
    "ERROR_ITEMTYPE_NOT_FOUND": "Tipo de item inv\u00e1lido ou n\u00e3o encontrado",
    "ERROR_RIGHT_MISSING": "Sem permiss\u00e3o para acessar este recurso",
    "ERROR_NOT_ALLOWED": "Opera\u00e7\u00e3o n\u00e3o permitida",

    # Request errors
    "ERROR_BAD_ARRAY": "Formato de array inv\u00e1lido na requisi\u00e7\u00e3o",
    "ERROR_RANGE_EXCEED_TOTAL": "Range solicitado excede o total de itens",
    "ERROR_GLPI_PARTIAL_ADD": "Item adicionado parcialmente (alguns campos falharam)",
    "ERROR_GLPI_ADD": "Falha ao adicionar item",
    "ERROR_GLPI_UPDATE": "Falha ao atualizar item",
    "ERROR_GLPI_DELETE": "Falha ao deletar item",

    # Generic errors
    "ERROR": "Erro gen\u00e9rico no servidor GLPI",
    "ERROR_RESOURCE_NOT_FOUND": "Recurso n\u00e3o encontrado",
    "ERROR_METHOD_NOT_ALLOWED": "M\u00e9todo HTTP n\u00e3o permitido",
    "ERROR_INVALID_PARAMETER": "Par\u00e2metro inv\u00e1lido",
}


def translate_error(error_code: str, status_code: Optional[int] = None) -> str:
    """Translate GLPI error code to PT-BR message.

    Args:
        error_code: GLPI error code
        status_code: HTTP status code

    Returns:
        Translated error message in PT-BR
    """
    # Try exact match first
    if error_code in ERROR_MESSAGES:
        return ERROR_MESSAGES[error_code]

    # Fallback based on HTTP status code
    if status_code:
        if status_code == 400:
            return "Requisi\u00e7\u00e3o inv\u00e1lida"
        elif status_code == 401:
            return "N\u00e3o autenticado. Verifique seus tokens"
        elif status_code == 403:
            return "Sem permiss\u00e3o para acessar este recurso"
        elif status_code == 404:
            return "Recurso n\u00e3o encontrado"
        elif status_code == 405:
            return "M\u00e9todo HTTP n\u00e3o permitido"
        elif status_code == 500:
            return "Erro interno do servidor GLPI"
        elif status_code >= 500:
            return "Erro no servidor GLPI"

    return f"Erro desconhecido: {error_code}"


def raise_glpi_error(error_data: dict, status_code: Optional[int] = None):
    """Parse GLPI API error response and raise appropriate exception.

    Args:
        error_data: Error response from GLPI API
        status_code: HTTP status code

    Raises:
        GLPIError: With translated message
    """
    # GLPI API returns errors as: [error_code, error_message] or {"error": "message"}
    if isinstance(error_data, list) and len(error_data) >= 1:
        error_code = error_data[0]
        translated = translate_error(error_code, status_code)
        raise GLPIError(translated, error_code, status_code)

    elif isinstance(error_data, dict):
        error_code = error_data.get("error", "ERROR")
        translated = translate_error(error_code, status_code)
        raise GLPIError(translated, error_code, status_code)

    else:
        raise GLPIError("Erro desconhecido", status_code=status_code)
