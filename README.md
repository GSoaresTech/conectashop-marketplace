# ConectaShop: Grupo Servidor

Servidores REST e gRPC da equipe S13 na dinâmica IntegraLab, da disciplina de Sistemas Distribuídos e Computação Paralela. Cada equipe implementou um lado dos mesmos contratos, Cliente ou Servidor, na tecnologia que quisesse, e as integrações entre equipes foram sorteadas no laboratório.

Projeto encerrado em 06/10/2026. O resultado está no [relatório técnico](docs/relatorio/relatorio-tecnico.pdf).

| Serviço | Contrato | Porta padrão | Tecnologia |
|---|---|---|---|
| Catalog & Quote API (REST) | [catalog-quote-api.md](contracts/rest/catalog-quote-api.md) | 8080 | Python 3.13, FastAPI |
| ShippingService (gRPC) | [shipping.proto](contracts/grpc/shipping.proto) | 50051 | Python 3.13, grpcio |

## Equipe

| Membro | Responsabilidade | Pasta |
|---|---|---|
| Gabriel Soares | Servidor REST | [rest-server/](rest-server/) |
| Gabriel Marques | Servidor gRPC | [grpc-server/](grpc-server/) |
| Deyvid Gustavo | Relatório técnico e testes de validação | [docs/relatorio/](docs/relatorio/) |

## Execução

Requisito: Python 3.13. Cada servidor tem o próprio ambiente virtual e roda em um terminal separado.

Servidor REST, em `http://<ip>:8080/api/v1`:

```bash
cd rest-server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
SERVER_TEAM=S13 python -m app.main
```

Servidor gRPC, em `<ip>:50051`:

```bash
cd grpc-server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
SERVER_TEAM=S13 python main.py
```

| Variável | Padrão | Uso |
|---|---|---|
| `SERVER_TEAM` | `S00` | Código da equipe nas respostas e nos logs |
| `REST_HOST` | `0.0.0.0` | Host do REST |
| `REST_PORT` | `8080` | Porta do REST |
| `GRPC_PORT` | `50051` | Porta do gRPC (o host é fixo em `0.0.0.0`) |

Comandos para Windows, testes automatizados e exemplos de chamada estão no README de cada servidor: [rest-server](rest-server/README.md) e [grpc-server](grpc-server/README.md).

## Resultado da integração

| Item | Valor |
|---|---|
| Código da equipe | S13 |
| `REST_BASE_URL` | `http://172.16.17.59:8080` |
| `GRPC_TARGET` | `172.16.17.59:50051` |
| Cliente sorteado | C5 (REST e gRPC) |

A aplicação Cliente do C5 teve problemas técnicos e não executou a bateria de testes. O C5 testou o REST pela página `/docs` do nosso servidor (R1, R5 e casos de erro, todos conforme o contrato), e nenhuma chamada gRPC chegou. Antes do sorteio, a equipe validou R1 a R5 e G1 a G5 com testes próprios.

- [Relatório técnico](docs/relatorio/relatorio-tecnico.pdf) ([DOCX](docs/relatorio/relatorio-tecnico.docx))
- [Matriz de integração](docs/relatorio/matriz-integracao.md)
- [Dados do sorteio e checklist](docs/integracao.md)
- [Logs das chamadas recebidas](logs/)

## Estrutura

```
contracts/            Contratos REST e gRPC (não alterar)
rest-server/          Servidor REST
grpc-server/          Servidor gRPC
logs/
  rest/server.log     Chamadas recebidas pelo REST
  grpc/server.log     Chamadas recebidas pelo gRPC
docs/
  integracao.md       Dados do sorteio e checklist
  relatorio/          Relatório técnico (PDF e DOCX) e matriz de integração
  referencias/        Guia da atividade
BACKLOG.md            Épicos, features e user stories
CONTRIBUTING.md       Padrão de branches e commits
.env.example          Variáveis de ambiente
```

O fluxo de branches e commits usado no projeto está em [CONTRIBUTING.md](CONTRIBUTING.md), e o andamento de cada feature no [BACKLOG](BACKLOG.md).
