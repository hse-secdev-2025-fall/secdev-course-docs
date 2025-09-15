# P01: что сделать (коротко)

1) Создай ветку `p01-setup` от `main`.
2) Добавь/обнови: `README`, `SECURITY.md`, `.pre-commit-config.yaml`, CI workflow.
3) Запусти локально: `ruff/black/isort`, `pytest -q`, `pre-commit run --all-files`.
4) Открой PR по шаблону, запроси ревью у `@instructors`.
5) Добейся **зелёного CI**, закрой blocking, merge и поставь тег `P01`.


## Импорт из student-steps.md

# P01 — Подробные шаги для студента

## 1) Примите assignment и клонируйте
```bash
git clone https://github.com/hse-secdev-2025-fall/<your-repo>.git
cd <your-repo>
```

## 2) Настройте окружение
```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt
pre-commit install
pytest -q
```

## 3) Ветка и изменения
```bash
git checkout -b p01-setup
```
- Обновите `README.md` (цели, запуск, тесты)
- Укажите контакт в `SECURITY.md`
- Проверьте `pre-commit run --all-files`

## 4) Коммит и PR
```bash
git add -A
git commit -m "chore(p01): repo hygiene, README/SECURITY"
git push -u origin p01-setup
```
Откройте PR «P01 — repo hygiene», заполните шаблон.

## 5) CI → зелёный
- Исправьте форматирование: `ruff check --fix . && black . && isort .`
- Прогоните `pytest -q`, повторите коммит.

## 6) Ревью и merge
- Запросите ревью у `@hse-secdev-2025-fall/instructors`
- Закройте blocking-замечания → merge в `main`

## 7) Тег
```bash
git tag P01
git push --tags
```

### Траблшутинг
- `src refspec main` → сделайте коммит в ветке `p01-setup` и откройте PR (в `main` пуш запрещён).
- CRLF/переводы строк → `.gitattributes` + `git add --renormalize .`
- Секреты в репо → удалить, инвалидировать, сообщить преподавателю.
