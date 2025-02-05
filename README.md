# sprachhilfer

[![tests](https://github.com/ShawonAshraf/sprachhilfer/actions/workflows/tests.yml/badge.svg)](https://github.com/ShawonAshraf/sprachhilfer/actions/workflows/tests.yml)

An LLM based application for learners of the German language to get feedback on their writing.

## live version

[Streamlit](https://sprachhilfer.streamlit.app/)


## local env setup

```bash
poetry shell
poetry install
```

## running locally

Create a `.env` file with the following contents:

```
LLM_BASE_URL=
LLM_API_KEY=
LLM_MODEL_NAME=
DEBUG=
```

Set `DEBUG` to `True` if you want debug logs locally. Other variables you can set from your OpenAI compatible LLM provider.

```bash
poetry run streamlit run src/frontend/ui.py
```

