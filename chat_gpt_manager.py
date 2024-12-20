import openai

class ChatGPTClient:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        openai.api_key = self.api_key

    def get_response(self, prompt: str, role: str = "user") -> str:
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": role, "content": prompt}
                ]
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Произошла ошибка: {e}"
