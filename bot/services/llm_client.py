import openai
import config

class LLMClient:
    def __init__(self):
        self.client = openai.OpenAI(
            base_url=config.LLM_API_BASE_URL,
            api_key=config.LLM_API_KEY,
        )
        self.model = config.LLM_API_MODEL

    def chat_completion(self, messages, tools=None):
        params = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.2,
        }
        if tools:
            params["tools"] = tools
            params["tool_choice"] = "auto"
        response = self.client.chat.completions.create(**params)
        return response.choices[0].message