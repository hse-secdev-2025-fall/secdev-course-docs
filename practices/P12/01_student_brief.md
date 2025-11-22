# Инструкция для студента (P12 — IaC & Container Security)

## 1) Ветка и подготовка

1. Перейдите на актуальный `main` и создайте ветку:

```bash
git switch main
git pull
git switch -c p12-iac-container
```

2. Убедитесь, что:

* у вас есть `Dockerfile` для приложения (P07);
* есть хотя бы минимальные IaC-манифесты (например, `k8s/`, `deploy/`, `iac/`, Terraform или docker-compose) — если нет, создайте простейшее описание инфраструктуры по примеру из `secdev-course-docs` или seed-репозитория;
* базовый CI из P08–P11 работает.

---

## 2) Структура для P12

Создайте каталоги и файлы:

```bash
mkdir -p EVIDENCE/P12
mkdir -p security
touch security/hadolint.yaml
touch security/checkov.yaml
touch security/trivy.yaml  # опционально, но полезно
```

IaC-артефакты:

* если уже есть `k8s/` или `iac/` — используйте их;
* если нет ничего, создайте:

```bash
mkdir -p iac
# мини-пример K8s-манифеста или docker-compose.yaml под ваш сервис
```

---

## 3) Workflow `ci-p12-iac-container.yml`

1. Скопируйте шаблон из `secdev-course-docs`:

   * `practices/P12/06_templates/.github/workflows/ci-p12-iac-container.yml`

2. Положите его в свой репозиторий:

```text
.github/workflows/ci-p12-iac-container.yml
```

3. Проверьте/подправьте внутри:

* путь к `Dockerfile` (по умолчанию `Dockerfile` в корне);
* путь к IaC (например, `iac/`, `k8s/`, `deploy/`);
* имя и тег образа, который будет собираться (например, `app:local`).

Workflow должен:

1. Собрать контейнерный образ из вашего `Dockerfile`;
2. Прогнать Hadolint по `Dockerfile` (через docker-образ hadolint);
3. Прогнать Checkov по каталогу с IaC;
4. Прогнать Trivy по собранному образу;
5. Сохранить отчёты в `EVIDENCE/P12/` и загрузить их как artifacts.

---

## 4) Минимальные требования по харднингу

В рамках P12 нужно:

1. **Dockerfile:**

   * не использовать `FROM ...:latest` (фиксированный тег/версия);
   * по возможности запускать процесс **не от root**;
   * вынести конфигурацию/секреты во внешние переменные/volume, а не хардкодить их в образ.

2. **IaC:**

   * описать базовые ресурсы для запуска вашего сервиса (deployment + service для K8s, или docker-compose-сервис, или Terraform-конфигурацию);
   * не жёстко открывать всё наружу (избегать `0.0.0.0/0` без необходимости, `hostNetwork: true`, и т.п.).

3. **Trivy:**

   * хотя бы один отчёт по образу;
   * кратко посмотреть на список уязвимостей и зафиксировать 1–2 вывода (в описании PR).

---

## 5) Запуск workflow и проверка артефактов

1. Зафиксируйте изменения:

```bash
git add .github/workflows/ci-p12-iac-container.yml security/ EVIDENCE/P12 iac/ k8s/ deploy/ || true
git commit -m "P12: add IaC & container security checks"
git push -u origin p12-iac-container
```

2. Откройте PR `p12-iac-container → main`.

3. Во вкладке **Actions** найдите workflow `Security - IaC & Container (P12)` (или как вы его назвали) и запустите:

* по кнопке `Run workflow`,
* либо через новый `push` (если оставили триггер на пути `Dockerfile`, `iac/**`, `k8s/**` и т.п.).

4. После успешного запуска проверьте:

* в Actions скачайте артефакт (например, `P12_EVIDENCE`);
* убедитесь, что внутри есть:

```text
hadolint_report.json
checkov_report.json
trivy_report.json
```

* при необходимости положите их в репозиторий:

```bash
cp <скачанный_каталог>/*.json EVIDENCE/P12/
git add EVIDENCE/P12/*.json
git commit -m "P12: add IaC/container security reports"
git push
```

---

## 6) Что написать в PR

Мини-шаблон:

```text
P12 - IaC & Container Security

Dockerfile: проверен hadolint (EVIDENCE/P12/hadolint_report.json)
IaC: проверен checkov по каталогу iac/ (EVIDENCE/P12/checkov_report.json)
Image: проверен trivy по образу <имя:тег> (EVIDENCE/P12/trivy_report.json)

Харднинг:
- FROM: заменён latest → <конкретная версия>
- Пользователь: добавлен non-root user для запуска процесса
- IaC: <например, ограничен ingress, убраны лишние capabilities и т.п.>

Дальнейшие шаги:
- [ ] исправить критичные/высокие findings
- [ ] доработать IaC по результатам отчёта
```

---

## 7) Как использовать `secdev-seed-s09-s12` как пример

Если хотите посмотреть живой пример:

* откройте в `secdev-seed-s09-s12`:

  * `.github/workflows/ci-s12-iac-container.yml`,
  * `security/hadolint.yaml`,
  * `security/checkov.yaml`,
  * `security/trivy.yaml`,
  * структуру `EVIDENCE/S12/`.

Ориентируйтесь на эту структуру, но **сдавать P12 нужно из вашего курсового репозитория**.
