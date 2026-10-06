# Integração no laboratório

## Dados informados no sorteio

| Item | Valor |
|---|---|
| Código da equipe | |
| `REST_BASE_URL` | `http://<ip>:8080` |
| `GRPC_TARGET` | `<ip>:50051` |
| Estado | REST=UP; gRPC=UP |

Após o sorteio, só podem ser compartilhados endereço, porta, código da equipe e estado do serviço.

## Checklist antes do sorteio

- [ ] REST responde em `/api/v1` e está acessível por outra máquina.
- [ ] Catálogo e regras de cotação são exatamente os definidos.
- [ ] Headers ausentes geram o erro REST previsto.
- [ ] Todos os status HTTP e corpos de erro estão corretos.
- [ ] ShippingService usa exatamente o `shipping.proto` fornecido.
- [ ] Health retorna `SERVING` e o `server_team` correto.
- [ ] CalculateShipping implementa tarifa, peso por kg iniciado e prazo como definido.
- [ ] Erros gRPC retornam os status e descrições previstos.
- [ ] Logs registram Cliente e Request ID.
- [ ] `REST_BASE_URL` e `GRPC_TARGET` foram testados a partir de outra máquina.
- [ ] Nenhum requisito extra de autenticação ou configuração foi adicionado.

## Durante a janela de testes

1. Manter REST e gRPC ativos o tempo todo.
2. Não fornecer código, stubs ou detalhes internos aos Clientes.
3. Ao final, copiar os logs para `logs/rest/` e `logs/grpc/` e preencher a [matriz de integração](relatorio/matriz-integracao.md).
