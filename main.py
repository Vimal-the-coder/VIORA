import asyncio
import threading

from PyQt6.QtWidgets import QApplication
from gui.viora_interface import VioraWindow
from voice.speech_to_text import listen
from voice.text_to_speech import speak
from commands.router import route_command
from ai.llm import ask_ai
from ai.memory import ConversationMemory


def run_voice_assistant():

    print("=" * 50)
    print("             VIORA IS ONLINE")
    print("=" * 50)

    memory = ConversationMemory(max_messages=10)

    # Startup message
    asyncio.run(
        speak("Hello, I am VIORA. I am online and ready to help you.")
    )

    while True:

        # =========================
        # LISTEN
        # =========================

        command = listen()

        if command is None:
            continue

        command = command.lower().strip()

        print(f"You: {command}")

        # =========================
        # EXIT
        # =========================

        if command in [
            "exit",
            "quit",
            "stop",
            "goodbye",
            "go offline",
            "shutdown viora",
        ]:

            asyncio.run(
                speak("Goodbye. VIORA is going offline.")
            )

            break

        # =========================
        # CLEAR MEMORY
        # =========================

        if command in [
            "clear memory",
            "forget conversation",
            "forget everything",
            "clear conversation",
        ]:

            memory.clear()

            asyncio.run(
                speak("Conversation memory has been cleared.")
            )

            continue

        # =========================
        # LOCAL COMMAND ROUTER
        # =========================

        response = route_command(command)

        if response:

            asyncio.run(
                speak(str(response))
            )

            memory.add("user", command)
            memory.add("assistant", str(response))

            continue

        # =========================
        # AI FALLBACK
        # =========================

        context = memory.get_context()

        print("VIORA: Asking AI...")

        try:

            response = ask_ai(
                command,
                context=context
            )

            if response:

                memory.add("user", command)
                memory.add("assistant", response)

                asyncio.run(
                    speak(response)
                )

            else:

                asyncio.run(
                    speak("Sorry, I could not generate a response.")
                )

        except Exception as e:

            print(f"AI Error: {e}")

            asyncio.run(
                speak(
                    "Sorry, I am having trouble connecting to my AI service."
                )
            )


def main():

    # =========================
    # CREATE PYQT APPLICATION
    # =========================

    app = QApplication([])

    # =========================
    # CREATE VIORA INTERFACE
    # =========================

    window = VioraWindow()

    window.show()

    # =========================
    # START VOICE ASSISTANT
    # =========================

    assistant_thread = threading.Thread(
        target=run_voice_assistant,
        daemon=True
    )

    assistant_thread.start()

    # =========================
    # START PYQT EVENT LOOP
    # =========================

    app.exec()


if __name__ == "__main__":
    main()