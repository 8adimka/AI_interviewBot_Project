# 📚 Telegram Bot for Technical Interviews

### Conduct structured technical interviews with AI and voice input

## 📦 Stack:
Python, Django, SQLAlchemy, PostgreSQL, Docker,
OpenAI API, Telegram API, Speech Recognition
---
### 🔍 Project Overview:

This is a Django-based Telegram bot designed to conduct structured technical interviews with candidates.
It supports voice input, uses OpenAI GPT for generating questions and analyzing answers, and stores the interview flow in PostgreSQL.

### 🧠 Features:
- 🗣 Voice message processing with speech recognition
- 🤖 AI-powered question generation and answer evaluation
- 🧩 Modular service-based architecture
- 🗄 Data stored in PostgreSQL database
- 🐳 Dockerized for easy deployment and scaling

---
### 📁 Project Structure:

```interview_bot/
├── .env                      # Environment variables
├── bot/                      # Django app
│   ├── controllers/          # Handlers for bot commands
│   ├── services/             # Business logic layer (DTOs, OpenAI clients)
│   ├── dao/                  # Data Access Layer (DAOs, repositories)
│   ├── models/               # Django ORM models
│   ├── management/commands/  # Custom management commands
│   ├── telegram_config.py    # Telegram bot configuration
│   ├── config.py             # App-level config
├── interview_bot/            # Django project
│   ├── settings.py           # Django settings
├── manage.py                 # Management script
├── Dockerfile                # Docker image definition
└── docker-compose.yaml       # Multi-container setup
```

---
### 🔧 Setup & Run (Docker):

1. Prerequisites:

    - Docker & Docker Compose installed
    - Telegram Bot Token from @BotFather
    - OpenAI API key

2. Create .env file:
```
### Database
DB_NAME=interview_db
DB_USER=v
DB_PASSWORD=1111
DB_HOST=db
DB_PORT=5432

### Telegram
TELEGRAM_BOT_TOKEN=your_token_here

### OpenAI
OPENAI_API_KEY=your_openai_key_here
```

3. Start services
    - docker-compose up -d --build

4. Initialize DB
    - docker-compose exec bot python manage.py migrate
    - docker-compose exec bot python manage.py createsuperuser  # optional

5. Logs & Maintenance
    - docker-compose logs -f bot
    - docker-compose down           # Stop
    - docker-compose down -v       # Stop & remove volumes


### ⚙️ Dependencies
requirements.txt

  • Django 5.1.7 
  • SQLAlchemy 2.0.39

  • Alembic 
  • python-telegram-bot 21.11.1

  • OpenAI SDK 1.66.2 
  • psycopg2-binary

  • Speech Recognition (via external lib) 
  • httpx, dotenv, tqdm, etc.

### 🚀 Production Notes
  *Redis can be added for caching if needed to scale the project.

---

# 🇷🇺 Телеграм-бот для проведения технических интервью

## Описание проекта:
Бот на Django для проведения технических интервью. Генерирует вопросы с помощью OpenAI GPT, оценивает ответы и сохраняет всё в базу данных PostgreSQL.
Поддерживает голосовые сообщения и Docker-развёртывание.

### 📦 Стек технологий
Python, Django, SQLAlchemy, PostgreSQL
Docker, OpenAI API, Telegram API, Speech Recognition

### 🔑 Основной функционал:

- 🗣 Распознавание голосовых сообщений
- 🤖 Генерация вопросов и оценка ответов с помощью GPT
- 🗄 Сохранение истории интервью
- 🐳 Docker для изоляции и масштабируемости

### 🚀 Запуск в Docker:
Запуск в Docker:
1. Подготовка
  - Убедитесь, что у вас установлен Docker и Docker Compose.
  - Создайте файл .env в корне проекта и укажите переменные окружения, например:
```
DB_HOST=db
DB_PORT=5432
DB_NAME=interview_db
DB_USER=v
DB_PASSWORD=1111
TELEGRAM_BOT_TOKEN=your_token_here
OPENAI_API_KEY=your_openai_key_here
```

2. Сборка и запуск контейнеров -> Выполните команду:
    - docker-compose up --build -d  
• Флаг --build пересоберет контейнеры при изменениях.
    • Флаг -d запустит контейнеры в фоновом режиме.

3. Проверка состояния контейнеров:
    - docker ps  
Вы должны увидеть два работающих контейнера: bot и db.

4. Выполнение миграций:  
  После первого запуска выполните миграции базы данных:
    - docker-compose exec bot python manage.py migrate  
  При необходимости создайте суперпользователя Django:  
    - docker-compose exec bot python manage.py createsuperuser  

5. Логирование контейнера:  
Посмотреть логи работающего бота:
    - docker-compose logs -f bot

6. Остановка контейнеров:  
    - docker-compose down

Где хранятся данные PostgreSQL?  
В файле docker-compose.yaml определен именованный том для базы данных:
```
volumes:
  postgres_data:
```
Docker будет хранить данные PostgreSQL в /var/lib/docker/volumes/postgres_data/_data.  
Если нужно полностью очистить базу данных:
  - docker volume rm interview_bot_postgres_data  

После запуска бот будет доступен в Telegram, а база данных будет работать в контейнере PostgreSQL.


📬 Vadim Medintsev
📧 Email: m8adimka@gmail.com
🌍 LinkedIn [linkedin.com/in/vadim-medintsev/](https://www.linkedin.com/in/vadim-medintsev/)
