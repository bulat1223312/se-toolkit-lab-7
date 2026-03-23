import os
from dotenv import load_dotenv

load_dotenv(".env.bot.secret")

BOT_TOKEN = os.getenv("BOT_TOKEN")
LMS_API_BASE_URL = os.getenv("LMS_API_BASE_URL")
LMS_API_KEY = os.getenv("LMS_API_KEY")
LLM_API_BASE_URL = os.getenv("LLM_API_BASE_URL")
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_API_MODEL = os.getenv("LLM_API_MODEL")