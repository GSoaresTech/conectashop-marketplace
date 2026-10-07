# Logs

Logs das chamadas recebidas pelos servidores. Fazem parte da entrega final.

| Arquivo | Origem |
|---|---|
| `rest/server.log` | Servidor REST |
| `grpc/server.log` | Servidor gRPC |

Os dois servidores gravam direto nestes arquivos, sempre acrescentando linhas ao final.

## Formato mínimo

Cada linha deve conter horário, protocolo, equipe Servidor, equipe Cliente, Request ID, operação, entrada, status e resultado.

```
[2026-09-08T20:00:00] protocol=REST server=S03 client=C01 requestId=req-101 operation=GET_PRODUCT input=KB-100 status=200 result=OK
[2026-09-08T20:02:10] protocol=GRPC server=S03 client=C01 requestId=req-204 operation=CalculateShipping weight=1500 zone=LOCAL mode=STANDARD status=OK priceCents=1800
```

Chamadas com erro também devem ser registradas.

## Integração de 06/10/2026

Os arquivos versionados são os logs da máquina `172.16.17.59` no dia da integração, sem edição.

- `rest/server.log`: as linhas das 20:29 às 20:40 são as chamadas do Cliente C5, feitas pela página `/docs` do servidor. O C5 preencheu `X-Client-Team` com `S13`, o código do Servidor, por isso o campo `client` não mostra `C5`.
- `grpc/server.log`: só registra as inicializações do servidor. Nenhuma chamada gRPC chegou durante a janela.

A análise completa está no [relatório técnico](../docs/relatorio/).
