# Инструкция для студента (P10 — SAST & Secrets)

## 1) Ветка и базовая структура

1. От `main` создайте рабочую ветку:

```bash
git switch main
git pull
git switch -c p10-sast-secrets
```

2. Убедитесь, что CI из P08–P09 **зелёный** на `main` (чтобы не маскировать старые проблемы).

3. Подготовьте каталоги и конфиги:

```bash
mkdir -p EVIDENCE/P10
mkdir -p security/semgrep
touch security/semgrep/rules.yml
touch security/.gitleaks.toml
```

4. В `.github/workflows/` создайте файл:

* `.github/workflows/ci-sast-secrets.yml` — workflow для Semgrep + Gitleaks.

Можно начать с шаблона из `practices/P10/06_templates/.github/workflows/ci-sast-secrets.yml`.

---

## 2) Минимальные требования к SAST (Semgrep)

**Задача:** запускать Semgrep при изменениях кода и конфигов, получать SARIF-отчёт и сохранять его в `EVIDENCE/P10/semgrep.sarif`.

Минимально достаточно:

* использовать базовый профиль `p/ci` (быстрые проверки для CI);
* при желании добавить 1–2 своих правила в `security/semgrep/rules.yml` под ваш проект;
* запускать Semgrep в CI через docker (как в шаблоне) или через `pip install semgrep`.

Пример ожидаемого результата:

* job `Security - SAST & Secrets` в Actions отработал зелёным;
* в артефактах job или в репозитории есть `EVIDENCE/P10/semgrep.sarif`;
* в описании PR — короткий комментарий: были ли findings, что с ними планируете делать.

---

## 3) Минимальные требования к secrets scanning (Gitleaks)

**Задача:** запускать Gitleaks на репозиторий и получать `EVIDENCE/P10/gitleaks.json`.

Минимально:

* сканируем **текущую рабочую копию** репозитория (`--source=/repo`), без истории коммитов;
* используем конфиг `security/.gitleaks.toml` (allowlist и базовые настройки);
* допускается, что на первом запуске будут false positives — важно их увидеть и зафиксировать.

Ожидаемый результат:

* в job артефактах есть `EVIDENCE/P10/gitleaks.json`;
* вы глазами посмотрели отчёт и:

  * либо подтвердили, что это настоящие секреты (и убрали их из кода),
  * либо добавили аккуратное исключение в `.gitleaks.toml` (по пути/regex) и зафиксировали это в описании PR.

---

## 4) Локальная проверка (по желанию)

Если хотите повторить CI локально (и у вас есть Docker):

```bash
# Семгреп (похожим образом, как в CI)
docker run --rm -v $PWD:/src returntocorp/semgrep:latest \
  semgrep ci --config p/ci --config /src/security/semgrep/rules.yml \
    --sarif --output /src/EVIDENCE/P10/semgrep.sarif --metrics=off || true

# Gitleaks
docker run --rm -v $PWD:/repo zricethezav/gitleaks:latest \
  detect --no-banner --config=/repo/security/.gitleaks.toml \
    --source=/repo --report-format=json \
    --report-path=/repo/EVIDENCE/P10/gitleaks.json || true
```

Если Docker недоступен — ориентируйтесь на запуск из GitHub Actions (workflow всё равно обязателен).

---

## 5) PR и ревью

1. Зафиксируйте изменения:

```bash
git add -A
git commit -m "P10: add SAST & secrets scanning"
git push -u origin p10-sast-secrets
```

2. Откройте PR `p10-sast-secrets → main`:

* заголовок в духе: `P10 - SAST & Secrets (Semgrep + Gitleaks)`;
* в описании PR укажите:

  * где лежат отчёты: `EVIDENCE/P10/semgrep.sarif`, `EVIDENCE/P10/gitleaks.json`;
  * какие профили/правила Semgrep использованы;
  * нашли ли вы реальные проблемы / секреты и что с ними сделали.

3. Запустите workflow (если он не стартанул автоматически) через вкладку **Actions**.

4. Добейтесь **зелёного** статуса job `Security - SAST & Secrets`.

5. Ответьте на комментарии ревьюера и доведите PR до состояния, когда его можно мерджить.

---

## 6) Как использовать `secdev-seed-s09-s12` в качестве примера

Если вы не уверены в конфигурации:

* посмотрите на workflow `.github/workflows/ci-s10-sast-secrets.yml` в `secdev-seed-s09-s12`;
* изучите, как там устроены:

  * `EVIDENCE/S10/semgrep.sarif`,
  * `EVIDENCE/S10/gitleaks.json`,
  * `security/semgrep/rules.yml`,
  * `security/.gitleaks.toml`.

Можно сначала воспроизвести похожую схему в своём проекте, а затем постепенно её ужесточать (добавлять свои правила, пороги и т.д.).

**Важно:** финальная сдача P10 идёт **из вашего course-project репозитория**, а не из seed-репо.
