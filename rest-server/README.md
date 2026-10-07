# Servidor REST — Catalog & Quote API

- Responsável: Gabriel Soares
- Tecnologia: Python 3.13, FastAPI, Uvicorn
- Contrato: [contracts/rest/catalog-quote-api.md](../contracts/rest/catalog-quote-api.md)
- Backlog: épico E02 (F02 a F08)

## Estrutura

| Arquivo | Conteúdo |
|---|---|
| `app/main.py` | Criação da aplicação e rotas |
| `app/config.py` | Variáveis de ambiente |
| `app/catalog.py` | Catálogo fixo em memória |
| `app/quotes.py` | Validação e cálculo de cotações |
| `app/errors.py` | Formato padrão de erro |
| `app/logs.py` | Registro das chamadas recebidas |
| `tests/` | Testes R1–R5 e casos de erro |

## Variáveis de ambiente

| Variável | Padrão |
|---|---|
| `SERVER_TEAM` | `S00` |
| `REST_HOST` | `0.0.0.0` |
| `REST_PORT` | `8080` |

## Execução

Todos os comandos são executados dentro de `rest-server/`.

### Instalação

Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows (CMD):

```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Iniciar o servidor

Linux:

```bash
SERVER_TEAM=S03 python -m app.main
```

Windows (CMD):

```bat
set SERVER_TEAM=S03
python -m app.main
```

A API fica disponível em `http://<ip-da-maquina>:8080/api/v1`. A página `/docs` permite testar as rotas pelo navegador.

### Testes

```bash
pytest
```

### Exemplo de chamada

```bash
curl http://localhost:8080/api/v1/products/KB-100 -H "X-Client-Team: C01" -H "X-Request-ID: req-001"
```

## Logs

Cada chamada recebida aparece no terminal e é gravada em `logs/rest/server.log`, na raiz do repositório.
