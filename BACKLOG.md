# Backlog

Hierarquia: ÉPICO (`Exx`) → FEATURE (`Fxx`) → USER STORY (`USxx`).
Cada feature corresponde a uma branch. Status: `A fazer`, `Em andamento`, `Concluído`.

## Resumo

| Épico | Feature | Responsável | Branch | Status |
|---|---|---|---|---|
| E01 | F01 Estrutura do repositório | Gabriel | `feature/f01-estrutura-repositorio` | Concluído |
| E02 | F02 Configuração do servidor REST | Gabriel | `feature/rest-server` | Concluído |
| E02 | F03 Headers obrigatórios | Gabriel | `feature/rest-server` | Concluído |
| E02 | F04 Consulta de produto | Gabriel | `feature/rest-server` | Concluído |
| E02 | F05 Cotação | Gabriel | `feature/rest-server` | Concluído |
| E02 | F06 Erros padronizados | Gabriel | `feature/rest-server` | Concluído |
| E02 | F07 Logs REST | Gabriel | `feature/rest-server` | Concluído |
| E02 | F08 Testes REST | Gabriel | `feature/rest-server` | Concluído |
| E03 | F09 Configuração do servidor gRPC | membro3 | `feature/f09-grpc-configuracao` | A fazer |
| E03 | F10 Health | membro3 | `feature/f10-grpc-health` | A fazer |
| E03 | F11 Validação de entrada | membro3 | `feature/f11-grpc-validacao` | A fazer |
| E03 | F12 Cálculo de frete | membro3 | `feature/f12-grpc-frete` | A fazer |
| E03 | F13 Logs gRPC | membro3 | `feature/f13-grpc-logs` | A fazer |
| E03 | F14 Testes gRPC | membro3 | `feature/f14-grpc-testes` | A fazer |
| E04 | F15 Validação em rede | Gabriel e membro3 | `feature/f15-validacao-rede` | A fazer |
| E04 | F16 Instruções de execução | Gabriel e membro3 | `feature/f16-instrucoes-execucao` | A fazer |
| E04 | F17 Registro das integrações | Deyvid | `feature/f17-registro-integracoes` | A fazer |
| E04 | F18 Relatório técnico | Deyvid | `feature/f18-relatorio-tecnico` | A fazer |

---

## E01 — Base do repositório

### F01 Estrutura do repositório

- **US01** Como membro da equipe, quero pastas separadas por componente, para trabalhar sem conflito com os demais.
- **US02** Como membro da equipe, quero os contratos REST e gRPC no repositório, para usá-los como única referência.
- **US03** Como membro da equipe, quero regras de branch e commit, para manter o histórico organizado.
- **US04** Como membro da equipe, quero um backlog com responsáveis, para saber o que cada um entrega.

---

## E02 — Servidor REST (Catalog & Quote API)

Referência: [contracts/rest/catalog-quote-api.md](contracts/rest/catalog-quote-api.md)

### F02 Configuração do servidor REST

- **US05** Como equipe Servidor, quero definir host, porta e código da equipe por variável de ambiente, para ajustar o serviço no laboratório sem alterar código.
  - Padrão `0.0.0.0:8080`.
  - Rotas sob `/api/v1`.
  - Respostas em `application/json; charset=utf-8`.

### F03 Headers obrigatórios

- **US06** Como Cliente, quero receber erro quando faltar `X-Client-Team` ou `X-Request-ID`, para corrigir a chamada.
  - HTTP 400, code `MISSING_REQUIRED_HEADER`.
- **US07** Como Cliente, quero receber o `X-Request-ID` no header da resposta, para correlacionar a chamada.

### F04 Consulta de produto

- **US08** Como Cliente, quero consultar um produto pelo SKU, para obter nome, preço e disponibilidade.
  - Catálogo fixo em memória com os 4 SKUs do contrato.
  - HTTP 200 com `sku`, `name`, `unitPriceCents`, `available`.
- **US09** Como Cliente, quero ser informado quando o SKU não existir.
  - HTTP 404, code `PRODUCT_NOT_FOUND`.

### F05 Cotação

- **US10** Como Cliente, quero enviar uma lista de itens e receber subtotal, desconto e total.
  - Desconto: abaixo de 50000 → 0%; 50000 a 99999 → 5%; 100000 ou mais → 10%.
  - `discountCents` truncado para inteiro.
  - Resposta com `requestId`, `subtotalCents`, `discountPercent`, `discountCents`, `totalCents`.
- **US11** Como Cliente, quero receber erro específico quando a cotação for inválida.
  - SKU inexistente: HTTP 422, `INVALID_PRODUCT`.
  - Quantidade fora de 1 a 10, lista fora de 1 a 5 itens ou SKU duplicado: HTTP 422, `INVALID_QUANTITY_OR_ITEMS`.

### F06 Erros padronizados

- **US12** Como Cliente, quero que todo erro siga o formato `{code, message, requestId}`, para tratar falhas da mesma forma.
  - JSON inválido ou campo obrigatório ausente: HTTP 400, `INVALID_REQUEST`.
  - Erro inesperado: HTTP 500, `INTERNAL_ERROR`.

### F07 Logs REST

- **US13** Como equipe Servidor, quero registrar toda chamada recebida, para analisar falhas de integração.
  - Formato definido em [logs/README.md](logs/README.md).
  - Gravação em `logs/rest/`, incluindo chamadas com erro.

### F08 Testes REST

- **US14** Como equipe Servidor, quero testes automatizados de R1 a R5 e dos casos de erro, para validar o contrato antes do sorteio.

---

## E03 — Servidor gRPC (ShippingService)

Referência: [contracts/grpc/README.md](contracts/grpc/README.md)

### F09 Configuração do servidor gRPC

- **US15** Como equipe Servidor, quero gerar os stubs a partir de `contracts/grpc/shipping.proto`, para garantir compatibilidade com qualquer Cliente.
- **US16** Como equipe Servidor, quero definir host, porta e código da equipe por variável de ambiente, para ajustar o serviço no laboratório sem alterar código.
  - Padrão `0.0.0.0:50051`.

### F10 Health

- **US17** Como Cliente, quero chamar `Health`, para confirmar que alcancei o Servidor correto.
  - Resposta `status=SERVING` e `server_team` com o código da equipe.

### F11 Validação de entrada

- **US18** Como Cliente, quero receber `INVALID_ARGUMENT` com descrição específica quando a requisição for inválida.
  - `x-client-team` ausente: `MISSING_CLIENT_TEAM`.
  - `request_id` vazio: `MISSING_REQUEST_ID`.
  - `weight_grams` fora de 1 a 30000: `INVALID_WEIGHT`.
  - `zone` não especificada: `INVALID_ZONE`.
  - `mode` não especificado: `INVALID_MODE`.

### F12 Cálculo de frete

- **US19** Como Cliente, quero calcular o frete por peso, zona e modo, para obter preço e prazo.
  - `price_cents = tarifa_base + teto(weight_grams / 1000) × adicional`.
  - Prazo conforme tabela do contrato.
  - Resposta repete `request_id` e preenche `server_team`.
  - Erro inesperado: `INTERNAL`, `INTERNAL_ERROR`.

### F13 Logs gRPC

- **US20** Como equipe Servidor, quero registrar toda chamada recebida, para analisar falhas de integração.
  - Formato definido em [logs/README.md](logs/README.md).
  - Gravação em `logs/grpc/`, incluindo chamadas com erro.

### F14 Testes gRPC

- **US21** Como equipe Servidor, quero testes automatizados de G1 a G5 e dos casos de erro, para validar o contrato antes do sorteio.

---

## E04 — Integração e entrega

### F15 Validação em rede

- **US22** Como equipe Servidor, quero acessar REST e gRPC a partir de outra máquina, para garantir que os Clientes conseguirão conectar.
  - Checklist de [docs/integracao.md](docs/integracao.md) concluído.

### F16 Instruções de execução

- **US23** Como avaliador, quero instruções de instalação e execução, para iniciar os dois serviços.
  - Tecnologia, dependências, portas configuráveis e comandos exatos no README.

### F17 Registro das integrações

- **US24** Como equipe, quero a matriz de integração preenchida, para comprovar os testes recebidos.
  - [docs/relatorio/matriz-integracao.md](docs/relatorio/matriz-integracao.md) com Clientes, resultados e Request IDs.
- **US25** Como equipe, quero os logs das integrações versionados, para servir de evidência.
  - Logs copiados para `logs/rest/` e `logs/grpc/`.

### F18 Relatório técnico

- **US26** Como professor, quero um relatório técnico, para avaliar resultados, falhas e análise da equipe.
  - Estrutura definida em [docs/relatorio/README.md](docs/relatorio/README.md).
  - Entrega em PDF ou DOCX.
