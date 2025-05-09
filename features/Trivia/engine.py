# features/trivia/engine.py

import random

# Sample static questions for demo purposes
TRIVIA_QUESTIONS = {
    "easy": [
        {"question": "Who is known as the 'God of Cricket'?", "answer": "Sachin Tendulkar"},
        {"question": "How many players are there in a cricket team?", "answer": "11"}
    ],
    "medium": [
        {"question": "Which bowler has taken the most wickets in Test cricket?", "answer": "Muttiah Muralitharan"},
        {"question": "In which year did India win their first Cricket World Cup?", "answer": "1983"}
    ],
    "hard": [
        {"question": "Who was the captain of the Australian team during the 2003 World Cup?", "answer": "Ricky Ponting"},
        {"question": "Which Indian player has the highest score in a single ODI match?", "answer": "Rohit Sharma"}
    ]
}

def get_random_question(difficulty="easy"):
    """Returns a random question from the given difficulty level."""
    questions = TRIVIA_QUESTIONS.get(difficulty.lower(), TRIVIA_QUESTIONS["easy"])
    return random.choice(questions)

def check_answer(user_answer: str, correct_answer: str) -> bool:
    """Checks if the user's answer is correct (case-insensitive match)."""
    return user_answer.strip().lower() == correct_answer.strip().lower()

def format_question(question_data: dict) -> str:
    """Returns a formatted version of the trivia question."""
    return f"🧠 Trivia Time!\n\nQ: {question_data['question']}"

def get_trivia_question() -> str:
    """Return a random trivia question."""
    return "Who scored the fastest century in ODI cricket?"

