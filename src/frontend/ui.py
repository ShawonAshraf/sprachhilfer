import streamlit as st
from loguru import logger

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


def create_interface() -> None:
    llm_engine = get_llm_engine()

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
        # TODO: fix later
        with col3:
            # clear_btn = st.form_submit_button(label="Leeren", icon="❌")
            pass
    # output area
    with st.container(border=True):
        if submit_btn:
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

        # TODO: implement the functionality later
        # if clear_btn:
        #     pass


if __name__ == "__main__":
    create_interface()
