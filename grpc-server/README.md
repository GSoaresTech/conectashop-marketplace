# Servidor gRPC — ShippingService

- Responsável: membro3
- Tecnologia: Python 3.13, grpcio
- Contrato: [contracts/grpc/shipping.proto](../contracts/grpc/shipping.proto) e [regras do serviço](../contracts/grpc/README.md)
- Backlog: épico E03 (F09 a F14)

## Estrutura

| Arquivo | Conteúdo |
|---|---|
| `main.py` | Servidor, validações, cálculo do frete e logs |
| `shipping_pb2.py` e `shipping_pb2_grpc.py` | Stubs gerados a partir do contrato (não editar) |
| `testes_grpc.py` | Chamadas G1–G5 contra o servidor em execução |

## Variáveis de ambiente

| Variável | Padrão |
|---|---|
| `SERVER_TEAM` | `S00` |
| `GRPC_PORT` | `50051` |

O host é fixo em `0.0.0.0`, então o serviço aceita conexões de outras máquinas.

## Execução

Todos os comandos são executados dentro de `grpc-server/`.

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

### Gerar os stubs

`shipping_pb2.py` e `shipping_pb2_grpc.py` já estão no repositório. Só é preciso gerar de novo se forem apagados:

```bash
python -m grpc_tools.protoc -I../contracts/grpc --python_out=. --grpc_python_out=. ../contracts/grpc/shipping.proto
```

### Iniciar o servidor

Linux:

```bash
SERVER_TEAM=S03 python main.py
```

Windows (CMD):

```bat
set SERVER_TEAM=S03
python main.py
```

O serviço fica disponível em `<ip-da-maquina>:50051`. O terminal mostra o andamento de cada chamada recebida.

### Testes

Com o servidor em execução, em outro terminal com o ambiente ativado:

```bash
python testes_grpc.py
```

Por padrão o script chama `localhost:50051`. Para testar o servidor de outra máquina, informe o endereço em `GRPC_TARGET`:

```bash
GRPC_TARGET=172.16.17.59:50051 python testes_grpc.py
```

### Exemplo de chamada

```bash
python -c "import grpc, shipping_pb2 as pb, shipping_pb2_grpc as rpc; c = rpc.ShippingServiceStub(grpc.insecure_channel('localhost:50051')); print(c.Health(pb.HealthRequest(), metadata=[('x-client-team', 'C01')]))"
```

## Logs

Cada chamada recebida é gravada em `logs/grpc/server.log`, na raiz do repositório, no mesmo formato do log REST descrito em [logs/README.md](../logs/README.md).
