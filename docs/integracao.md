# Integração no laboratório

## Dados informados no sorteio

| Item | Valor |
|---|---|
| Código da equipe | S13 |
| `REST_BASE_URL` | `http://172.16.17.59:8080` |
| `GRPC_TARGET` | `172.16.17.59:50051` |
| Estado | REST=UP; gRPC=UP |
| Cliente sorteado | C5 (REST e gRPC) |
| Data | 06/10/2026 |

Após o sorteio, só podem ser compartilhados endereço, porta, código da equipe e estado do serviço.

## Checklist antes do sorteio

- [x] REST responde em `/api/v1` e está acessível por outra máquina.
- [x] Catálogo e regras de cotação são exatamente os definidos.
- [x] Headers ausentes geram o erro REST previsto.
- [x] Todos os status HTTP e corpos de erro estão corretos.
- [x] ShippingService usa exatamente o `shipping.proto` fornecido.
- [x] Health retorna `SERVING` e o `server_team` correto.
- [x] CalculateShipping implementa tarifa, peso por kg iniciado e prazo como definido.
- [x] Erros gRPC retornam os status e descrições previstos.
- [x] Logs registram Cliente e Request ID.
- [x] `REST_BASE_URL` foi testado a partir de outra máquina (chamadas do C5 durante a janela).
- [ ] `GRPC_TARGET` foi testado a partir de outra máquina. O serviço ficou ativo, mas o log do laboratório não registra nenhuma chamada externa. Antes da aula ele foi testado só pelo IP da própria máquina.
- [x] Nenhum requisito extra de autenticação ou configuração foi adicionado.

## Durante a janela de testes

1. Manter REST e gRPC ativos o tempo todo.
2. Não fornecer código, stubs ou detalhes internos aos Clientes.
3. Ao final, conferir os logs em `logs/rest/` e `logs/grpc/` e preencher a [matriz de integração](relatorio/matriz-integracao.md).

## Resultado

A aplicação Cliente do C5 teve problemas técnicos e não executou a bateria de testes. O C5 testou o REST pela página `/docs` do nosso servidor e não fez chamadas gRPC. Os detalhes estão na [matriz de integração](relatorio/matriz-integracao.md) e no [relatório técnico](relatorio/).
