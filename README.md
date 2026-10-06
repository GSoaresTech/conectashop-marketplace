# ConectaShop — Grupo Servidor

Servidores REST e gRPC da dinâmica de interoperabilidade da disciplina de Sistemas Distribuídos e Computação Paralela.

| Serviço | Contrato | Porta padrão | Tecnologia |
|---|---|---|---|
| Catalog & Quote API (REST) | [catalog-quote-api.md](contracts/rest/catalog-quote-api.md) | 8080 | Python, FastAPI |
| ShippingService (gRPC) | [shipping.proto](contracts/grpc/shipping.proto) | 50051 | Python, grpcio |

## Equipe

| Membro | Responsabilidade | Pasta |
|---|---|---|
| Gabriel | Servidor REST | `rest-server/` |
| membro3 | Servidor gRPC | `grpc-server/` |
| Deyvid | Relatório técnico | `docs/relatorio/` |

## Estrutura

```
contracts/          Contratos REST e gRPC (não alterar)
rest-server/        Servidor REST
grpc-server/        Servidor gRPC
logs/               Logs das chamadas recebidas
docs/
  integracao.md     Dados do sorteio e checklist
  relatorio/        Relatório técnico e matriz de integração
  referencias/      Guia da atividade
BACKLOG.md          Épicos, features e user stories
CONTRIBUTING.md     Padrão de branches e commits
.env.example        Variáveis de ambiente
```

## Execução

A definir na feature F16 do [BACKLOG](BACKLOG.md).

## Como contribuir

Ver [CONTRIBUTING.md](CONTRIBUTING.md).
