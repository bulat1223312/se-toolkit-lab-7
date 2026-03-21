#!/usr/bin/env python3
import sys
import argparse
from telegram.ext import Application, CommandHandler
import config
from handlers import start, help, health, scores, labs

def run_test_mode(command: str):
    """Симулирует команду Telegram, вызывая обработчик напрямую."""
    command = command.lstrip("/")
    if command == "start":
        print(start())
    elif command == "help":
        print(help())
    elif command == "health":
        print(health())
    elif command.startswith("scores"):
        parts = command.split()
        lab_id = parts[1] if len(parts) > 1 else None
        print(scores(lab_id))
    elif command == "labs":
        print(labs())
    else:
        print("Неизвестная команда")

def run_bot():
    """Запускает Telegram-бота."""
    if not config.BOT_TOKEN:
        print("BOT_TOKEN не задан в .env.bot.secret", file=sys.stderr)
        sys.exit(1)

    app = Application.builder().token(config.BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", lambda u, c: u.message.reply_text(start())))
    app.add_handler(CommandHandler("help", lambda u, c: u.message.reply_text(help())))
    app.add_handler(CommandHandler("health", lambda u, c: u.message.reply_text(health())))
    app.add_handler(CommandHandler("scores", lambda u, c: u.message.reply_text(scores(c.args[0] if c.args else None))))
    app.add_handler(CommandHandler("labs", lambda u, c: u.message.reply_text(labs())))
    app.run_polling()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", help="Запустить в тестовом режиме с командой", nargs="?", const="start")
    args = parser.parse_args()
    if args.test is not None:
        run_test_mode(args.test)
    else:
        run_bot()