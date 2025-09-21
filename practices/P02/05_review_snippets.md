# Полезные сниппеты для P02 — Git-процессы и рецензирование

Ниже — минимальные заготовки, которые студенты могут **скопировать в свой репозиторий**.
Рекомендуемая раскладка:
- `.github/CODEOWNERS` — владельцы компонентов для авто-подписания ревью;
- `docs/REVIEW_CHECKLIST.md` — чек-лист ревьюера (и как DoD в PR);
- защита ветки `main` — через GitHub UI (или `gh api`).

---

## 1) CODEOWNERS (минимум)

Скопируйте в файл `.github/CODEOWNERS`:

```txt
# Глобальный владелец (на курс)
*                 @instructors

# Пример владельцев по компонентам (замените на свои команды/логины)
app/auth/*        @instructors
app/api/*         @instructors
```

> Как это работает: при изменениях в указанных путях GitHub автоматически добавит владельцев в ревьюеры PR.

---

## 2) Чек-лист ревью (минимальный)

Скопируйте в `docs/REVIEW_CHECKLIST.md` и прикладывайте ссылку в PR:

```md
# Check-list Code Review (минимальный)
- [ ] Объём PR разумный; цель понятна (одна тема на PR)
- [ ] Изменения покрыты тестами (позитив/негатив)
- [ ] Обработка ошибок и граничных случаев
- [ ] Именование и структура кода понятны
- [ ] Док/комментарии релевантны и точны
```

Рекомендации ревьюеру:
- Комментируйте **по делу** и по строкам/диффу, избегайте «LGTM» без аргументов;
- Используйте *Request changes* для блокирующих замечаний;
- Старайтесь оставлять **конкретные** предложения исправлений.

---

## 3) Защита ветки `main` и required-checks

### Через GitHub UI (быстрый путь)
Settings → Branches → **Add rule** → Branch name pattern: `main`  
Включите (как минимум):
- ☑ **Require a pull request before merging**
- ☑ **Require status checks to pass before merging** → добавьте **CI / build**
- ⛔ **Restrict who can push to matching branches** (запрет прямых пушей/force-push)

(Опционально) если используете CODEOWNERS:
- ☑ **Require review from Code Owners**

### Через GitHub CLI (опционально, для продвинутых)
Запустите в каталоге репозитория (требует `gh auth login`):

```bash
gh api -X PUT -H "Accept: application/vnd.github+json" \
  "/repos/${GITHUB_REPOSITORY}/branches/main/protection" \
  -f required_status_checks.strict=true \
  -f required_status_checks.contexts[]="CI / build" \
  -f enforce_admins=true \
  -f required_pull_request_reviews.dismiss_stale_reviews=true \
  -f required_pull_request_reviews.required_approving_review_count=1 \
  -f allow_force_pushes=false \
  -f allow_deletions=false
```

> Убедитесь, что имя статуса совпадает с вашим CI-job (у нас — `CI / build`).

---

### Подсказка для студентов
- Один PR — **одна** законченная тема; 
- Заполняйте шаблон PR: «что/почему/как проверял» + ссылку на чек-лист;
- Не забывайте про связь с Issue/задачей и зелёный `CI / build`.
