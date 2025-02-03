import abc
from typing import List, Optional

from openai import OpenAI
from pydantic import BaseModel


class BaseLLMResponse(BaseModel):
    thought_process: str
    answer: str


class BaseLLMEngine(BaseModel):
    def __init__(
        self,
        model: str,
        base_url: Optional[str],
        system_input: Optional[str],
        api_key: Optional[str],
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.system_input = system_input

    def __prepare_inference_input(self, user_input: str) -> List:
        messages = []
        if self.system_input:
            messages.append({"role": "system", "content": self.system_input})
        if user_input:
            messages.append({"role": "user", "content": user_input})

        return messages

    def __generate_raw_response(
        self, user_input: str, temperature: float = 0.1
    ) -> Optional[str]:
        messages = self.__prepare_inference_input(user_input)
        assert len(messages) >= 1

        client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

        response = client.chat.completions.create(
            messages=messages, temperature=temperature, model=self.model
        )

        return response.choices[0].message.content

    def generate(self, user_input: str) -> Optional[BaseLLMResponse]:
        raw_response = self.__generate_raw_response(user_input)
        return self.format_response(raw_response) if raw_response else None

    @abc.abstractmethod
    def format_response(self, raw_response: str) -> BaseLLMResponse:
        pass
