# P01 — Repo Hygiene & Bootstrap (инструкция для студента)

## Что нужно сдать
PR из ветки `p01-setup` в `main` + зелёный CI + тег `P01`.

## Шаги

1) **Клонирование и ветка**
```bash
git clone <URL вашего репозитория>
cd <repo>
git switch -c p01-setup
```

2) **Минимальная гигиена в репозитории**
- Обнови `README.md`: как запускать приложение и тесты.
- Добавь/обнови `SECURITY.md`: как сообщать об уязвимостях, контакты.
- Убедись, что есть `.gitattributes` для нормализации перевода строк.
- Проверь наличие `.pre-commit-config.yaml`.

3) **Установка инструментов и локальные проверки**
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt || true
pip install ruff black isort pytest pre-commit
pre-commit install
pre-commit run --all-files
ruff check --fix .
black .
isort .
pytest -q
```

4) **CI**
- Проверь, что `.github/workflows/ci.yml` присутствует (см. `05_ci_snippets.md`).
- Если локально всё зелёное — запушь ветку:
```bash
git add -A
git commit -m "P01: bootstrap repo hygiene (CI, pre-commit, README, SECURITY)"
git push -u origin p01-setup
```

5) **PR и ревью**
- Открой PR `p01-setup → main` по шаблону, запроси ревью у преподавателей.
- Исправь замечания, добейся **зелёного CI**.

6) **Merge и тег**
После merge в `main` поставь тег:
```bash
git tag P01
git push --tags
```

### Траблшутинг
- Ошибка с веткой `main`: сделай хотя бы один коммит в `p01-setup` и открой PR (прямые пуши в `main` запрещены).
- Проблемы с переводами строк: добавь `.gitattributes` и выполни `git add --renormalize .`.
- Закоммиченные секреты: немедленно удали из кода/истории, инвалидируй в провайдере и сообщи преподавателю.