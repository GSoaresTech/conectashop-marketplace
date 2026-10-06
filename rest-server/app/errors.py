"""Formato padrão de erro e tratamento de exceções."""

from fastapi.responses import JSONResponse


class RespostaJson(JSONResponse):
    media_type = "application/json; charset=utf-8"


class ErroApi(Exception):
    def __init__(self, status, codigo, mensagem):
        super().__init__(mensagem)
        self.status = status
        self.codigo = codigo
        self.mensagem = mensagem


def resposta_erro(request, status, codigo, mensagem):
    # O middleware lê esse valor para preencher o campo result do log
    request.state.resultado = codigo

    corpo = {
        "code": codigo,
        "message": mensagem,
        "requestId": request.headers.get("X-Request-ID"),
    }
    return RespostaJson(corpo, status_code=status)


async def tratar_erro_api(request, erro):
    return resposta_erro(request, erro.status, erro.codigo, erro.mensagem)


async def tratar_corpo_invalido(request, erro):
    return resposta_erro(request, 400, "INVALID_REQUEST", "Invalid JSON or missing required field")


async def tratar_erro_http(request, erro):
    return resposta_erro(request, erro.status_code, "INVALID_REQUEST", erro.detail)
