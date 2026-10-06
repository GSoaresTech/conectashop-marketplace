# Matriz de integração

| Protocolo | Cliente parceiro | Testes recebidos | Resultado inicial | Resultado final | Request IDs | Observação |
|---|---|---|---|---|---|---|
| REST | | R1–R5 | | | | |
| REST | | R1–R5 | | | | |
| gRPC | | G1–G5 | | | | |
| gRPC | | G1–G5 | | | | |

## Resultado por teste

| Teste | Esperado | Cliente 1 | Cliente 2 |
|---|---|---|---|
| R1 | HTTP 200; `unitPriceCents=25990` | | |
| R2 | HTTP 404; `PRODUCT_NOT_FOUND` | | |
| R3 | HTTP 200; subtotal 64970; desconto 5; total 61722 | | |
| R4 | HTTP 200; subtotal 119990; desconto 10; discount 11999; total 107991 | | |
| R5 | HTTP 422; `INVALID_PRODUCT` | | |
| G1 | `SERVING`; `server_team` correto | | |
| G2 | `price_cents=1800`; `estimated_days=2` | | |
| G3 | `price_cents=4600`; `estimated_days=2` | | |
| G4 | `price_cents=3400`; `estimated_days=7` | | |
| G5 | `INVALID_ARGUMENT`; `INVALID_WEIGHT` | | |
