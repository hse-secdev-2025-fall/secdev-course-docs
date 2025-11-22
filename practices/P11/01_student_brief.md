# Инструкция для студента (P11 — DAST с OWASP ZAP baseline)

## 1) Ветка и подготовка

1. Перейдите на актуальный `main` и создайте ветку под практику:

```bash
git switch main
git pull
git switch -c p11-dast-zap
```

2. Убедитесь, что:

   * ваш сервис можно поднять локально/в CI (например, через `uvicorn` или `docker compose`);
   * есть простой health-эндпойнт (например, `/healthz`), который возвращает 200.

---

## 2) Целевой HTTP-сервис для DAST

Для P11 ZAP baseline должен сканировать **ваш курсовой сервис**, а не демо из seed.

Минимальные требования:

- сервис поднимается на GitHub-раннере (Linux) одной командой;
- health-чек в CI может дождаться его готовности;
- сервис доступен по `http://localhost:<PORT>/`.

Пример для FastAPI (адаптируйте под свой код):

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080
# healthz:
curl -sf http://localhost:8080/healthz
```

Если у вас другой фреймворк/порт — поменяйте:

- модуль `app.main:app` на свой;
- порт `8080` на свой;
- путь `/healthz` на тот, что реально есть.

---

## 3) Добавляем workflow `ci-p11-dast.yml`

1. Возьмите шаблон из `secdev-course-docs`:

   * `practices/P11/06_templates/.github/workflows/ci-p11-dast.yml`

2. Скопируйте его в свой курсовой репозиторий:

```text
.github/workflows/ci-p11-dast.yml
```

3. Внутри файла обязательно проверьте и при необходимости исправьте:

* шаг запуска приложения (`Run app`):

  * команду (`uvicorn app.main:app ...` → под ваш сервис),
  * порт (`8080` → ваш порт),
  * URL health-чека (`http://localhost:8080/healthz` → ваш);
* аргументы ZAP baseline:

  * флаг `-t http://localhost:8080` → ваш целевой URL.

4. Подготовьте каталог под артефакты (если его ещё нет):

```bash
mkdir -p EVIDENCE/P11
```

---

## 4) Запуск workflow в Actions и проверка артефактов

1. Закоммитьте изменения:

```bash
git add .github/workflows/ci-p11-dast.yml EVIDENCE/P11 || true
git commit -m "P11: add DAST (ZAP baseline) workflow"
git push -u origin p11-dast-zap
```

2. Откройте PR `p11-dast-zap → main`.

3. Перейдите во вкладку **Actions** и запустите workflow:

* либо по кнопке `Run workflow` (если настроен только `workflow_dispatch`);
* либо сработает автоматический запуск по `push` (если вы оставили триггер на пути `app/**`, `src/**` и т.д.).

4. Дождитесь завершения job:

* зелёный статус говорит о том, что:

  * сервис поднялся,
  * ZAP baseline отработал,
  * артефакты успешно сохранены.

5. После успешного запуска проверьте:

* в Actions скачайте артефакт `P11_EVIDENCE` (или другое имя, указанное в workflow);
* убедитесь, что внутри есть:

```text
zap_baseline.html
zap_baseline.json
```

* при необходимости добавьте эти файлы в репозиторий:

```bash
cp <скачанный_каталог>/zap_baseline.* EVIDENCE/P11/
git add EVIDENCE/P11/zap_baseline.*
git commit -m "P11: add ZAP baseline reports"
git push
```

---

## 5) Что написать в PR

В описании PR `p11-dast-zap → main` добавьте короткое резюме:

```text
P11 - DAST (ZAP baseline)

Target: http://localhost:8080/
Reports: EVIDENCE/P11/zap_baseline.html, zap_baseline.json
Result: N alerts (High=X, Medium=Y, Low=Z).

План действий:
- [ ] исправить / перепроверить <если есть реальные проблемы>
- [ ] задокументировать принятый риск / ложное срабатывание (если актуально)
```

Этого достаточно для базового уровня.

---

## 6) Как использовать `secdev-seed-s09-s12` как пример (не как место сдачи)

Если нужно подсмотреть живой пример:

* откройте `secdev-seed-s09-s12/.github/workflows/ci-s11-dast.yml`;
* посмотрите, как там:

  * запускается учебный FastAPI-сервис,
  * вызывается `owasp/zap2docker-stable` с `zap-baseline.py`,
  * сохраняются отчёты в `EVIDENCE/S11/`.

Можно ориентироваться на этот пример, но **сдавать практику P11 нужно из своего курсового репозитория**.
