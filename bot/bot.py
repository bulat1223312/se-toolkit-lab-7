#!/usr/bin/env python3
import sys
import argparse
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import config
from handlers import start, help, health, labs, scores
from handlers.natural import route as natural_route

def run_test_mode(command: str):
    if command.startswith('/'):
        command = command[1:]

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
        response = natural_route(command)
        print(response)

def run_bot():
    if not config.BOT_TOKEN:
        print("BOT_TOKEN not set in .env.bot.secret", file=sys.stderr)
        sys.exit(1)

    app = Application.builder().token(config.BOT_TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("help", help_handler))
    app.add_handler(CommandHandler("health", health_handler))
    app.add_handler(CommandHandler("labs", labs_handler))
    app.add_handler(CommandHandler("scores", scores_handler))

    # Message handler for plain text
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    # Callback for inline buttons
    app.add_handler(CallbackQueryHandler(button_callback))

    app.run_polling()

# --- Telegram handlers ---

async def start_handler(update, context):
    keyboard = [
        [InlineKeyboardButton("Labs", callback_data="labs"),
         InlineKeyboardButton("Scores", callback_data="scores")],
        [InlineKeyboardButton("Top learners", callback_data="top"),
         InlineKeyboardButton("Completion", callback_data="completion")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(start(), reply_markup=reply_markup)

async def help_handler(update, context):
    await update.message.reply_text(help())

async def health_handler(update, context):
    await update.message.reply_text(health())

async def labs_handler(update, context):
    await update.message.reply_text(labs())

async def scores_handler(update, context):
    args = context.args
    lab_id = args[0] if args else None
    await update.message.reply_text(scores(lab_id))

async def message_handler(update, context):
    text = update.message.text
    if text.startswith('/'):
        return
    response = natural_route(text)
    await update.message.reply_text(response)

async def button_callback(update, context):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == "labs":
        reply = labs()
    elif data == "scores":
        reply = "Please specify a lab, e.g., /scores lab-04"
    elif data == "top":
        reply = "For which lab? Use /top_learners lab-04"
    elif data == "completion":
        reply = "For which lab? Use /completion lab-04"
    else:
        reply = "Unknown"
    await query.edit_message_text(reply)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", help="Run in test mode with a command", nargs="?", const="start")
    args = parser.parse_args()
    if args.test is not None:
        run_test_mode(args.test)
    else:
        run_bot()