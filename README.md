# 🏛️ University Database CLI Management Tool & Analytics Layer

Консольна утиліта та аналітичний інструмент для моделювання, міграції та адміністрування реляційної бази даних умовного навчального закладу. 

Проєкт демонструє еволюцію розробки: від низькорівневих аналітичних SQL-запитів до створення автоматизованої системи керування даними за допомогою ORM, міграцій та CLI-інтерфейсу.

---

## 📌 Про проєкт

Проєкт структурно розділений на два логічні модулі:

1. **Raw SQL Layer (`raw_sql_analytics/`):** Відповідає за дослідження реляційних зв'язків та написання SQL-запитів до бази даних **SQLite** за допомогою курсорів. Включає агрегації, об'єднання та фільтрації. Реалізовано можливість збереження результату в csv файл.
2. **ORM & CLI layer (`university_cli/`):** Включає архітектуру на базі **SQLAlchemy 2.0 ORM**, розгорнуту в контейнері **PostgreSQL** через **Docker**. Керування структурою БД реалізовано через міграції **Alembic**, а взаємодія з даними реалізована у вигляді повноцінної **CLI-програми** на базі модуля `argparse` для виконання CRUD-операцій.

---

## 🛠 Технологічний стек

| Категорія | Технології |
|---|---|
| Мова програмування | Python 3.13 |
| Бази даних | PostgreSQL, SQLite |
| ORM | SQLAlchemy 2.0 |
| Міграції | Alembic |
| Контейнеризація | Docker Compose |
| Інструменти тестування | Faker (генерація mock-даних) |
| Менеджер залежностей | Poetry |

---

## ✨ Функціонал

### Модуль 1: Чистий SQL (`raw_sql_analytics`)
- Створення структури зв'язків в базі даних за допомогою **ER-діаграми**.
- Генерація та наповнення бази SQLite випадковими даними за допомогою Faker (`seed_raw.py`).
- Реалізовано SQL-запити різного рівня складності (наприклад: пошук топ-5 студентів за середнім балом, середній бал у групах за предметом, курси конкретного викладача тощо).
- Додана можливість збереження результату SQL-запиту в csv файл.


### Модуль 2: ORM Система та CLI-утиліта (`university_cli`)
- Описано реляційну схему даних у вигляді Python-класів (моделі `Student`, `Group`, `Teacher`, `Discipline`, `Grade`).
- Реалізовано **CLI** утиліту для CRUD-операцій (Create, Read, Update, Delete) для будь-якої таблиці прямо через термінал.
- Генерація та наповнення бази PostgreSQL випадковими даними через сесії **SQLAlchemy**.
- Реалізовано аналогічні запити за допомогою **SQLAlchemy ORM**.

---

## 🗂 Структура проєкту

```
university-db-cli-tool/
│
├── raw_sql_analytics/             # Чистий SQL та SQLite
│   ├── sql_queries/               # Окремі файли SQL-запитів
│   ├── create_db.py               
│   ├── execute_query.py           # Скрипт для виконання запитів та збереження в CSV
│   ├── seed_raw.py                # Генерація даних через Faker
│   └── ER-diagram.png             # Схема зв'язків бази даних
│
├── university_cli/                # SQLAlchemy ORM & CLI
│   ├── alembic/                   
│   ├── db_config.py               
│   ├── models.py                  # Моделі SQLAlchemy 2.0 
│   ├── my_select.py               # Запити через SQLAlchemy ORM
│   ├── seed_orm.py                # Наповнення PostgreSQL через сесії ORM
│   ├── .env.example
│   ├── docker-compose.yml
│   └── CRUD_helper.py             # CLI утиліта 
│
└── pyproject.toml                 
```

---

## 🚀 Як запустити

### 1. Клонуй репозиторій
```bash
git clone https://github.com/Khrystyna979/university-db-cli-tool.git
cd university-db-cli-tool
```

### 2. Встанови залежності через Poetry:
```bash
pip install poetry
poetry install
```

### Запуск Частини SQLAlchemy ORM + PostgreSQL

- Перейди в папку модуля university_cli:
```bash
cd university_cli
```
- Створи `.env` файл
```bash
cp .env.example .env
```
Заповни значення у `.env` (дивись `.env.example`)
- Запусти PostgreSQL через Docker
```bash
docker compose up -d
```
- Застосуй міграції Alembic для створення таблиць
```bash
poetry run alembic upgrade head
```
- Заповни базу даних фейковими даними через ORM-сесії
```bash
poetry run python seed_orm.py
```
- Використання консольної CLI-утиліти
Для перегляду всього списку доступних команд та аргументів запусти команду:
```bash
poetry run python CRUD_helper.py --help
```
- Приклади використання команд для адміністрування
Показати список усіх студентів:
```bash
poetry run python CRUD_helper.py --action list -m Student
```
Створити нового викладача:
```bash
poetry run python CRUD_helper.py --action create -m Teacher --name 'Khrystyna Oliinyk'
```
Оновити ім'я викладача за його ID
```bash
poetry run python CRUD_helper.py --action update -m Teacher --id 3 --name 'Andrew Bezos'
```
Видалити запис про групу
```bash
poetry run python CRUD_helper.py --action remove -m Group --id 1
```

### Запуск Частини (Чистий SQL + SQLite)
- Перейди в папку модуля
```bash
cd raw_sql_analytics
```
- Запусти скрипт створення бази й генерації даних
```bash
poetry run python seed_raw.py
```
- Для запуску та перевірки SQL-запитів використовуй
```bash
poetry run python execute_query.py
```

---

## 👩‍💻 Автор

**Oliinyk Khrystyna** — [GitHub](https://github.com/Khrystyna979) | [LinkedIn](https://www.linkedin.com/in/khrystyna-oliinyk-200110376)