# Git / GitHub - Шпаргалка по рабочему процессу

## Ветки
```bash
git checkout -b p02-git-review   # создать и переключиться
git switch main                  # вернуться на main
git pull --ff-only               # подтянуть обновления
```

## Коммиты
```bash
git add -A
git commit -m "feat(p02): add minimal CRUD and tests"
git log --oneline --graph --decorate -n 10
```

## Публикация ветки и PR
```bash
git push -u origin p02-git-review
# Далее - открыть PR через веб‑интерфейс GitHub и выбрать цель: main
```

## Обновление PR после правок
```bash
git add -A
git commit -m "fix: address review comments"
git push
```

## Слияние после зачёта
```bash
git switch main
git pull --ff-only
git merge --no-ff p02-git-review
git push
git tag P02 && git push --tags
```

## Разрешение конфликтов (кратко)
```bash
git fetch origin
git merge origin/main   # в вашей фича-ветке
# отредактировать конфликтующие файлы, затем:
git add <files>
git commit
git push
```

## Сообщения коммитов (рекомендации)
- Императив: `feat/fix/chore/docs/test(ref): что и зачем`
- Один коммит - одна логическая единица
- Избегайте `misc fixes` / `wip`
