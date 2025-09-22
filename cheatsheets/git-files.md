# Шпаргалка 2 — Git‑файлы и «что за что отвечает»

## `.gitignore` — что не коммитить
**Назначение:** список путей/масок, которые Git игнорирует.

Пример для Python:
```gitignore
__pycache__/
.venv/
.idea/ .vscode/
.pytest_cache/
.env
*.pyc
```

## `.gitattributes` — политика текста/бинарников и EOL
**Зачем:** у разных ОС разные переводы строк (CRLF/LF) → «шум» в диффах.  
**Решение:** единая политика EOL и типы файлов.

Мини‑пример:
```gitattributes
* text=auto eol=lf
*.md  text eol=lf
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
```

После добавления обязательно:
```bash
git add --renormalize .
git commit -m "chore: normalize line endings"
```

## `.github/` — интеграция с GitHub
- `workflows/ci.yml` — **GitHub Actions (CI)**: что запускать при PR/push.
- `CODEOWNERS` — владельцы путей (авто‑запрос ревью, если включено «Require review from Code Owners»).
  ```txt
  *            @org/instructors
  app/auth/*   @org/auth-team
  ```
- `PULL_REQUEST_TEMPLATE.md` — шаблон описания PR (что/почему/как проверял).
- `ISSUE_TEMPLATE/` — шаблоны задач/багов (по желанию).

## `.gitkeep` / `.keep`
Фиктивный файл, чтобы **пустая папка** попала в Git (сам Git пустые каталоги не хранит).

## `README.md` и `SECURITY.md`
- `README.md` — как запускать/тестировать, где что лежит.
- `SECURITY.md` — как репортить уязвимости, сроки реакции (SLA), контакт.

## (по необходимости) `.gitmodules`
Появляется при использовании **submodules** (в курсе обычно не нужно).
