# Logs

Logs das chamadas recebidas pelos servidores. Fazem parte da entrega final.

| Pasta | Origem |
|---|---|
| `rest/` | Servidor REST |
| `grpc/` | Servidor gRPC |

## Formato mínimo

Cada linha deve conter horário, protocolo, equipe Servidor, equipe Cliente, Request ID, operação, entrada, status e resultado.

```
[2026-09-08T20:00:00] protocol=REST server=S03 client=C01 requestId=req-101 operation=GET_PRODUCT input=KB-100 status=200 result=OK
[2026-09-08T20:02:10] protocol=GRPC server=S03 client=C01 requestId=req-204 operation=CalculateShipping weight=1500 zone=LOCAL mode=STANDARD status=OK priceCents=1800
```

Chamadas com erro também devem ser registradas.
