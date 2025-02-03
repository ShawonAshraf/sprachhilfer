from backend.engine.r1engine import DeepSeekR1Engine
from backend.settings import settings
from templates.system import get_system_prompt


def main():
    r1_engine = DeepSeekR1Engine(
        model=settings.llm_model_name,
        api_key=settings.llm_api_key.get_secret_value(),
        base_url=settings.llm_base_url,
        system_input=get_system_prompt()
    )

    _ = r1_engine.generate("Wie hoch ist die Temperatur draußen?")


if __name__ == "__main__":
    main()
