import sys
import json
from services.llm_client import LLMClient
from services.tools import TOOLS
from services.lms_client import LmsClient
import config

llm = LLMClient()
lms = LmsClient(config.LMS_API_BASE_URL, config.LMS_API_KEY)

# Карта соответствия имени инструмента -> функция из LmsClient
TOOL_MAP = {
    "get_items": lms.get_items,
    "get_learners": lms.get_learners,
    "get_scores": lms.get_scores,
    "get_pass_rates": lms.get_pass_rates,
    "get_timeline": lms.get_timeline,
    "get_groups": lms.get_groups,
    "get_top_learners": lms.get_top_learners,
    "get_completion_rate": lms.get_completion_rate,
    "trigger_sync": lms.trigger_sync,
}

SYSTEM_PROMPT = """You are a helpful assistant that answers questions about the lab data.
You have access to several tools (API functions). When the user asks a question, decide which tool(s) to call.
If multiple tools are needed, call them in sequence, then use the results to answer.
Be concise but informative. If the user asks something unrelated to labs, be polite and explain what you can do."""

def route(user_message: str) -> str:
    """Обрабатывает сообщение пользователя через LLM с инструментами."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ]

    # Цикл вызова инструментов
    while True:
        # Вызываем LLM с текущими сообщениями
        response = llm.chat_completion(messages, tools=TOOLS)
        messages.append({"role": "assistant", "content": response.content, "tool_calls": response.tool_calls})

        # Если LLM не просит вызвать инструменты – выходим
        if not response.tool_calls:
            return response.content or "I'm not sure how to help. Try using /help for commands."

        # Выполняем каждый инструмент
        for tool_call in response.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            print(f"[tool] LLM called: {tool_name}({tool_args})", file=sys.stderr)

            # Находим функцию в TOOL_MAP
            func = TOOL_MAP.get(tool_name)
            if func is None:
                result = f"Error: tool {tool_name} not implemented"
            else:
                try:
                    result = func(**tool_args)
                except Exception as e:
                    result = f"Error executing {tool_name}: {e}"
            # Преобразуем результат в строку (можно JSON)
            result_str = json.dumps(result, ensure_ascii=False, indent=2) if isinstance(result, dict) else str(result)
            print(f"[tool] Result: {result_str[:200]}", file=sys.stderr)

            # Добавляем результат в сообщения
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result_str,
            })

        # После выполнения всех инструментов, снова идём в LLM (следующая итерация цикла)
        # (можно ограничить количество итераций)