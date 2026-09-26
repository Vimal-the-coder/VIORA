class ConversationMemory:
    def __init__(self, max_messages=10):
        self.messages = []
        self.max_messages = max_messages

    def add(self, role, content):
        self.messages.append({
            "role": role,
            "content": content
        })

        # Keep only recent messages
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def get_context(self):
        if not self.messages:
            return ""

        context = []

        for message in self.messages:
            role = message["role"].capitalize()
            content = message["content"]

            context.append(f"{role}: {content}")

        return "\n".join(context)

    def clear(self):
        self.messages.clear()