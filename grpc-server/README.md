# Servidor gRPC — ShippingService

- Responsável: membro3
- Tecnologia: Python 3.13, grpcio, grpcio-tools
- Contrato: [contracts/grpc/shipping.proto](../contracts/grpc/shipping.proto)
- Backlog: épico E03 (F09 a F14)

## Estrutura

| Arquivo | Conteúdo |
|---|---|
| `server/main.py` | Inicialização do servidor |
| `server/config.py` | Variáveis de ambiente |
| `server/shipping_service.py` | Health e CalculateShipping |
| `server/shipping_rules.py` | Tarifa, adicional por kg e prazo |
| `server/logs.py` | Registro das chamadas recebidas |
| `server/generated/` | Stubs gerados a partir do `.proto` |
| `tests/` | Testes G1–G5 e casos de erro |

## Variáveis de ambiente

| Variável | Padrão |
|---|---|
| `SERVER_TEAM` | `S00` |
| `GRPC_HOST` | `0.0.0.0` |
| `GRPC_PORT` | `50051` |

## Geração dos stubs

Os stubs devem ser gerados a partir de `contracts/grpc/shipping.proto`, sem cópias ou alterações do arquivo.

```bash
python -m grpc_tools.protoc -I ../contracts/grpc \
  --python_out=server/generated \
  --grpc_python_out=server/generated \
  ../contracts/grpc/shipping.proto
```

## Execução

A definir na feature F16.
