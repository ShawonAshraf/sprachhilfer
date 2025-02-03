from backend.engine.r1engine import DeepSeekR1Engine
from backend.settings import settings
from templates.system import get_system_prompt
from loguru import logger


def get_llm_engine():
    logger.info("Starting LLM Engine")
    logger.info(f"Settings: {settings.json()}")

    r1_engine = DeepSeekR1Engine(
        model=settings.llm_model_name,
        api_key=settings.llm_api_key.get_secret_value(),
        base_url=settings.llm_base_url,
        system_input=get_system_prompt(),
    )

    return r1_engine
