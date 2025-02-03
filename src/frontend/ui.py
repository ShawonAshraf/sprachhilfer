import streamlit as st
from loguru import logger
from backend.engine.r1engine import DeepSeekR1Engine

from backend.main import get_llm_engine


def create_interface(llm_engine: DeepSeekR1Engine) -> None:
    logger.info("Starting interface creation")

    st.title("Sprachhilfer")

    # input text area
    st.header("Ihre Schrift")
    with st.form(key="input_form"):
        user_input = st.text_area(placeholder="Schreiben Sie hier bitte!", label="")

        col1, col2, col3 = st.columns(3)
        with col1:
            submit_btn = st.form_submit_button(label="Einreichen", icon="✅")
        with col2:
            pass
        with col3:
            clear_btn = st.form_submit_button(label="Leeren", icon="❌")

    # output area
    with st.container():
        st.header("Feedback")
        if submit_btn:
            with st.status("Bitte warten Sie!") as status:
                out = llm_engine.generate(user_input)
                status.update(label="Fertig!", state="complete")
                st.toast("Rückmeldung generiert")
            st.markdown(out.thought_process)

            st.markdown(out.answer)

        if clear_btn:
            pass


if __name__ == "__main__":
    engine = get_llm_engine()
    create_interface(engine)
