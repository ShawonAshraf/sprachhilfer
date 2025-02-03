from loguru import logger

from backend.engine.base import BaseLLMEngine, BaseLLMResponse
from backend.settings import settings


class DeepSeekR1Engine(BaseLLMEngine):
    """
    DeepSeekR1Engine: Extends from the BaseLLMEngine class and provides a format_response implementation for DeepSeekR1 models.
    """

    def format_response(self, raw_response: str) -> BaseLLMResponse:
        """
        Extracts the thought process and answer from a raw response string and returns them in a BaseLLMResponse object.
        The function splits the raw response using the "</think>" delimiter expecting exactly two parts:
        one for the thought process (enclosed in "<think>" tags) and one for the answer.
        It removes the "<think>" tag from the thought process, strips any leading "Answer:" text from the answer,
        and trims whitespace from both parts.
        Args:
            raw_response (str): The raw response string containing both the thought process and the answer.
        Returns:
            BaseLLMResponse: An object encapsulating the cleaned thought process and answer.
        Raises:
            AssertionError: If the raw response does not contain exactly one "</think>" delimiter.
        """

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
