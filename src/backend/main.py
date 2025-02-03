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

    print(r1_engine.generate("what is the colour of a rose?"))


if __name__ == "__main__":
    main()
