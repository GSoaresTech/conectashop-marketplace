import pytest
from fastapi.testclient import TestClient

from app import logs, main
from app.quotes import percentual_desconto

HEADERS = {"X-Client-Team": "C01", "X-Request-ID": "req-001"}


@pytest.fixture
def cliente(tmp_path, monkeypatch):
    monkeypatch.setattr(logs, "ARQUIVO_LOG", tmp_path / "server.log")
    return TestClient(main.app)


def cotar(cliente, itens):
    return cliente.post("/api/v1/quotes", json={"items": itens}, headers=HEADERS)


def test_r1_consulta_produto_existente(cliente):
    resposta = cliente.get("/api/v1/products/KB-100", headers=HEADERS)

    assert resposta.status_code == 200
    assert resposta.json() == {
        "sku": "KB-100",
        "name": "Teclado Mecânico",
        "unitPriceCents": 25990,
        "available": True,
    }


def test_r2_produto_inexistente(cliente):
    resposta = cliente.get("/api/v1/products/XX-999", headers=HEADERS)

    assert resposta.status_code == 404
    assert resposta.json() == {
        "code": "PRODUCT_NOT_FOUND",
        "message": "Product not found",
        "requestId": "req-001",
    }


def test_r3_cotacao_com_desconto_de_5(cliente):
    resposta = cotar(cliente, [{"sku": "KB-100", "quantity": 2}, {"sku": "MS-200", "quantity": 1}])

    assert resposta.status_code == 200
    assert resposta.json() == {
        "requestId": "req-001",
        "subtotalCents": 64970,
        "discountPercent": 5,
        "discountCents": 3248,
        "totalCents": 61722,
    }


def test_r4_cotacao_com_desconto_de_10(cliente):
    resposta = cotar(cliente, [{"sku": "MN-400", "quantity": 1}])

    assert resposta.status_code == 200
    assert resposta.json() == {
        "requestId": "req-001",
        "subtotalCents": 119990,
        "discountPercent": 10,
        "discountCents": 11999,
        "totalCents": 107991,
    }


def test_r5_cotacao_com_sku_inexistente(cliente):
    resposta = cotar(cliente, [{"sku": "XX-999", "quantity": 1}])

    assert resposta.status_code == 422
    assert resposta.json()["code"] == "INVALID_PRODUCT"
    assert resposta.json()["requestId"] == "req-001"


def test_cotacao_sem_desconto(cliente):
    resposta = cotar(cliente, [{"sku": "MS-200", "quantity": 1}])

    assert resposta.json()["discountPercent"] == 0
    assert resposta.json()["totalCents"] == 12990


@pytest.mark.parametrize("subtotal, esperado", [(49999, 0), (50000, 5), (99999, 5), (100000, 10)])
def test_faixas_de_desconto(subtotal, esperado):
    assert percentual_desconto(subtotal) == esperado


@pytest.mark.parametrize("header_removido", ["X-Client-Team", "X-Request-ID"])
def test_header_obrigatorio_ausente(cliente, header_removido):
    headers = {nome: valor for nome, valor in HEADERS.items() if nome != header_removido}
    resposta = cliente.get("/api/v1/products/KB-100", headers=headers)

    assert resposta.status_code == 400
    assert resposta.json()["code"] == "MISSING_REQUIRED_HEADER"


def test_header_ausente_tem_prioridade_sobre_corpo_invalido(cliente):
    resposta = cliente.post("/api/v1/quotes", json={"items": "x"}, headers={"X-Request-ID": "req-001"})

    assert resposta.status_code == 400
    assert resposta.json()["code"] == "MISSING_REQUIRED_HEADER"


def test_resposta_devolve_request_id_e_content_type(cliente):
    resposta = cliente.get("/api/v1/products/KB-100", headers=HEADERS)

    assert resposta.headers["X-Request-ID"] == "req-001"
    assert resposta.headers["Content-Type"] == "application/json; charset=utf-8"


@pytest.mark.parametrize("quantidade", [0, 11])
def test_quantidade_fora_do_intervalo(cliente, quantidade):
    resposta = cotar(cliente, [{"sku": "KB-100", "quantity": quantidade}])

    assert resposta.status_code == 422
    assert resposta.json()["code"] == "INVALID_QUANTITY_OR_ITEMS"


@pytest.mark.parametrize("itens", [[], [{"sku": "KB-100", "quantity": 1}] * 6])
def test_numero_de_itens_fora_do_intervalo(cliente, itens):
    resposta = cotar(cliente, itens)

    assert resposta.status_code == 422
    assert resposta.json()["code"] == "INVALID_QUANTITY_OR_ITEMS"


def test_sku_duplicado(cliente):
    resposta = cotar(cliente, [{"sku": "KB-100", "quantity": 1}, {"sku": "KB-100", "quantity": 2}])

    assert resposta.status_code == 422
    assert resposta.json()["code"] == "INVALID_QUANTITY_OR_ITEMS"


def test_json_invalido(cliente):
    headers = {**HEADERS, "Content-Type": "application/json"}
    resposta = cliente.post("/api/v1/quotes", content='{"items": [', headers=headers)

    assert resposta.status_code == 400
    assert resposta.json()["code"] == "INVALID_REQUEST"


@pytest.mark.parametrize(
    "corpo",
    [
        {},
        {"items": [{"sku": "KB-100"}]},
        {"items": [{"quantity": 1}]},
        {"items": [{"sku": "KB-100", "quantity": "2"}]},
    ],
)
def test_corpo_com_campo_ausente_ou_invalido(cliente, corpo):
    resposta = cliente.post("/api/v1/quotes", json=corpo, headers=HEADERS)

    assert resposta.status_code == 400
    assert resposta.json()["code"] == "INVALID_REQUEST"


def test_rota_inexistente_segue_formato_padrao(cliente):
    resposta = cliente.get("/api/v1/produtos/KB-100", headers=HEADERS)

    assert resposta.status_code == 404
    assert set(resposta.json()) == {"code", "message", "requestId"}


def test_erro_inesperado(cliente, monkeypatch):
    def falhar(sku):
        raise RuntimeError("falha simulada")

    monkeypatch.setattr(main, "buscar_produto", falhar)
    resposta = cliente.get("/api/v1/products/KB-100", headers=HEADERS)

    assert resposta.status_code == 500
    assert resposta.json()["code"] == "INTERNAL_ERROR"
    assert resposta.headers["X-Request-ID"] == "req-001"


def test_chamadas_sao_registradas_no_log(cliente):
    cliente.get("/api/v1/products/KB-100", headers=HEADERS)
    cliente.get("/api/v1/products/XX-999", headers={"X-Client-Team": "C02", "X-Request-ID": "req-002"})
    cotar(cliente, [{"sku": "KB-100", "quantity": 2}, {"sku": "MS-200", "quantity": 1}])

    linhas = logs.ARQUIVO_LOG.read_text(encoding="utf-8").splitlines()

    assert len(linhas) == 3
    assert "client=C01 requestId=req-001 operation=GET_PRODUCT input=KB-100 status=200 result=OK" in linhas[0]
    assert "client=C02 requestId=req-002 operation=GET_PRODUCT input=XX-999 status=404 result=PRODUCT_NOT_FOUND" in linhas[1]
    assert "operation=CREATE_QUOTE input=KB-100x2,MS-200x1 status=200 result=OK" in linhas[2]
