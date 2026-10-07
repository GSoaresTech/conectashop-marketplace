# Relatório técnico

- Responsável: Deyvid Gustavo
- Backlog: épico E04 (F17 e F18)

| Arquivo | Conteúdo |
|---|---|
| [relatorio-tecnico.pdf](relatorio-tecnico.pdf) | Relatório final para leitura e entrega |
| [relatorio-tecnico.docx](relatorio-tecnico.docx) | Mesmo relatório em formato editável |
| [matriz-integracao.md](matriz-integracao.md) | Matriz dos Clientes que testaram a equipe e resultado por teste |

## Estrutura do relatório

1. Identificação da equipe e tecnologias escolhidas.
2. Arquitetura dos dois servidores.
3. `REST_BASE_URL` e `GRPC_TARGET` usados na atividade.
4. Testes internos antes do sorteio.
5. Matriz com os Clientes que testaram o grupo e resultado observado para R1 a R5 e G1 a G5.
6. Trechos de log do Servidor e, quando fornecidos, do Cliente com o mesmo Request ID.
7. Falhas observadas, causa provável ou confirmada e correções feitas sem alterar o contrato.
8. Comparação REST × gRPC do ponto de vista de quem implementou os servidores.
9. Conclusão sobre interoperabilidade entre tecnologias diferentes.

## Classificação de falhas

| Categoria | Exemplo |
|---|---|
| Rede ou ambiente | Porta bloqueada, IP incorreto, serviço fora do ar |
| Divergência de contrato | Campo, path ou tipo diferente do definido |
| Regra de negócio | Valor de cotação ou frete incorreto |
| Erro do Cliente | Header ou metadata ausente, body inválido |
