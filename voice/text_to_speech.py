import re
import asyncio
import edge_tts
import pygame
import os


def clean_for_speech(text):
    # Remove Markdown formatting
    text = re.sub(r"[*_~`#]", "", text)

    # Convert common symbols into speech-friendly words
    replacements = {
        "&": " and ",
        "@": " at ",
        "%": " percent ",
        "+": " plus ",
        "=": " equals ",
        "<": " less than ",
        ">": " greater than ",
        "|": " ",
    }

    for symbol, replacement in replacements.items():
        text = text.replace(symbol, replacement)

    return re.sub(r"\s+", " ", text).strip()


async def speak(text):
    text = clean_for_speech(text)

    print(f"VIORA: {text}")

    # Generate deeper, slower assistant-style voice
    communicate = edge_tts.Communicate(
        text,
        "en-IN-PrabhatNeural",
        rate="+5%",
        pitch="-20Hz",
        volume="+0%"
    )

    await communicate.save("voice.mp3")

    # Play audio directly
    pygame.mixer.init()
    pygame.mixer.music.load("voice.mp3")
    pygame.mixer.music.play()

    # Wait until speech finishes
    while pygame.mixer.music.get_busy():
        await asyncio.sleep(0.1)

    pygame.mixer.music.stop()
    pygame.mixer.quit()

    # Delete temporary audio file
    if os.path.exists("voice.mp3"):
        os.remove("voice.mp3")


if __name__ == "__main__":
    asyncio.run(
        speak("Hello, I am VIORA. How can I help you?")
    )