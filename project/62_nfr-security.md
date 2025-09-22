# Нефункциональные требования по безопасности (расширенная версия)

## Формат требований
| ID | Категория | Требование | Критерии приёмки | Проверка | Приоритет |
|----|-----------|------------|------------------|----------|-----------|
| SEC-VAL-01 | Validation | Валидация входа на всех внешних границах | Неверные входы → 400 + структурная ошибка | pytest: негативные кейсы | Must |
| SEC-AUTH-01 | AuthN/AuthZ | Доступ к ресурсам - только владельцу/роли | Запрет IDOR | pytest: доступ чужим id → 403 | Must |
| SEC-ERR-01 | Error Handling | Единый формат ошибок (код/сообщение/детали) | Нет «traceback в ответе» | pytest: фоллси | Must |
| SEC-LOG-01 | Logging | 1 запись/запрос с request_id | Демонстрация в P13 | Ручн.+авто | Should |
| SEC-SEC-01 | Secrets | Секреты вне репозитория | Скан без находок | pre-commit/CI | Must |

## Матрица трассируемости (пример)
| Требование | Тест(ы) | PR | Примечание |
|---|---|---|---|
| SEC-VAL-01 | `tests/test_items_validation.py::test_invalid_payload` | #12 | edge cases числовых полей |
| SEC-AUTH-01 | `tests/test_access.py::test_idor_forbidden` | #15 | роль admin допускается |

## Политика ошибок
- Не возвращать stack traces и внутренние детали.
- Карта ошибок: `VALIDATION_ERROR`, `NOT_FOUND`, `FORBIDDEN`, `UNAUTHORIZED`, `CONFLICT`, `INTERNAL_ERROR`.

## Минимальные заголовки безопасности (если публичный фронт)
- `Content-Security-Policy` (позже, при фронте), `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: no-referrer`.
