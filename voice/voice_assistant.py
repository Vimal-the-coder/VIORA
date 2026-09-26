import time
import asyncio

from voice.speech_to_text import listen
from voice.text_to_speech import speak
from commands.router import route_command
from ai.llm import ask_ai
from ai.memory import ConversationMemory


# Conversation memory
memory = ConversationMemory(max_messages=10)


def main():
    print("VIORA is starting...")

    # Startup greeting
    asyncio.run(speak("Good morning, Boss. VIORA systems have been successfully initialized."))

    while True:

        # -------------------------
        # SPEECH TO TEXT
        # -------------------------
        start = time.time()

        command = listen()

        print(f"STT time: {time.time() - start:.2f}s")

        if command is None:
            continue

        command = command.strip()

        print(f"You: {command}")

        # -------------------------
        # EXIT COMMANDS
        # -------------------------
        if command.lower() in ["exit", "quit", "stop"]:
            asyncio.run(speak("Goodbye."))
            break

        # -------------------------
        # ROUTER
        # -------------------------
        start = time.time()

        command_response = route_command(command)

        print(f"Router time: {time.time() - start:.2f}s")

        # -------------------------
        # LOCAL COMMAND HANDLED
        # -------------------------
        if command_response:

            print(f"VIORA: {command_response}")

            start = time.time()

            asyncio.run(speak(command_response))

            print(f"TTS time: {time.time() - start:.2f}s")

            continue

        # -------------------------
        # GEMINI + MEMORY
        # -------------------------
        start = time.time()

        # Get previous conversation
        context = memory.get_context()

        # Ask Gemini with context
        response = ask_ai(
            command,
            context=context
        )

        print(f"AI time: {time.time() - start:.2f}s")

        # -------------------------
        # SAVE MEMORY
        # -------------------------
        memory.add("user", command)
        memory.add("assistant", response)

        print(f"VIORA: {response}")

        # -------------------------
        # TTS
        # -------------------------
        start = time.time()

        asyncio.run(speak(response))

        print(f"TTS time: {time.time() - start:.2f}s")


if __name__ == "__main__":
    main()