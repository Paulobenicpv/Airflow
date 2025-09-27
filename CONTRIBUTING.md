# Contribuindo

Obrigado por contribuir!

## Como começar
1. Faça um fork e crie uma branch: `git checkout -b feature/minha-feature`.
2. Rode os checks locais: `pre-commit run -a && pytest -q`.
3. Garanta que os DAGs carregam: `airflow dags list`.
4. Abra um PR para `main` com descrição clara (use o template).

## Convenções
- Commits: **Conventional Commits** (ex.: `feat:`, `fix:`, `docs:`).
- Código: `black`, `isort`, `ruff` – executados via CI e pre-commit.
- Testes: inclua testes unitários/integrados onde fizer sentido.
- Segurança: **não** inclua segredos; use o Secrets Backend.

## Processo de revisão
- 1+ aprovação obrigatória.
- CI precisa passar (lint, testes, DagBag, build de imagem).