# core/chat/response_builder.py

from core.chat.nlu_processor import detect_intent
from services.llm_service import get_llm_response
from core.analytics.player_analyzer import analyze_player
from features.trivia.engine import get_trivia_question
from features.banter.mode import get_banter_reply

def build_response(user_input: str, session_state: dict = {}) -> str:
    intent = detect_intent(user_input)

    if intent == "greeting":
        return "Hey there! Ready to dominate fantasy cricket or have some fun?"

    elif intent == "player_query":
        player_name = extract_player_name(user_input)
        if player_name:
            return analyze_player(player_name)
        else:
            return "Please mention the player's name you'd like stats on."

    elif intent == "team_build":
        return "I can help build your dream fantasy team. Would you like form-based or stat-based suggestions?"

    elif intent == "trivia_game":
        return get_trivia_question()

    elif intent == "banter_mode":
        return get_banter_reply(user_input)

    elif intent == "live_analysis":
        return "Let me pull live match stats... (feature in progress)"

    elif intent == "goodbye":
        return "Catch you later! May your team always top the leaderboard 🏆"

    else:
        return get_llm_response(user_input)  # Fallback to LLM for general chat


def extract_player_name(text: str) -> str:
    # Naive extractor (replace with better NER if needed)
    for word in text.split():
        if word.istitle():  # crude check for names
            return word
    return ""
