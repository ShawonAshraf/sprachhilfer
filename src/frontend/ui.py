import streamlit as st
from loguru import logger

from backend.engine.r1engine import DeepSeekR1Engine
from backend.main import get_llm_engine


logger.info("Setting page configuration")
st.set_page_config(
    page_title="Sprachhilfer",
    page_icon=":books:",
    menu_items={
        "About": "https://github.com/ShawonAshraf/sprachhilfer",
        "Report a Bug": "https://github.com/ShawonAshraf/sprachhilfer/issues",  # type: ignore
    },
)


def show_response(user_input: str, llm_engine: DeepSeekR1Engine) -> None:
    st.header("Feedback")
    with st.status("Bitte warten Sie!") as status:
        out = llm_engine.generate(user_input)
        status.update(label="Fertig!", state="complete")
        st.toast("Rückmeldung generiert 🤖")

    with st.expander("Denkprozess"):
        with st.chat_message("assistant"):
            st.caption("Ihr Feedback")
            st.markdown(out.thought_process)

    with st.chat_message("assistant"):
        st.caption("Antwort")
        st.markdown(out.answer)


def show_interface(llm_engine: DeepSeekR1Engine) -> None:
    logger.info("Starting interface")

    st.title("Sprachhilfer")
    # model info
    with st.container(border=True):
        st.markdown(f"**API:** {llm_engine.base_url}")
        st.markdown(f"**Model:** {llm_engine.model}")

    # input text area
    st.header("Ihre Schrift")
    with st.form(key="input_form"):
        user_input = st.text_area(
            placeholder="Schreiben Sie hier bitte!",
            label="schrift",
            label_visibility="hidden",
        )
        # triggers the response generation
        submit_btn = st.form_submit_button(label="Einreichen", icon="✅")

    # output area
    with st.container(border=True):
        if submit_btn:
            # check for input here
            # show an error if input is empty
            if not user_input:
                st.error("Input can't be empty!", icon="🚨")
            else:
                show_response(user_input, llm_engine)


if __name__ == "__main__":
    engine: DeepSeekR1Engine = get_llm_engine()
    show_interface(engine)
