import config
from services.lms_client import LmsClient

# Создаём клиент один раз при импорте
lms = LmsClient(config.LMS_API_BASE_URL, config.LMS_API_KEY)

def start() -> str:
    return "👋 Добро пожаловать в бот-помощник по лабораторным работам! Используйте /help для списка команд."

def help() -> str:
    return """📋 Доступные команды:
/start — приветствие
/help — эта справка
/health — статус бэкенда
/labs — список лабораторных
/scores <название_лабы> — оценки по задачам (например, /scores lab-04)"""

def health() -> str:
    try:
        items = lms.get_items()
        if items is None:
            return "⚠️ Не удалось получить данные от бэкенда. Проверьте, что он запущен."
        count = len(items)
        return f"✅ Бэкенд доступен. Загружено {count} элементов."
    except Exception as e:
        # Формируем понятное сообщение об ошибке
        error_msg = str(e).lower()
        if "connection refused" in error_msg:
            return f"❌ Ошибка подключения к бэкенду: {e}. Убедитесь, что бэкенд запущен на порту {config.LMS_API_BASE_URL}."
        elif "timeout" in error_msg:
            return f"❌ Таймаут подключения к бэкенду: {e}. Проверьте сеть."
        else:
            return f"❌ Ошибка при обращении к бэкенду: {e}"

def labs() -> str:
    try:
        items = lms.get_items()
        if not items:
            return "📭 Список лабораторных пуст. Возможно, данные ещё не синхронизированы."
        # Фильтруем только лабораторные работы (обычно type: 'lab' или есть поле tasks)
        labs_list = [item for item in items if item.get('type') == 'lab']
        if not labs_list:
            return "📭 Лабораторные работы не найдены."
        result = "📚 Доступные лабораторные работы:\n"
        for lab in labs_list:
            name = lab.get('name', lab.get('id', 'Без названия'))
            result += f"• {name}\n"
        return result
    except Exception as e:
        return f"❌ Ошибка при получении списка лабораторных: {e}"

def scores(lab_id: str = None) -> str:
    if not lab_id:
        return "ℹ️ Укажите ID лабораторной, например: /scores lab-04"
    try:
        rates = lms.get_pass_rates(lab_id)
        if rates is None or not rates:
            return f"📊 Нет данных об оценках для {lab_id}. Убедитесь, что лабораторная существует и данные синхронизированы."
        # rates — это словарь вида {"task_name": pass_rate_percent, ...}
        result = f"📈 Проходные баллы для {lab_id}:\n"
        for task, rate in rates.items():
            result += f"• {task}: {rate:.1f}%\n"
        return result
    except Exception as e:
        return f"❌ Ошибка при получении оценок для {lab_id}: {e}"