# DFD — Data Flow Diagram (шаблон)

## Диаграмма (Mermaid)
```mermaid
flowchart LR
  U[User/Client] -->|F1: HTTPS| BFF[Web/API]
  subgraph Edge[Trust Boundary: Edge]
    BFF --> SVC[Service]
  end
  subgraph Core[Trust Boundary: Core]
    SVC --> DB[(Database)]
  end
```

## Список потоков
| ID | Откуда → Куда | Канал/Протокол | Данные/PII | Комментарий |
|----|---------------|-----------------|------------|-------------|
| F1 | U → BFF       | HTTPS           | creds      |             |
| F2 | BFF → SVC     | mTLS            | session    |             |
| F3 | SVC → DB      | TCP             | PII        |             |
