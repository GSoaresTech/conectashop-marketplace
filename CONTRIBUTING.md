# Fluxo de trabalho

## Branches

- `main`: versão estável. Não recebe commits diretos.
- Cada feature do [BACKLOG](BACKLOG.md) tem uma branch própria, criada a partir da `main`.

| Tipo | Padrão | Exemplo |
|---|---|---|
| Feature | `feature/fNN-descricao` | `feature/f05-rest-cotacao` |
| Correção | `fix/fNN-descricao` | `fix/f05-desconto-arredondamento` |

`fNN` é o código da feature no backlog. A descrição usa letras minúsculas e hífens.

## Passo a passo

```bash
git switch main
git pull
git switch -c feature/f05-rest-cotacao
# commits
git push -u origin feature/f05-rest-cotacao
```

1. Abrir pull request para a `main`.
2. Outro membro revisa.
3. Merge sem fast-forward (`--no-ff`) para manter a feature visível no histórico.
4. Atualizar o status da feature no BACKLOG.

## Commits

Formato:

```
<tipo>(<escopo>): <descrição no imperativo>

Refs: USNN
```

| Tipo | Uso |
|---|---|
| `feat` | Nova funcionalidade |
| `fix` | Correção |
| `test` | Testes |
| `docs` | Documentação |
| `refactor` | Mudança de código sem alterar comportamento |
| `chore` | Estrutura, dependências e configuração |

| Escopo | Pasta |
|---|---|
| `rest` | `rest-server/` |
| `grpc` | `grpc-server/` |
| `contratos` | `contracts/` |
| `relatorio` | `docs/relatorio/` |
| `logs` | `logs/` |
| `repo` | Arquivos da raiz e `docs/` |

Exemplos:

```
feat(rest): adiciona endpoint GET /products/{sku}
test(grpc): adiciona testes G1 a G5
fix(rest): corrige status do erro de SKU duplicado
```

Cada commit deve conter uma única mudança lógica.

## Regras

- Os arquivos em `contracts/` não podem ser alterados.
- Cada membro trabalha na própria pasta. Mudanças em arquivos da raiz devem ser avisadas ao grupo.
