"""Registro das chamadas recebidas."""

from datetime import datetime
from pathlib import Path

from app.config import SERVER_TEAM

PASTA_LOGS = Path(__file__).resolve().parents[2] / "logs" / "rest"
ARQUIVO_LOG = PASTA_LOGS / "server.log"


def nome_operacao(request):
    caminho = request.url.path

    if request.method == "GET" and caminho.startswith("/api/v1/products/"):
        return "GET_PRODUCT"
    if request.method == "POST" and caminho == "/api/v1/quotes":
        return "CREATE_QUOTE"
    return f"{request.method}:{caminho}"


def registrar(request, status):
    horario = datetime.now().isoformat(timespec="seconds")
    cliente = request.headers.get("X-Client-Team") or "-"
    request_id = request.headers.get("X-Request-ID") or "-"
    entrada = getattr(request.state, "entrada", "-")
    resultado = getattr(request.state, "resultado", "OK")

    linha = (
        f"[{horario}] protocol=REST server={SERVER_TEAM} client={cliente} "
        f"requestId={request_id} operation={nome_operacao(request)} input={entrada} "
        f"status={status} result={resultado}"
    )

    print(linha, flush=True)
    PASTA_LOGS.mkdir(parents=True, exist_ok=True)
    with open(ARQUIVO_LOG, "a", encoding="utf-8") as arquivo:
        arquivo.write(linha + "\n")
