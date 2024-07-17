import streamlit as st

from utils.database import fetch_random_word


def english_translation_game():
    st.title("Deutsch üben")
    if "word_tuple" not in st.session_state:
        st.session_state.word_tuple = fetch_random_word()

    german_word, english_translation = st.session_state.word_tuple
    st.write(f"Übersetzen Sie das folgende Wort ins Englische: {german_word}")

    if "user_translation" not in st.session_state:
        st.session_state.user_translation = ""

    user_translation = st.text_input(
        "Ins Englische", value=st.session_state.user_translation
    )

    if st.button("Check"):
        if user_translation.lower().strip() == english_translation.lower().strip():
            st.success("✅ Richtig! Gut gemacht")
            st.session_state.user_translation = ""
        else:
            st.error(f"Nicht gut: {english_translation}")
            st.session_state.user_translation = ""

    if st.button("Nächster Wort"):
        st.session_state.word_tuple = fetch_random_word()
        st.rerun()
