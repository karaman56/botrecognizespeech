# 🤖 AI Bots with DialogFlow Integration


Два интеллектуальных бота для Telegram и VK с интеграцией Google DialogFlow для обработки естественного языка (NLP). Боты могут отвечать на вопросы пользователей на разных языках и отправлять уведомления об ошибках в Telegram.

## 🌟 Особенности

- **🤖 Два бота в одном проекте**: Telegram и VK
- **🧠 Искусственный интеллект**: интеграция с Google DialogFlow
- **🌐 Мультиязычность**: поддержка русского и английского языков
- **🚨 Мониторинг ошибок**: автоматическая отправка ошибок в Telegram
- **⚡ Автозапуск**: настройка через Supervisor для работы 24/7
- **🔐 Безопасность**: все ключи хранятся в `.env` файле

## 📁 Структура проекта

botrecognizespeech/
├── telegram_dialogflow_bot.py # Telegram бот с DialogFlow
├── vk_dialogflow_bot.py # VK бот с DialogFlow
├── .env.example # Шаблон конфигурации
├── requirements.txt # Зависимости Python
├── README.md # Эта документация
└── .gitignore # Игнорируемые файлы

## 🚀 Быстрый старт

### Предварительные требования

- Python 3.8 или выше
- Аккаунты:
  - [Telegram Bot Token](https://core.telegram.org/bots#6-botfather)
  - [VK Group Token](https://vk.com/dev/bots)
  - [Google Cloud Project](https://cloud.google.com/dialogflow/docs/quick/setup)

### Установка

1. **Клонируйте репозиторий**
   ```bash
   git clone https://github.com/karaman56/botrecognizespeech.git
   cd botrecognizespeech
   ```
2. **Создайте виртуальное окружение**
    ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # или
   venv\Scripts\activate     # Windows
    ```
3. ***Установите зависимости***
    ```bash
   pip install -r requirements.txt
   ```
4. ***Настройте конфигурацию***
    ```bash
   cp .env.example .env
   # Отредактируйте .env файл, добавив свои ключи
   ```
5. ***Создайте файл .env со следующими переменными:***
    ```
    # Telegram Bot
    BOT_TOKEN=your_telegram_bot_token_here

    # VK Bot
    VK_TOKEN=your_vk_bot_token_here

    # Google DialogFlow
    DIALOGFLOW_PROJECT_ID=your_dialogflow_project_id
    GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json

    # Error Reporting Bot
    BOT_TOKEN_TG=your_error_reporting_bot_token
    CHAT_ID=your_telegram_chat_id
    ```
### Получение [Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts)
1. Создайте проект в Google Cloud Console
2. Включите DialogFlow API
3. Создайте сервисный аккаунт и скачайте JSON ключ
4. Положите файл в папку проекта как credentials.json

### Запуск ботов локально
Telegram бот:
```bash
python telegram_dialogflow_bot.py
```

VK бот:

```bash
python vk_dialogflow_bot.py
```

### 🎯 Функциональность
Telegram Bot
Команда /start - приветственное сообщение
Команда /help - справка по командам
Обработка текстовых сообщений
Интеграция с DialogFlow для AI-ответов
Отправка ошибок в мониторинговый Telegram бот
VK Bot
Команды /start, начать - приветственное сообщение
Команды /help, помощь - справка по командам
Обработка текстовых сообщений на русском языке
Интеграция с DialogFlow для AI-ответов
Фильтрация fallback-интентов (не отвечает на непонятные вопросы)
Отправка ошибок в мониторинговый Telegram бот

### Деплой на сервер
- Настройка Supervisor (для Linux серверов)
- Установите Supervisor

```bash
    sudo apt-get install supervisor
```

#### Для Telegram бота:

```bash
sudo nano /etc/supervisor/conf.d/telegram-bot.conf
ini
[program:telegram-bot]
command=/path/to/venv/bin/python3 /path/to/telegram_dialogflow_bot.py
directory=/path/to/project
autostart=true
autorestart=true
stderr_logfile=/var/log/telegram-bot.err.log
stdout_logfile=/var/log/telegram-bot.out.log
```

#### Для VK бота:

```bash
sudo nano /etc/supervisor/conf.d/vk-bot.conf
ini
[program:vk-bot]
command=/path/to/venv/bin/python3 /path/to/vk_dialogflow_bot.py
directory=/path/to/project
autostart=true
autorestart=true
stderr_logfile=/var/log/vk-bot.err.log
stdout_logfile=/var/log/vk-bot.out.log
```

#### Запустите ботов

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start telegram-bot
sudo supervisorctl start vk-bot
```

#### 🔧 Технические детали

- Зависимости
`python-telegram-bot` - для работы с Telegram API
`vk-api - для работы с VK API`
`google-cloud-dialogflow` - для интеграции с DialogFlow
`python-dotenv` - для управления переменными окружения
`requests` - для HTTP запросов

#### Мониторинг ошибок
- Система отправляет уведомления в Telegram при:
- Ошибках DialogFlow API
- Ошибках отправки сообщений
- Критических ошибках запуска ботов
- Успешном запуске ботов
- Логирование
#### Боты записывают логи в:
- Консоль (при локальном запуске)
- Файлы логов (при работе через Supervisor)
- Telegram (критические ошибки)

#### 🐛 Устранение неполадок
- Распространенные проблемы
- "DialogFlow error: 7 PERMISSION_DENIED"
- Проверьте GOOGLE_APPLICATION_CREDENTIALS
- Убедитесь что DialogFlow API включен
- "Telegram bot error: Conflict"
- Убедитесь что запущен только один экземпляр бота
- "VK token invalid"
- Обновите токен VK группы
- Проверьте права доступа

#### Просмотр логов
```bash
# Telegram бот
tail -f /var/log/telegram-bot.out.log
```

#### VK 
```tail -f /var/log/vk-bot.out.log```


- [telegram_dialogflow_bot.py](https://t.me/First_napominalka_bot)
- [vk_dialogflow_bot.py](https://vk.com/club234091612)
- [Бот куда приходят ошибки](https://t.me/shet5683_bot)

## спасибо за внимание!
