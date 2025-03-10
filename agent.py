import os
from mistralai import Mistral
import discord

MISTRAL_MODEL = "mistral-large-latest"
SYSTEM_PROMPT = "You are Peter Griffin who is acting as a helpful assistant."


class MistralAgent:
    def __init__(self):
        MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

        self.client = Mistral(api_key=MISTRAL_API_KEY)

    async def run(self, message: discord.Message, history: list[list]):
        # Set up the messages for the API call
        # The first message is the system prompt
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        # Set up chat history
        for author_message_pair in history:
            if author_message_pair[0] == "user":
                messages.append({"role": "user", "content": author_message_pair[1].content})
            else:
                messages.append({"role": "assistant", "content": author_message_pair[1].content})
        
        # Add the newest message (question to model) to the chat history
        messages.append({"role": "user", "content": message.content})

        # Get the response from the Mistral agent
        response = await self.client.chat.complete_async(
            model=MISTRAL_MODEL,
            messages=messages,
        )

        return response.choices[0].message.content
