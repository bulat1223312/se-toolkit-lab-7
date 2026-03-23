import sys
import json
import config
from services.llm_client import LLMClient
from services.tools import TOOLS
from services.lms_client import LmsClient

llm = LLMClient()
lms = LmsClient(config.LMS_API_BASE_URL, config.LMS_API_KEY)

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

SYSTEM_PROMPT = """You are a helpful assistant that answers questions about lab data. You have access to several tools (API functions). When the user asks a question, decide which tool(s) to call. If multiple tools are needed, call them in sequence, then use the results to answer. Be concise but informative. If the user asks something unrelated to labs, be polite and explain what you can do.

For multi-step queries like "which lab has the lowest pass rate", first call get_items to list all labs, then for each lab call get_pass_rates, compare the overall pass rates (e.g., average of tasks), and respond with the lab name and the percentage.

For "which group is doing best in lab 3", call get_groups with lab='lab-03', analyze the group scores, and respond with the group name and its average score.

Always include numbers and percentages in your answer when available."""

def route(user_message: str) -> str:
    try:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ]

        max_iterations = 5
        for _ in range(max_iterations):
            response = llm.chat_completion(messages, tools=TOOLS)
            msg = {"role": "assistant", "content": response.content}
            if response.tool_calls:
                msg["tool_calls"] = response.tool_calls
            messages.append(msg)

            if not response.tool_calls:
                return response.content or "I'm not sure how to help. Try using /help for commands."

            for tool_call in response.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                print(f"[tool] LLM called: {tool_name}({tool_args})", file=sys.stderr)

                func = TOOL_MAP.get(tool_name)
                if func is None:
                    result = f"Error: tool {tool_name} not implemented"
                else:
                    try:
                        result = func(**tool_args)
                    except Exception as e:
                        result = f"Error executing {tool_name}: {e}"

                if isinstance(result, (dict, list)):
                    result_str = json.dumps(result, ensure_ascii=False, indent=2)
                else:
                    result_str = str(result)

                print(f"[tool] Result: {result_str[:200]}", file=sys.stderr)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result_str,
                })

        return "I'm still processing. Please try again later."
    except Exception as e:
        print(f"Error in route: {e}", file=sys.stderr)
        return f"Sorry, an error occurred: {e}"