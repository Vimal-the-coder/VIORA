import asyncio

from voice.speech_to_text import listen
from voice.text_to_speech import speak


def confirm_action(action):
    """Ask the user for voice confirmation."""

    question = f"Are you sure you want to {action}?"

    print(f"VIORA: {question}")

    # Speak the confirmation question
    asyncio.run(speak(question))

    # Listen for the answer
    answer = listen()

    if answer is None:
        return False

    answer = answer.lower().strip()

    print(f"You: {answer}")

    positive_answers = [
        "yes",
        "yeah",
        "yep",
        "confirm",
        "do it",
        "sure",
        "okay",
        "ok"
    ]

    negative_answers = [
        "no",
        "nope",
        "cancel",
        "don't",
        "do not"
    ]

    if answer in positive_answers:
        return True

    if answer in negative_answers:
        return False

    # Unknown answer = safest option
    asyncio.run(speak("I didn't understand. Action cancelled."))
    return False