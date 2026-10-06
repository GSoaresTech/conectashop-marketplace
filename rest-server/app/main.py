"""Criação da aplicação FastAPI e registro das rotas."""

import uvicorn
from fastapi import APIRouter, FastAPI

from app.config import HOST, PORT, SERVER_TEAM
from app.errors import RespostaJson

app = FastAPI(title="Catalog & Quote API", version="v1", default_response_class=RespostaJson)

api = APIRouter(prefix="/api/v1")


app.include_router(api)


if __name__ == "__main__":
    print(f"Servidor REST da equipe {SERVER_TEAM} em http://{HOST}:{PORT}/api/v1")
    uvicorn.run(app, host=HOST, port=PORT, access_log=False)
