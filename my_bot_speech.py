# Импортируем необходимые компоненты из библиотеки
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Токен вашего бота от @BotFather
BOT_TOKEN = "5435821594:AAGa7Cg-Vw4JAL4-ztTcJMfQpoA-8yLoyZg"


# Функция для команды /start
def start(update: Update, context: CallbackContext) -> None:
    """
    Обрабатывает команду /start
    Вызывается когда пользователь пишет /start боту
    """
    # update.message.reply_text() отправляет сообщение обратно в тот же чат
    update.message.reply_text(
        "Привет! Я эхобот. Напиши что-нибудь, и я повторю это!"
    )


# Функция для команды /help
def help_command(update: Update, context: CallbackContext) -> None:
    """Обрабатывает команду /help"""
    update.message.reply_text(
        "Просто напиши любое сообщение, и я его повторю!\n"
        "Команды:\n"
        "/start - начать общение\n"
        "/help - показать эту справку"
    )


# Основная функция эхо - обрабатывает текстовые сообщения
def echo(update: Update, context: CallbackContext):
    """
    Обрабатывает ЛЮБЫЕ текстовые сообщения от пользователя
    и отправляет их обратно (эхо)
    """
    # update.message.text содержит текст сообщения от пользователя
    user_message = update.message.text

    # Отправляем сообщение обратно пользователю
    update.message.reply_text(f"Ты сказал: {user_message}")


# Функция для обработки ошибок
def error(update: Update, context: CallbackContext) -> None:
    """Логирует ошибки"""
    print(f"Произошла ошибка: {context.error}")


# Главная функция, которая запускает бота
def main() -> None:
    """
    Основная функция, где:
    - Создается экземпляр бота
    - Настраиваются обработчики команд и сообщений
    - Запускается бесконечный цикл опроса серверов Telegram
    """

    # Создаем Updater - объект, который получает обновления от Telegram
    updater = Updater(BOT_TOKEN)

    # Получаем Dispatcher для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Регистрируем обработчики команд:
    # CommandHandler("command_name", function) - обрабатывает команды
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # Регистрируем обработчик текстовых сообщений:
    # MessageHandler(Filters.text, function) - обрабатывает ВСЕ текстовые сообщения
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Регистрируем обработчик ошибок
    dispatcher.add_error_handler(error)

    # Запускаем бота в режиме опроса (polling)
    print("Бот запущен...")
    updater.start_polling()

    # Бот работает до принудительной остановки (Ctrl+C)
    updater.idle()


# Точка входа в программу
if __name__ == "__main__":
    main()