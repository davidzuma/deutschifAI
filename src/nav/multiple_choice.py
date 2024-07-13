import streamlit as st

from utils.database import get_word_and_options


def multiple_choice_game():
    st.title("Deutsches Multiple-Choice-Spiel")
    if "word" not in st.session_state:
        (
            st.session_state.word,
            st.session_state.correct_translation,
            st.session_state.options,
        ) = get_word_and_options()

    st.write(f"Aktuelles Wort: {st.session_state.word}")

    # Create radio buttons for options
    choice = st.radio(
        "Wähle die richtige englische Übersetzung:", st.session_state.options
    )

    # Create a submit button
    if st.button("Check"):
        if choice == st.session_state.correct_translation:
            st.success("✅ Richtig! Gut gemacht")
        else:
            st.error(
                f"❌ die richtige Antwort war: {st.session_state.correct_translation}"
            )

    if st.button("Nächstes Wort"):
        (
            st.session_state.word,
            st.session_state.correct_translation,
            st.session_state.options,
        ) = get_word_and_options()
        st.rerun()


if __name__ == "__main__":
    multiple_choice_game()
