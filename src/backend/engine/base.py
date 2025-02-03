from openai import OpenAI

class BaseLLMEngine:
    def __init__(self, api_key, model, base_url, system_input):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.system_input = system_input

    def __prepare_inference_input(self, user_input):
        messages = []
        if self.system_input:
            messages.append(
                {"role": "system", "content": self.system_input}
            )
        if user_input:
            messages.append(
                {"role": "user", "content": user_input}
            )

        return messages

    def __generate_raw_response(self, user_input, temperature=0.1):
        messages = self.__prepare_inference_input(user_input)
        assert messages

        client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

        response = client.chat.completions.create(
            messages=messages,
            temperature=temperature,
            model=self.model
        )

        return response.choices[0].message.content

    def generate(self, user_input):
        raw_response = self.__generate_raw_response(user_input)
        formatted = self.format_response(raw_response)
        return formatted

    def format_response(self, raw_response):
        pass
