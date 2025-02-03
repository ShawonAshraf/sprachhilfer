from backend.engine.r1engine import DeepSeekR1Engine


def test_generate(monkeypatch):
    def mock_generate(self, user_input):
        return "Mocked response"

    monkeypatch.setattr(DeepSeekR1Engine, 'generate', mock_generate)

    r1_engine = DeepSeekR1Engine(
        model="",
        api_key="",
        base_url="",
        system_input=None
    )

    assert r1_engine.generate("what is the colour of a rose?") == "Mocked response"


def test_format_response():
    r1_engine = DeepSeekR1Engine(
        model="",
        api_key="",
        base_url="",
        system_input=None
    )

    dummy_response = "<think>this is some thinking</think>\n\nI think."

    formatted = r1_engine.format_response(dummy_response)

    assert formatted.thought_process, "Thought process can't be none for R1 models"
    assert formatted.answer, "Answer can't be none"

    assert formatted.thought_process == "this is some thinking"
    assert formatted.answer == "I think."
