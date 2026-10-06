"""Formato padrão de erro e tratamento de exceções."""

from fastapi.responses import JSONResponse


class RespostaJson(JSONResponse):
    media_type = "application/json; charset=utf-8"
