from loguru import logger

from backend.engine.base import BaseLLMEngine, BaseLLMResponse
from backend.settings import settings


class DeepSeekR1Engine(BaseLLMEngine):
    def format_response(self, raw_response: str) -> BaseLLMResponse:
        # separate the answer and the thought process
        parts = raw_response.split("</think>")

        assert len(parts) == 2

        thought = parts[0]
        # remove the remaining think tag
        thought = thought.replace("<think>", "").strip()

        answer = parts[1]
        # remove if there's an "Answer:" part
        answer = answer.replace("Answer:", "").strip()

        response = BaseLLMResponse(thought_process=thought, answer=answer)
        if settings.debug:
            logger.debug(response)

        return response
