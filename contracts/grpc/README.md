# Contrato gRPC — ShippingService

O arquivo [shipping.proto](shipping.proto) é a cópia exata do contrato. Não renomear package, service, métodos, campos, enums nem números de campo.

- Porta sugerida: `50051`

## Metadata obrigatória

| Chave | Descrição |
|---|---|
| `x-client-team` | Código da equipe Cliente (ex.: C01) |

## Regras de CalculateShipping

- `request_id` é obrigatório e não pode ser vazio.
- `weight_grams` deve estar entre 1 e 30000.
- `zone` não pode ser `SHIPPING_ZONE_UNSPECIFIED`.
- `mode` não pode ser `SHIPPING_MODE_UNSPECIFIED`.
- A resposta repete `request_id` exatamente como recebido.
- `server_team` contém o código do grupo Servidor (ex.: S02).

### Tarifa base (centavos)

| Zona | STANDARD | EXPRESS |
|---|---|---|
| LOCAL | 1000 | 1600 |
| REGIONAL | 1800 | 2800 |
| NATIONAL | 3000 | 4500 |

### Adicional por quilograma iniciado

| Modo | Adicional |
|---|---|
| STANDARD | 400 centavos |
| EXPRESS | 600 centavos |

```
quilogramas_cobrados = teto(weight_grams / 1000)
price_cents = tarifa_base + quilogramas_cobrados × adicional
```

### Prazo estimado (dias)

| Zona | STANDARD | EXPRESS |
|---|---|---|
| LOCAL | 2 | 1 |
| REGIONAL | 4 | 2 |
| NATIONAL | 7 | 3 |

## Health

```
HealthResponse { status: "SERVING", server_team: "S02" }
```

## Erros

| Situação | Status | Descrição |
|---|---|---|
| `x-client-team` ausente | `INVALID_ARGUMENT` | `MISSING_CLIENT_TEAM` |
| `request_id` vazio | `INVALID_ARGUMENT` | `MISSING_REQUEST_ID` |
| `weight_grams` fora do intervalo | `INVALID_ARGUMENT` | `INVALID_WEIGHT` |
| `zone` UNSPECIFIED | `INVALID_ARGUMENT` | `INVALID_ZONE` |
| `mode` UNSPECIFIED | `INVALID_ARGUMENT` | `INVALID_MODE` |
| Erro inesperado | `INTERNAL` | `INTERNAL_ERROR` |

## Testes obrigatórios

| Teste | Entrada | Resultado esperado |
|---|---|---|
| G1 | `Health()` | `status=SERVING`; `server_team` identifica o servidor |
| G2 | 1500 g, LOCAL, STANDARD | `price_cents=1800`; `estimated_days=2` |
| G3 | 2500 g, REGIONAL, EXPRESS | `price_cents=4600`; `estimated_days=2` |
| G4 | 1000 g, NATIONAL, STANDARD | `price_cents=3400`; `estimated_days=7` |
| G5 | `weight_grams=0` | `INVALID_ARGUMENT`; `INVALID_WEIGHT` |
