# sprachhilfer

[![tests](https://github.com/ShawonAshraf/sprachhilfer/actions/workflows/tests.yml/badge.svg)](https://github.com/ShawonAshraf/sprachhilfer/actions/workflows/tests.yml)

_sprachhilfer_ or _language assistant_ or _language helper_ is an LLM based application for learners of the German language to get feedback on their writing.


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

## roadmap

- [ ] [#2](https://github.com/ShawonAshraf/sprachhilfer/issues/2)
- [ ] [#3](https://github.com/ShawonAshraf/sprachhilfer/issues/3)
