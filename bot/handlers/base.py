import config
from services.lms_client import LmsClient

# Создаём клиент один раз при старте
lms = LmsClient(config.LMS_API_BASE_URL, config.LMS_API_KEY)

def start() -> str:
    return "Welcome! Я бот-помощник по лабораторным работам. Используйте /help для списка команд."

def help() -> str:
    return """Доступные команды:
/start — приветствие
/help — эта справка
/health — статус бэкенда
/labs — список лабораторных
/scores <lab> — проходные баллы по задачам (например, /scores lab-04)"""

def health() -> str:
    try:
        items = lms.get_items()
        count = len(items)
        return f"Backend is healthy. {count} items available."
    except Exception as e:
        return f"Backend error: {e}"

def labs() -> str:
    try:
        labs_list = lms.get_labs()
        if not labs_list:
            return "No labs found."
        result = "Available labs:\n"
        for lab in labs_list:
            # Ожидаем, что поле name содержит название, например "Lab 01 — Products, Architecture & Roles"
            name = lab.get('name', lab.get('id', 'Unnamed'))
            result += f"- {name}\n"
        return result
    except Exception as e:
        return f"Error fetching labs: {e}"

def scores(lab_id: str = None) -> str:
    if not lab_id:
        return "Please specify a lab ID, e.g., /scores lab-04"
    try:
        rates = lms.get_pass_rates(lab_id)
        if not rates:
            return f"No data for {lab_id}."
        result = f"Pass rates for {lab_id}:\n"
        for task, value in rates.items():
            if isinstance(value, dict):
                # Если API возвращает {pass_rate: float, attempts: int}
                percent = value.get('pass_rate', 0)
                attempts = value.get('attempts', 0)
                result += f"- {task}: {percent:.1f}% ({attempts} attempts)\n"
            else:
                # Если API возвращает просто число (процент)
                percent = float(value)
                result += f"- {task}: {percent:.1f}%\n"
        return result
    except Exception as e:
        return f"Error fetching scores for {lab_id}: {e}"