import speech_recognition as sr


def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("VIORA: Listening...")

        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"You: {text}")
        return text

    except sr.UnknownValueError:
        print("VIORA: Sorry, I couldn't understand you.")
        return None

    except sr.RequestError as e:
        print(f"VIORA: Speech recognition service error: {e}")
        return None


if __name__ == "__main__":
    listen()