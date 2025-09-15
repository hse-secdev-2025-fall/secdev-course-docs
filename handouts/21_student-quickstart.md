# Быстрый старт студента (с нуля до первого PR)

## 1) Примите assignment и клонируйте репозиторий
- Откройте инвайт‑ссылку Classroom → `Accept` → дождитесь создания приватного репозитория.
- Клонируйте:
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

## 3) Создайте ветку P01 и сделайте изменения
```bash
git checkout -b p01-setup
```
- Поправьте `README.md` (цели, запуск, тесты).
- Укажите приватный контакт в `SECURITY.md`.
- Убедитесь, что `pre-commit run --all-files` чистый.

## 4) Закоммитьте и откройте PR
```bash
git add -A
git commit -m "chore(p01): repo hygiene, README/SECURITY"
git push -u origin p01-setup
```
- Откройте PR «**P01 - repo hygiene**», заполните шаблон.

## 5) Сделайте CI зелёным
- Если CI красный - откройте `Actions` → логи. Частые фиксы:
```bash
ruff check --fix . && black . && isort .
pytest -q
```
- Закоммитьте исправления.

## 6) Запросите ревью и смёржьте
- Запросите ревью у `@hse-secdev-2025-fall/instructors`.
- Закройте **blocking** замечания → **merge** в `main` → поставьте тег `P01`:
```bash
git tag P01 && git push --tags
```

### Частые проблемы
- `src refspec main does not match any` - делайте PR из ветки `p01-setup` (push в `main` запрещён).
- CRLF/переводы строк - `.gitattributes` + `git add --renormalize .`.
- Секреты в репо - удалите, инвалидируйте, сообщите приватно (см. `SECURITY.md`).
