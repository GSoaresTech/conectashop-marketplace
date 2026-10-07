# Matriz de integração

Equipe Servidor S13, integração de 06/10/2026. O guia prevê dois Clientes REST e dois Clientes gRPC por Servidor, mas o sorteio atribuiu à equipe um único Cliente, o C5, para os dois protocolos.

| Protocolo | Cliente parceiro | Testes recebidos | Resultado inicial | Resultado final | Request IDs | Observação |
|---|---|---|---|---|---|---|
| REST | C5 | R1 e R5, além de casos de erro | A aplicação do C5 não executou os testes | R1 e R5 OK; R2, R3 e R4 não executados | `req-001`, `MN-400` | Chamadas feitas pela página `/docs` do servidor, com `X-Client-Team=S13` |
| gRPC | C5 | Nenhum | Nenhuma chamada recebida | G1 a G5 não executados | - | Servidor ativo durante a janela |

## Resultado por teste

| Teste | Esperado | Cliente C5 | Evidência no log |
|---|---|---|---|
| R1 | HTTP 200; `unitPriceCents=25990` | OK | 20:32:35, `req-001` |
| R2 | HTTP 404; `PRODUCT_NOT_FOUND` | Não executado | - |
| R3 | HTTP 200; subtotal 64970; desconto 5; total 61722 | Não executado | - |
| R4 | HTTP 200; subtotal 119990; desconto 10; discount 11999; total 107991 | Não executado | - |
| R5 | HTTP 422; `INVALID_PRODUCT` | OK, com o corpo de exemplo do Swagger (SKU `string`) | 20:39:32, `req-001` |
| G1 | `SERVING`; `server_team` correto | Não executado | - |
| G2 | `price_cents=1800`; `estimated_days=2` | Não executado | - |
| G3 | `price_cents=4600`; `estimated_days=2` | Não executado | - |
| G4 | `price_cents=3400`; `estimated_days=7` | Não executado | - |
| G5 | `INVALID_ARGUMENT`; `INVALID_WEIGHT` | Não executado | - |

## Outras chamadas do C5

| Horário | Chamada | Resposta | Observação |
|---|---|---|---|
| 20:31:51 | `GET /api/v1/products/{sku}` sem `X-Request-ID` | 400 `MISSING_REQUIRED_HEADER` | Conforme o contrato |
| 20:38:33 | `GET /api/v1/products/KB-100` com `X-Request-ID=MN-400` | 200 | SKU digitado no campo do Request ID |
| 20:40:28 | `POST /api/v1/quotes` com KB-100 × 0 | 422 `INVALID_QUANTITY_OR_ITEMS` | Conforme o contrato |
| 20:40:42 | `POST /api/v1/quotes` com KB-100 × 1000000000000 | 422 `INVALID_QUANTITY_OR_ITEMS` | Conforme o contrato |
| 20:40:52 | `POST /api/v1/quotes` com KB-100 × 1 | 200 | Cotação válida, subtotal 25990 sem desconto |

Todas as respostas do servidor seguiram o contrato. Os logs completos estão em [logs/rest/server.log](../../logs/rest/server.log) e [logs/grpc/server.log](../../logs/grpc/server.log).
