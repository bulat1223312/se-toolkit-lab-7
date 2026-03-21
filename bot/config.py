import os
from dotenv import load_dotenv

load_dotenv(".env.bot.secret")  # на виртуальной машине будет лежать секретный файл

BOT_TOKEN = os.getenv("BOT_TOKEN")
LMS_API_BASE_URL = os.getenv("LMS_API_BASE_URL")
LMS_API_KEY = os.getenv("LMS_API_KEY")
LLM_API_KEY = os.getenv("LLM_API_KEY")