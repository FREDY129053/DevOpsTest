# Проект: Python + TortoiseORM + PostgreSQL

## 🛠️ Стек
- **FastAPI** — быстрый веб-фреймворк для Python
- **Tortoise** ORM — асинхронный ORM
- **PostgreSQL** — реляционная СУБД
- **Docker + Docker Compose** (версия проекта: Docker 28.3.1, build 38b7060)

---

## 1. Требования к окружению
- Docker ≥ 28.3.1 (build 38b7060)
- Docker Compose (в составе Docker-клиента или как отдельный инструмент)

---

## 2. 🚀 Быстрый старт

```bash
cp .env.example .env
docker compose up --build
```

## 3. Проверка здоровья
```
curl -s localhost:8080/health
```
(ожидается нормальный ответ: {"status":"work"})

## 4. Примеры запросов
### Добавить товар
```
curl -X 'POST' \
  'http://localhost:8080/api/v1/items/add' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "string",
  "price": 100
}'
```

### Получить статистику
```
curl -X 'GET' \
  'http://localhost:8080/api/v1/items/stats' \
  -H 'accept: application/json'
```
При пустой базе `price` возвращается как **0**.

## 5. Переменные окружения (можно адаптировать под свои)
Файл .env.example должен содержать:
```env
# Тип окружения (dev | prod). Можно не указывать и будет prod
ENV_TYPE=prod

# --- Сетевые настройки сервера ---
# SERVER_HOST — обычно 0.0.0.0 (все интерфейсы) или localhost (127.0.0.1) для локальной разработки
SERVER_HOST=0.0.0.0

# Порт для приложения
SERVER_PORT=8080

# --- PostgreSQL ---
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=main_db
POSTGRES_PORT=5432
POSTGRES_DB=test
```

## 6. Запуск тестов локально
Создать виртуальное окружение в `app` и запустить через Python или
```
cd app && uv run pytest
```
Каждый тест создаёт свою отдельную базу данных, поэтому можно не беспокоиться о конфликте данных — всё изолировано и безопасно.

## 7. Структура проекта
```bash
.
├── app
│   ├── Dockerfile
│   ├── main.py  # Файл запуска
│   ├── migrations # Миграции
│   │   └── models
│   │       └── 1_20250909183622_None.py
│   ├── pyproject.toml
│   ├── setup.cfg
│   ├── src
│   │   ├── api  # Сборка API
│   │   │   ├── middlewares  # Middlewares проекта
│   │   │   │   └── logging.py
│   │   │   └── routers  # Роутеры проекта
│   │   │       ├── __init__.py
│   │   │       └── item_router.py
│   │   ├── config  # Конфиг проекта(загрузка и валидация env переменных)
│   │   │   └── load_env.py
│   │   ├── db  # База данных
│   │   │   ├── config.py  # Конфиг БД для миграций
│   │   │   ├── __init__.py  # Инициализация БД
│   │   │   └── models  # Модели в БД(таблицы)
│   │   │       ├── __init__.py
│   │   │       └── items.py
│   │   ├── repository  # Репозитори для взаимодействия с БД
│   │   │   └── item.py
│   │   ├── schemas  # Схемы входов/ответов API
│   │   │   ├── item.py
│   │   │   └── msg.py
│   │   ├── server.py  # Сборка приложения
│   │   └── service  # Сервис
│   │       └── item.py
│   ├── tests  # Папка с тестами
│   │   ├── conftest.py
│   │   ├── __init__.py
│   │   ├── test_add.py
│   │   └── test_stats.py
│   └── uv.lock
├── docker-compose.yaml
└── README.md
```
