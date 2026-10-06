# Relatório técnico

- Responsável: Deyvid
- Formato de entrega: PDF ou DOCX, conforme orientação do professor
- Backlog: épico E04 (F17 e F18)

O arquivo final deve ser salvo nesta pasta.

## Estrutura mínima

1. Identificação da equipe e tecnologias escolhidas.
2. Arquitetura dos dois servidores.
3. `REST_BASE_URL` e `GRPC_TARGET` usados na atividade.
4. Tabela com os 2 Clientes REST e os 2 Clientes gRPC que testaram o grupo ([matriz-integracao.md](matriz-integracao.md)).
5. Resultado observado para R1–R5 e G1–G5.
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
