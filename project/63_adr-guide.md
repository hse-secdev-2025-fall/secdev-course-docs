# Руководство по ADR (Architecture Decision Record)

## Когда писать ADR
- Вводим/меняем фреймворк, БД, схему аутентификации.
- Меняем контракты API/версионирование.
- Вносим существенные ограничения/риски.

## Жизненный цикл
- `proposed` → `accepted` → `deprecated` → `superseded by ADR-XX`.

## Структура и нейминг
- `docs/adr/ADR-0001-short-title.md` (инкрементный номер).
- Короткое и информативное название; дата в шапке.

## Ссылки и контекст
- Привязывайте ADR к Issue/PR; помечайте теги релизов `PXX`.

## Пример (укороченный)
```md
# ADR-0003: Токены доступа - JWT (HS256)
Status: accepted
Date: 2025-09-01

Context: требуется stateless масштабирование, простая интеграция.
Decision: JSON Web Token (HS256) с коротким TTL + refresh.
Consequences: просто масштабировать, но важно ревокировать refresh при утечке.
Alternatives: session-based, opaque tokens.
Links: #42, PR #57
```
