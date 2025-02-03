from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Settings class for configuring the Sprachhilfer application.

    Attributes:
        app_name (str): The name of the application. Defaults to "Sprachhilfer".
        llm_base_url (str): The base URL for accessing the LLM service.
        llm_api_key (SecretStr): Secret API key required for authentication with the LLM service.
        llm_model_name (str): The model name for the LLM service.
        debug (bool): Flag to toggle debugging mode.

    Configuration:
        Loads environment variables from the ".env" file.
    """

    app_name: str = "Sprachhilfer"

    llm_base_url: str = ""
    llm_api_key: SecretStr = SecretStr("")
    llm_model_name: str = ""
    debug: bool = False

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # type: ignore
