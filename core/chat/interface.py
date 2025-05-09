# core/chat/interface.py

import streamlit as st
from core.chat.nlu_processor import detect_intent
from core.chat.response_builder import generate_response

def run_chat_interface():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.chat_message("assistant").write("Hi! Ask me anything about fantasy cricket, teams, or trivia! 🎯")

    user_input = st.chat_input("Ask about a player, team, or play a game...")

    if user_input:
        st.session_state.chat_history.append(("user", user_input))
        intent = detect_intent(user_input)
        response = generate_response(user_input, intent)
        st.session_state.chat_history.append(("assistant", response))

    for sender, message in st.session_state.chat_history:
        st.chat_message(sender).write(message)
