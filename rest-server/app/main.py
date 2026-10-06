"""Criação da aplicação FastAPI e registro das rotas."""

import uvicorn
from fastapi import APIRouter, Depends, FastAPI, Header, Request

from app.catalog import buscar_produto
from app.config import HOST, PORT, SERVER_TEAM
from app.errors import ErroApi, RespostaJson, tratar_erro_api


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

api = APIRouter(prefix="/api/v1", dependencies=[Depends(validar_headers)])


@app.middleware("http")
async def processar_chamada(request: Request, call_next):
    resposta = await call_next(request)

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


app.include_router(api)


if __name__ == "__main__":
    print(f"Servidor REST da equipe {SERVER_TEAM} em http://{HOST}:{PORT}/api/v1")
    uvicorn.run(app, host=HOST, port=PORT, access_log=False)
