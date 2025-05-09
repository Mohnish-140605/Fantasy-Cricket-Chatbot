# features/banter/personality_engine.py

import random

# Different personalities for banter
PERSONALITIES = {
    "friendly": [
        "Nice choice! Keep it up, you're doing great!",
        "Oh, that was a brilliant pick! You're on fire!",
        "You're a cricket genius, aren't you? Keep going!"
    ],
    "sarcastic": [
        "Wow, what a pick... maybe try not to break your streak?",
        "Really? That's your pick? Well, good luck!",
        "Ah, another genius decision. Let’s see how this turns out!"
    ],
    "energetic": [
        "Yes! That's what I'm talking about! Woohoo!",
        "Cracking choice! You're on your way to victory!",
        "Let's go! That pick was fire, mate!"
    ],
    "mysterious": [
        "Only time will tell if that was the right pick...",
        "Hmm, that might just work... or not... who knows?",
        "You're playing a dangerous game... let's see how it turns out."
    ]
}

def get_banter(personality="friendly"):
    """Returns a random banter response based on personality."""
    return random.choice(PERSONALITIES.get(personality.lower(), PERSONALITIES["friendly"]))

def handle_banter(user_input: str, personality="friendly"):
    """Handle banter based on user input and personality mode."""
    if "?" in user_input:
        # Provide a fun response if a question is asked
        return get_banter(personality)
    elif "good pick" in user_input or "nice choice" in user_input:
        # Positive feedback if they celebrate a decision
        return get_banter("energetic")
    else:
        # Default response
        return get_banter(personality)
