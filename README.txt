Telegram Bot for Technical Interviews
Project Overview

This is a Django-based Telegram bot designed to conduct technical interviews.
The bot supports:
    • Voice message processing
    • Interaction with OpenAI GPT for question generation and answer evaluation
    • Structured interview workflows
    • Database PostgreSQL storage of questions and answers

Project Structure:
interview_bot/
├── .env                        # Environment variables
├── .gitignore
├── bot/                        # Main application (Django app)
│   ├── management/             # Custom management commands
│   │   ├── commands/
│   │   │   ├── add_initial_data.py
│   │   │   ├── add_prompts.py  # Command to add prompts
│   ├── controllers/            # Bot command handlers
│   │   ├── command.py
│   │   ├── start_handler.py
│   │   ├── voice_handler.py    # Voice message handler
│   ├── services/               # Business logic layer
│   │   ├── dto/                # Data Transfer Objects
│   │   ├── gpt_client.py
│   │   ├── openai_client.py    # OpenAI API client
│   ├── dao/                    # Data Access Layer
│   │   ├── answer_dao.py
│   │   ├── question_dao.py
│   ├── models/                 # Database models
│   │   ├── question.py
│   │   ├── answer.py
│   ├── config.py               # Bot configuration
├── interview_bot/              # Django project
│   ├── settings.py             # Django settings
├── manage.py                   # Django management
├── Dockerfile                  # Container configuration
└── docker-compose.yaml         # Multi-container setup

Prerequisites
    1. Docker and Docker Compose installed
    2. Telegram Bot Token from @BotFather
    3. OpenAI API key (if using GPT features)

Setup and Running with Docker
1. Configuration
Create .env file in project root:
ini
# Database
DB_NAME=interview_db
DB_USER=v
DB_PASSWORD=1111
DB_HOST=db
DB_PORT=5432

# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_WEBHOOK_URL=https://yourdomain.com

# OpenAI
OPENAI_API_KEY=your_openai_key
2. Build and Run Containers

# Start services
docker-compose up -d --build

# View logs
docker-compose logs -f bot

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v

3. Initialize Database
# Apply migrations
docker-compose exec bot python manage.py migrate

# Create superuser (optional)
docker-compose exec bot python manage.py createsuperuser

# Load initial data
docker-compose exec bot python manage.py add_initial_data

4. Access Services
    • PostgreSQL: localhost:5432
        ◦ User: v
        ◦ Password: 1111
        ◦ Database: interview_db
    • Django Admin (if configured): http://localhost:8000/admin

Management Commands
# Add new prompts
docker-compose exec bot python manage.py add_prompts

# Run tests
docker-compose exec bot python manage.py test
Database Backup
To backup PostgreSQL data:
docker-compose exec db pg_dump -U v interview_db > backup.sql

To restore:
cat backup.sql | docker-compose exec -T db psql -U v interview_db
Troubleshooting
    1. Database not ready:
        ◦ Wait for healthcheck to complete (usually <30s)
        ◦ Check logs: docker-compose logs db
    2. Bot not responding:
        ◦ Verify Telegram token in .env
        ◦ Check webhook configuration
    3. Migration issues:
       docker-compose exec bot python manage.py makemigrations
       docker-compose exec bot python manage.py migrate

Production Notes
For production deployment:
    1. Set DEBUG=False in Django settings
    2. Configure proper SSL for webhooks
    3. Use PostgreSQL backups
    4. Consider adding Redis for caching

Далее на русском.
Описание проекта.
Этот проект представляет собой Telegram-бота для проведения технических интервью.
Бот использует OpenAI для генерации вопросов, на основе заготовленных промптов, анализа ответов и персонализированной обратной связи.
Реализована поддержка голосовых сообщений с функцией распознавания речи.
Использовал Docker-compose для удобства масштабирования и поддержки.
Данные сохраняются в базе данных PostgreSQL. 

Бот поддерживает:
• Обработку голосовых сообщений
• Взаимодействие с OpenAI GPT для генерации вопросов и оценки ответов
• Структурированные рабочие процессы интервью
• Хранение вопросов и ответов в базе данных PostgreSQL

Структура проекта:
interview_bot/
 ├── .env                        # Файл с переменными окружения
 ├── .gitignore
 ├── bot/                        # Основное приложение (Django app)
 │   ├── management/             # Кастомные команды управления
 │   │   ├── __init__.py
 │   │   ├── commands/
 │   │   │   ├── __init__.py
 │   │   │   ├── add_initial_data.py
 │   │   │   ├── add_prompts.py  # Команда для добавления промптов
 │   ├── controllers/            # Обработчики команд бота
 │   │   ├── __init__.py
 │   │   ├── command.py
 │   │   ├── start_handler.py    # Обработчик команды /start
 │   │   ├── voice_handler.py    # Обработчик голосовых сообщений
 │   ├── services/               # Сервисный слой (бизнес-логика)
 │   │   ├──dto/                    # Data Transfer Objects (DTO)
 │   │   │   ├── __init__.py
 │   │   │   ├── gpt_request.py      # DTO для запроса к GPT
 │   │   │   ├── gpt_response.py     # DTO для ответа от GPT
 │   │   │   ├── question.py         # DTO для вопроса
 │   │   │   ├── transcription.py    # DTO для транскрипции
 │   │   ├── __init__.py
 │   │   ├── gpt_client.py
 │   │   ├── openai_client.py    # Клиент для работы с OpenAI API
 │   │   ├── question_service.py # Сервис для работы с вопросами
 │   ├── dao/                    # Data Access Object (доступ к данным)
 │   │   ├── __init__.py
 │   │   ├── answer_dao.py
 │   │   ├── question_dao.py
 │   │   ├── interview_repository.py  # Репозиторий для вопросов и ответов
 │   │   ├── topic_repository.py      # Репозиторий для тем собеседования
 │   │   ├── prompt_dao.py            # DAO для работы с текстовыми шаблонами
 │   ├── models/                 # Модели базы данных
 │   │   ├── __init__.py
 │   │   ├── question.py         # Модель для вопросов
 │   │   ├── answer.py           # Модель для ответов
 │   │   ├── prompt.py           # Модель для текстовых шаблонов
 │   ├── views.py                # Django views (если понадобятся)
 │   ├── urls.py                 # Django URLs (если понадобятся)
 │   ├── telegram_config.py      # Конфигурация Telegram бота
 │   ├── database.py
 │   ├── config.py
 ├── interview_bot/              # Основной проект Django
 │   ├── settings.py             # Настройки Django
 │   ├── urls.py                 # Основные URLs проекта
 │   ├── wsgi.py                 # WSGI-приложение
 ├── manage.py                   # Управление Django-проектом

Запуск в Docker:
1. Подготовка
Убедитесь, что у вас установлен Docker и Docker Compose.
Создайте файл .env в корне проекта и укажите переменные окружения, например:
DB_HOST=db
DB_PORT=5432
DB_NAME=interview_db
DB_USER=v
DB_PASSWORD=1111
TELEGRAM_BOT_TOKEN=your_token_here
OPENAI_API_KEY=your_openai_key_here

2. Сборка и запуск контейнеров
Выполните команду:
docker-compose up --build -d
    • Флаг --build пересоберет контейнеры при изменениях.
    • Флаг -d запустит контейнеры в фоновом режиме.

3. Проверка состояния контейнеров
docker ps
Вы должны увидеть два работающих контейнера: bot и db.

4. Выполнение миграций
После первого запуска выполните миграции базы данных:
docker-compose exec bot python manage.py migrate
При необходимости создайте суперпользователя Django:
docker-compose exec bot python manage.py createsuperuser

5. Логирование контейнера
Посмотреть логи работающего бота:
docker-compose logs -f bot

6. Остановка контейнеров
docker-compose down

Где хранятся данные PostgreSQL?
В файле docker-compose.yaml определен именованный том для базы данных:
volumes:
  postgres_data:
Docker будет хранить данные PostgreSQL в /var/lib/docker/volumes/postgres_data/_data.
Если нужно полностью очистить базу данных:
docker volume rm interview_bot_postgres_data

После запуска бот будет доступен в Telegram, а база данных будет работать в контейнере PostgreSQL.


