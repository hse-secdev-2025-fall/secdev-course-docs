# Анонс для Classroom/LMS — P11

**Тема:** DAST (OWASP ZAP baseline) для курсового сервиса  
**Что сдаём:** PR `p11-dast-zap → main` + workflow `.github/workflows/ci-p11-dast.yml`, отчёты ZAP в `EVIDENCE/P11/zap_baseline.html` и `EVIDENCE/P11/zap_baseline.json`  
**Баллы:** см. чек-лист P11  
**Дедлайн:** укажет преподаватель

Кратко: переносим идею семинара S11 (DAST через ZAP baseline) в основной курсовой репозиторий.  
Сервис поднимаем на GitHub-раннере, ZAP baseline сканирует `http://localhost:<PORT>/`, отчёты сохраняются в `EVIDENCE/P11/`.
