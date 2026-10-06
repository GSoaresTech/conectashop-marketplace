"""Criação da aplicação FastAPI e registro das rotas."""

import traceback

import uvicorn
from fastapi import APIRouter, Depends, FastAPI, Header, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from app.catalog import buscar_produto
from app.config import HOST, PORT, SERVER_TEAM
from app.errors import (
    ErroApi,
    RespostaJson,
    resposta_erro,
    tratar_corpo_invalido,
    tratar_erro_api,
    tratar_erro_http,
)
from app.quotes import PedidoCotacao, calcular_cotacao, validar_itens


def validar_headers(
    x_client_team: str | None = Header(default=None),
    x_request_id: str | None = Header(default=None),
):
    if not x_client_team or not x_request_id:
        raise ErroApi(
            400,
            "MISSING_REQUIRED_HEADER",
            "Headers X-Client-Team and X-Request-ID are required",
        )


app = FastAPI(title="Catalog & Quote API", version="v1", default_response_class=RespostaJson)
app.add_exception_handler(ErroApi, tratar_erro_api)
app.add_exception_handler(RequestValidationError, tratar_corpo_invalido)
app.add_exception_handler(HTTPException, tratar_erro_http)

api = APIRouter(prefix="/api/v1", dependencies=[Depends(validar_headers)])


@app.middleware("http")
async def processar_chamada(request: Request, call_next):
    try:
        resposta = await call_next(request)
    except Exception:
        traceback.print_exc()
        resposta = resposta_erro(request, 500, "INTERNAL_ERROR", "Unexpected server error")

    request_id = request.headers.get("X-Request-ID")
    if request_id:
        resposta.headers["X-Request-ID"] = request_id

    return resposta


@api.get("/products/{sku}")
def consultar_produto(sku: str):
    produto = buscar_produto(sku)
    if produto is None:
        raise ErroApi(404, "PRODUCT_NOT_FOUND", "Product not found")
    return produto


@api.post("/quotes")
def criar_cotacao(pedido: PedidoCotacao, request: Request):
    validar_itens(pedido.items)
    cotacao = calcular_cotacao(pedido.items)
    return {"requestId": request.headers["X-Request-ID"], **cotacao}


app.include_router(api)


if __name__ == "__main__":
    print(f"Servidor REST da equipe {SERVER_TEAM} em http://{HOST}:{PORT}/api/v1")
    uvicorn.run(app, host=HOST, port=PORT, access_log=False)
