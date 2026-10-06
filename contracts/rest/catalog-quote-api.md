# Contrato REST — Catalog & Quote API

Não adicionar campos, paths, headers ou regras além dos definidos aqui.

| Propriedade | Valor |
|---|---|
| Versão | v1 |
| Base path | `/api/v1` |
| Formato | `application/json; charset=utf-8` |
| Porta sugerida | `8080` |

## Headers

| Header | Obrigatório | Descrição |
|---|---|---|
| `X-Client-Team` | Sim | Código da equipe Cliente (ex.: C03) |
| `X-Request-ID` | Sim | Identificador único da chamada. Aparece nos logs e é devolvido no header da resposta |
| `Content-Type` | Quando houver body | `application/json` |

Se `X-Client-Team` ou `X-Request-ID` estiver ausente: HTTP 400, code `MISSING_REQUIRED_HEADER`.

## Catálogo fixo

| SKU | Nome | unitPriceCents | available |
|---|---|---|---|
| KB-100 | Teclado Mecânico | 25990 | true |
| MS-200 | Mouse Sem Fio | 12990 | true |
| HD-300 | Headset USB | 19990 | true |
| MN-400 | Monitor 27 | 119990 | true |

Valores monetários sempre em centavos inteiros (25990 = R$ 259,90).

## GET /api/v1/products/{sku}

Sucesso — HTTP 200:

```json
{
  "sku": "KB-100",
  "name": "Teclado Mecânico",
  "unitPriceCents": 25990,
  "available": true
}
```

Produto inexistente — HTTP 404:

```json
{
  "code": "PRODUCT_NOT_FOUND",
  "message": "Product not found",
  "requestId": "req-002"
}
```

## POST /api/v1/quotes

Body:

```json
{
  "items": [
    { "sku": "KB-100", "quantity": 2 },
    { "sku": "MS-200", "quantity": 1 }
  ]
}
```

### Validações

- `items` deve conter de 1 a 5 itens distintos.
- `quantity` deve ser inteiro entre 1 e 10.
- Todo SKU deve existir no catálogo.
- SKUs duplicados no mesmo request são inválidos.

### Cálculo

1. `subtotalCents` = soma de `unitPriceCents × quantity`.
2. Desconto: subtotal < 50000 → 0%; 50000 a 99999 → 5%; subtotal >= 100000 → 10%.
3. `discountCents` = parte inteira de `subtotalCents × discountPercent / 100`.
4. `totalCents` = `subtotalCents - discountCents`.

Sucesso — HTTP 200:

```json
{
  "requestId": "req-003",
  "subtotalCents": 64970,
  "discountPercent": 5,
  "discountCents": 3248,
  "totalCents": 61722
}
```

## Erros

| Situação | HTTP | code |
|---|---|---|
| Header obrigatório ausente | 400 | `MISSING_REQUIRED_HEADER` |
| JSON inválido ou campo obrigatório ausente | 400 | `INVALID_REQUEST` |
| Produto consultado não existe | 404 | `PRODUCT_NOT_FOUND` |
| SKU inválido na cotação | 422 | `INVALID_PRODUCT` |
| Quantidade fora do intervalo ou SKU duplicado | 422 | `INVALID_QUANTITY_OR_ITEMS` |
| Erro inesperado | 500 | `INTERNAL_ERROR` |

Formato padrão:

```json
{
  "code": "INVALID_PRODUCT",
  "message": "Human readable description",
  "requestId": "req-004"
}
```

## Testes obrigatórios

| Teste | Operação | Resultado esperado |
|---|---|---|
| R1 | GET KB-100 | HTTP 200; `unitPriceCents=25990` |
| R2 | GET XX-999 | HTTP 404; `PRODUCT_NOT_FOUND` |
| R3 | POST quote: 2×KB-100 + 1×MS-200 | HTTP 200; subtotal 64970; desconto 5; total 61722 |
| R4 | POST quote: 1×MN-400 | HTTP 200; subtotal 119990; desconto 10; discount 11999; total 107991 |
| R5 | POST quote com SKU inexistente | HTTP 422; `INVALID_PRODUCT` |
