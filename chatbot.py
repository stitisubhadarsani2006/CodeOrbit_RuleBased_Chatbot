"""
Rule-Based Chatbot (Python CLI version)
----------------------------------------
This chatbot has no AI model behind it. Every reply comes from a fixed
set of rules: it looks for known keywords/phrases inside whatever the
user typed, and returns the response tied to the FIRST rule that
matches. If nothing matches, it falls back to a generic reply.

How the decision process works, step by step:
  1. Clean up the input (lowercase it, strip extra spaces) so that
     "Hello", "hello", and "  HELLO  " are all treated the same way.
  2. Check the cleaned input against each rule category in order:
     greetings -> farewells -> thanks -> "how are you" -> identity
     questions -> help requests -> general questions -> fallback.
  3. Each category is just a list of keywords/phrases. If ANY keyword
     in that list is found inside the user's message, that category's
     response is chosen and no further categories are checked.
  4. If none of the categories match, and the message isn't even a
     question, the fallback response is used.

This "first match wins, ordered top to bottom" structure is exactly
like a chain of if / elif / else statements — it's just written with
lists of keywords instead of one big block of conditions, which makes
it easier to add new rules later.
"""

import random

# ---------------------------------------------------------------------------
# RULES: each entry is (list_of_trigger_keywords, list_of_possible_replies)
# Using a list of possible replies (instead of just one) lets the bot vary
# its answers a bit, picked randomly, so it doesn't feel too robotic.
# ---------------------------------------------------------------------------

GREETING_KEYWORDS = ["hi", "hello", "hey", "greetings", "good morning", "good evening"]
GREETING_RESPONSES = [
    "Hello! How can I help you today?",
    "Hi there! What's on your mind?",
    "Hey! Good to see you.",
]

FAREWELL_KEYWORDS = ["bye", "goodbye", "see you", "see ya", "farewell"]
FAREWELL_RESPONSES = [
    "Goodbye! Have a great day.",
    "See you later!",
    "Take care!",
]

THANKS_KEYWORDS = ["thanks", "thank you", "appreciate it"]
THANKS_RESPONSES = [
    "You're welcome!",
    "Happy to help!",
    "Anytime!",
]

WELLBEING_KEYWORDS = ["how are you", "how're you", "how are things"]
WELLBEING_RESPONSES = [
    "I'm just a program, but I'm running smoothly! How about you?",
    "Doing well, thanks for asking!",
]

IDENTITY_KEYWORDS = ["your name", "who are you", "what are you"]
IDENTITY_RESPONSES = [
    "I'm a simple rule-based chatbot built with Python.",
    "Just a small chatbot that matches keywords to canned replies.",
]

HELP_KEYWORDS = ["help", "what can you do", "commands"]
HELP_RESPONSES = [
    "I can respond to greetings, farewells, thanks, and a few simple "
    "questions. Try saying 'hi', asking 'how are you', or asking my name!",
]

FALLBACK_RESPONSES = [
    "I'm not sure I understand. Could you rephrase that?",
    "Sorry, I don't have a rule for that yet.",
    "Hmm, I don't know how to respond to that.",
]

GENERIC_QUESTION_RESPONSES = [
    "That's an interesting question, but I don't have a specific rule "
    "for it. I can only answer what I've been programmed to recognize.",
]


def contains_any(text, keywords):
    """Return True if any keyword appears anywhere inside text."""
    return any(keyword in text for keyword in keywords)


def get_response(user_input):
    """
    Core decision logic of the chatbot.

    This is the heart of the "rule-based" approach: a straightforward
    if / elif chain, checked top to bottom, where the FIRST matching
    rule decides the reply. Order matters — more specific rules (like
    'how are you') are checked before generic fallback logic.
    """
    text = user_input.lower().strip()

    if contains_any(text, GREETING_KEYWORDS):
        return random.choice(GREETING_RESPONSES)

    elif contains_any(text, FAREWELL_KEYWORDS):
        return random.choice(FAREWELL_RESPONSES)

    elif contains_any(text, THANKS_KEYWORDS):
        return random.choice(THANKS_RESPONSES)

    elif contains_any(text, WELLBEING_KEYWORDS):
        return random.choice(WELLBEING_RESPONSES)

    elif contains_any(text, IDENTITY_KEYWORDS):
        return random.choice(IDENTITY_RESPONSES)

    elif contains_any(text, HELP_KEYWORDS):
        return random.choice(HELP_RESPONSES)

    elif "?" in text:
        # Catches any other question we don't have a specific rule for,
        # so the bot at least acknowledges it was asked a question.
        return random.choice(GENERIC_QUESTION_RESPONSES)

    else:
        # No rule matched at all -> fallback response.
        return random.choice(FALLBACK_RESPONSES)


def main():
    print("Rule-Based Chatbot (type 'quit' or 'exit' to stop)")
    print("-" * 50)

    while True:
        user_input = input("You: ")

        # Exit condition checked first, before running it through the rules.
        if user_input.lower().strip() in ("quit", "exit"):
            print("Bot: Goodbye!")
            break

        response = get_response(user_input)
        print(f"Bot: {response}")


if __name__ == "__main__":
    main()
