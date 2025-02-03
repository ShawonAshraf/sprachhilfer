import abc
from typing import List, Optional

from loguru import logger
from openai import OpenAI
from pydantic import BaseModel

from backend.settings import settings


class BaseLLMResponse(BaseModel):
    """
    Represents a response from the language model, encapsulating both the internal thought process and the final answer.

    Attributes:
        thought_process (str): A detailed explanation of how the answer was derived.
        answer (str): The final response produced by the language model.
    """

    thought_process: str
    answer: str


class BaseLLMEngine(BaseModel):
    """
    BaseLLMEngine provides an abstract base for interacting with a language model (LLM)
    via an API client. It is responsible for preparing input messages, invoking the API,
    and formatting the response produced by the LLM.

    Attributes:
        model (str): The identifier of the LLM to use.
        base_url (Optional[str]): The API endpoint for the LLM.
        system_input (Optional[str]): An optional system prompt to guide the LLM’s behavior.
        api_key (Optional[str]): The API key used for authentication with the LLM service.

    Methods:
        __prepare_inference_input(user_input: str) -> List[Dict[str, str]]:
            Constructs the list of messages for input to the LLM, including any system prompt
            and the user’s input. Logs the messages if debug settings are enabled.

        __generate_raw_response(user_input: str, temperature: float = 0.1) -> Optional[str]:
            Prepares the input messages, initializes the LLM client, and sends the request.
            Returns the raw text response from the LLM after logging the details if debugging is enabled.

        generate(user_input: str) -> Optional[BaseLLMResponse]:
            Manages the full generation process by obtaining the raw response from the LLM,
            and then formatting it into a BaseLLMResponse using the abstract format_response method.

        format_response(raw_response: str) -> BaseLLMResponse:
            An abstract method that must be implemented by subclasses to parse and format
            the raw response string into a structured BaseLLMResponse.
    """

    model: str
    base_url: Optional[str]
    system_input: Optional[str]
    api_key: Optional[str]

    def __prepare_inference_input(self, user_input: str) -> List:
        """
        Prepares the inference input messages by combining system and user inputs.

        If a system input is configured, it is added first as a message with the role "system". Then,
        if a user input is provided, it is appended as a message with the role "user". Additionally,
        if debugging is enabled, the generated messages are logged.

        Parameters:
            user_input (str): The user-provided input message.

        Returns:
            List[dict]: A list of message dictionaries ready for inference.
        """
        
        messages = []
        if self.system_input:
            messages.append({"role": "system", "content": self.system_input})
        if user_input:
            messages.append({"role": "user", "content": user_input})

        if settings.debug:
            logger.debug(messages)

        return messages

    def __generate_raw_response(
        self, user_input: str, temperature: float = 0.1
    ) -> Optional[str]:
        """
        Generate a raw response string from the LLM client using the provided user input.

        Parameters:
            user_input (str): The input string to be processed by the LLM.
            temperature (float, optional): A parameter to control randomness in the response generation. Defaults to 0.1.

        Returns:
            Optional[str]: The raw response content from the LLM client if generation is successful, otherwise None.

        Raises:
            AssertionError: If the prepared messages list is empty.
        """
        
        messages = self.__prepare_inference_input(user_input)
        assert len(messages) >= 1

        logger.info(f"Initialising LLM Client with base_url: {self.base_url}")
        client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

        response = client.chat.completions.create(
            messages=messages, temperature=temperature, model=self.model
        )

        raw_response = response.choices[0].message.content
        if settings.debug:
            logger.debug(raw_response)

        return raw_response

    def generate(self, user_input: str) -> Optional[BaseLLMResponse]:
        """
        Generate a formatted response based on the provided user input.
        This method logs the provided input, generates a raw response using the
        internal __generate_raw_response method, and then formats that response using
        the format_response method. If no raw response is produced, the method returns None.
        Parameters:
            user_input (str): The input string from the user.
        Returns:
            Optional[BaseLLMResponse]: A formatted response if a raw response is generated,
            otherwise None.
        """

        logger.info(f"Generating response for input: {user_input}")
        raw_response = self.__generate_raw_response(user_input)
        return self.format_response(raw_response) if raw_response else None

    @abc.abstractmethod
    def format_response(self, raw_response: str) -> BaseLLMResponse:
        """
        Format the given raw LLM response into a structured BaseLLMResponse object.
        Parameters:
            raw_response (str): The raw string output from the language model.
        Returns:
            BaseLLMResponse: The formatted response encapsulated in a BaseLLMResponse object.
        """

        pass
