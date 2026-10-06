# Servidor REST — Catalog & Quote API

- Responsável: Gabriel
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

A definir na feature F16.
