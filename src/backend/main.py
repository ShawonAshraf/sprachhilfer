from backend.engine.r1engine import DeepSeekR1Engine
import os

def main():
    r1_engine = DeepSeekR1Engine(
        model=str(os.getenv("LLM_MODEL_NAME")),
        api_key=os.getenv("LLM_API_KEY"),
        base_url=os.getenv("LLM_BASE_URL"),
        system_input=None
    )

    print(r1_engine.generate("what is the colour of a rose?"))

if __name__ == "__main__":
    main()
