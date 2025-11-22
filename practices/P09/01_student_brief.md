# Инструкция для студента (P09 — SBOM & уязвимости зависимостей, SCA в CI)

## 1) Ветка и структура

1. От ветки `main` создайте ветку:

```bash
git switch main
git pull
git switch -c p09-sbom-sca
```

2. Убедитесь, что базовый CI из P08 **не ломается**:

   * `.github/workflows/ci.yml` должен по-прежнему давать зелёный статус по `push`/`pull_request`.

3. Добавьте структуру для артефактов P09:

```bash
mkdir -p EVIDENCE/P09
```

(Файлы туда будет складывать CI; можно добавить `.gitkeep`, но это не обязательно.)

4. В `.github/workflows/` создайте файл:

* `.github/workflows/ci-sbom-sca.yml` — workflow для SBOM & SCA
  (см. шаблон в `practices/P09/06_templates/.github/workflows/ci-sbom-sca.yml` и сниппеты в `practices/P09/05_sbom_sca_snippets.md`).

5. (Опционально, но нужно для уровня «2») добавьте файл политики вейверов:

```bash
mkdir -p policy
touch policy/waivers.yml
```

Структуру можно взять из шаблона `practices/P09/06_templates/policy/waivers.yml`.

---

## 2) Минимальные требования к SBOM & SCA

**SBOM:**

* Генерируется автоматически внутри workflow при `push`/`pull_request` (и/или `workflow_dispatch`).
* Используется один из инструментов уровня Syft/Trivy:

  * пример: Syft, формат CycloneDX JSON.
* Результат сохраняется в файл:

```text
EVIDENCE/P09/sbom.json
```

**SCA:**

* Сканер использует SBOM как вход:

  * пример: Grype (`sbom:/work/EVIDENCE/P09/sbom.json`) или Trivy (`trivy fs`/`trivy sbom`).
* Отчёт сохраняется в:

```text
EVIDENCE/P09/sca_report.json
EVIDENCE/P09/sca_summary.md
```

* `sca_summary.md` может содержать агрегированную сводку по severity:

  * сколько Critical/High/Medium/Low, и краткий комментарий.

**CI-часть:**

* Workflow имеет понятное имя, например `Security - SBOM & SCA`;
* триггеры:

  * `workflow_dispatch` (ручной запуск),
  * `push` по `requirements*.txt`, `.py` и самому workflow;
* права — не шире, чем нужно (достаточно `permissions: contents: read`);
* артефакты `EVIDENCE/P09/*` загружаются через `actions/upload-artifact`.

---

## 3) Политика и waivers (для уровня «2»)

Посмотрите `project/69_sbom-vuln-mgmt.md` — там описано:

* какие severity считаются критичными,
* когда нужен фикс, когда waiver и на какой срок,
* как оформлять исключения в `policy/waivers.yml`.

Минимум для P09 (уровень «1»):

* наличие файла `policy/waivers.yml` с базовой структурой (пусть даже пока без реальных исключений);
* понимание, как вы будете использовать его дальше (кратко описать в PR).

Для уровня «2»:

* выбрать **1–2 уязвимости**, для которых:

  * либо сделать **обновление зависимости/фиксы** и показать это в PR,
  * либо оформить **waiver** с обоснованием, ссылкой на Issue/PR и сроком пересмотра.

Завязывать жёсткий **fail CI по High/Critical** на P09 не обязательно (это можно оставить на более поздние практики), но вы можете добавить такой порог как «stretch goal».

---

## 4) Локальная проверка (по желанию)

Если у вас есть Docker, вы можете повторить действия workflow локально (примеры в `practices/P09/05_sbom_sca_snippets.md`):

```bash
# SBOM (CycloneDX)
docker run --rm -v $PWD:/work -w /work anchore/syft:latest \
  packages dir:. -o cyclonedx-json > EVIDENCE/P09/sbom.json

# SCA (Grype) + сводка через jq
docker run --rm -v $PWD:/work -w /work anchore/grype:latest \
  sbom:/work/EVIDENCE/P09/sbom.json -o json > EVIDENCE/P09/sca_report.json

echo "# SCA summary" > EVIDENCE/P09/sca_summary.md
jq '[.matches[].vulnerability.severity] | group_by(.) | map({(.[0]): length}) | add' \
  EVIDENCE/P09/sca_report.json >> EVIDENCE/P09/sca_summary.md || true
```

> Если Docker/jq недоступны — ориентируйтесь на запуск через GitHub Actions.

---

## 5) PR и ревью

1. Запушьте ветку:

```bash
git add -A
git commit -m "P09: add SBOM & SCA workflow"
git push -u origin p09-sbom-sca
```

2. Откройте PR `p09-sbom-sca → main`:

* название в духе `P09 - SBOM & SCA (dependencies)`,
* в описании укажите:

  * какой инструмент используете для SBOM,
  * какой для SCA,
  * где лежат артефакты (`EVIDENCE/P09/...`),
  * есть ли у вас реальный фикс/waiver по уязвимости.

3. Запустите workflow (если он не запустился автоматически) через вкладку **Actions**.

4. Добейтесь **зелёного статуса job** `Security - SBOM & SCA`.

5. Ответьте на замечания ревьюера и доведите PR до merge-состояния.

---

## 6) Как использовать `secdev-seed-s09-s12`

Если вы не уверены в конфигурации, можно:

* клонировать/создать репозиторий из `secdev-seed-s09-s12`,
* посмотреть готовый workflow `ci-s09-sbom-sca.yml` и структуру `EVIDENCE/S09`,
* адаптировать эту конфигурацию под свой проект (`EVIDENCE/P09/`, название job, триггеры).

**Важно:** сдавать вы должны **из вашего основного course-project репозитория**, а не из seed-репо.
