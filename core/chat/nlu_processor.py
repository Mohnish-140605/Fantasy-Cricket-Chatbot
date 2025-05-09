# core/chat/nlu_processor.py

import re

INTENTS = {
    "player_query": ["form", "stats", "record", "average", "performance"],
    "team_build": ["best team", "fantasy team", "suggest team", "pick players"],
    "trivia_game": ["trivia", "quiz", "question", "challenge"],
    "banter_mode": ["banter", "roast", "fun", "joke", "trash talk"],
    "live_analysis": ["live", "match", "who's winning", "current score"],
    "greeting": ["hello", "hi", "hey"],
    "goodbye": ["bye", "goodbye", "see you"],
}

def detect_intent(user_input: str) -> str:
    user_input = user_input.lower()
    for intent, keywords in INTENTS.items():
        for kw in keywords:
            if re.search(rf"\b{re.escape(kw)}\b", user_input):
                return intent
    return "unknown"
