import config
from services.lms_client import LmsClient

lms = LmsClient(config.LMS_API_BASE_URL, config.LMS_API_KEY)

def start() -> str:
    return "Welcome! I'm your lab assistant bot. Use /help to see commands."

def help() -> str:
    return """Available commands:
/start - welcome message
/help - show this help
/health - check backend status
/labs - list available labs
/scores <lab> - get per-task pass rates (e.g., /scores lab-04)"""

def health() -> str:
    try:
        items = lms.get_items()
        count = len(items)
        return f"Backend is healthy. {count} items available."
    except Exception as e:
        # Формируем сообщение с ошибкой, без traceback, но с деталями
        return f"Backend error: {e}"

def labs() -> str:
    try:
        labs_list = lms.get_labs()
        if not labs_list:
            return "No labs found."
        result = "Available labs:\n"
        for lab in labs_list:
            # Предполагается, что в данных есть поле 'name' с полным названием,
            # например "Lab 01 — Products, Architecture & Roles"
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
        if isinstance(rates, dict):
            for task, data in rates.items():
                if isinstance(data, dict):
                    percent = data.get('pass_rate', 0)
                    attempts = data.get('attempts', 0)
                    result += f"- {task}: {percent:.1f}% ({attempts} attempts)\n"
                else:
                    percent = float(data)
                    result += f"- {task}: {percent:.1f}%\n"
        elif isinstance(rates, list):
            for entry in rates:
                task = entry.get('task', 'Unknown')
                percent = entry.get('pass_rate', 0)
                attempts = entry.get('attempts', 0)
                result += f"- {task}: {percent:.1f}% ({attempts} attempts)\n"
        else:
            result += str(rates)
        return result
    except Exception as e:
        return f"Error fetching scores for {lab_id}: {e}"