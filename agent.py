import os
from mistralai import Mistral
import discord
import logging


MISTRAL_MODEL = "mistral-large-latest"
SYSTEM_PROMPT = "You are Peter Griffin acting as a helpful assistant who flags copyrighted content."
logger = logging.getLogger("discord")



class MistralAgent:
    def __init__(self):
        MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

        self.client = Mistral(api_key=MISTRAL_API_KEY)

    async def run(self, message: discord.Message, history: list[list]):
        # Set up the messages for the API call
        # The first message is the system prompt
        message.content = message.content + "\nProvide a confidence score to your assessment of copyrighted material. Make sure that score is in this exact format at the end of your message, with nothing else after. 'Confidence: 56%'\n"
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        # Set up chat history
        total_words = len(message.content.split())
        for author_message_pair in history.reverse():
            history_message_word_count = len(author_message_pair[1].content.split())
            # check if we can fit this history message to prompt, if not skip rest of history
            if total_words + history_message_word_count > 1000:
                logger.info("Reached max word count of 1000, stopping history")
                break
            # set up right role and message for API call
            if author_message_pair[0] == "user":
                messages.append({"role": "user", "content": author_message_pair[1].content})
            else:
                messages.append({"role": "assistant", "content": author_message_pair[1].content})
            # update word count currently
            total_words += len(author_message_pair[1].content.split())
        
        # Add the newest message (question to model) to the chat history

        # Check if the message is too long
        messages.append({"role": "user", "content": message.content})
        if len(message.content.split()) > 1000:
            logger.info("Reached max word count of 1000, stopping history")
            return "I'm sorry, I can't answer that question. It's too long. Can you try again?"
        
        # Get the response from the Mistral agent
        response = await self.client.chat.complete_async(
            model=MISTRAL_MODEL,
            messages=messages,
        )

        return response.choices[0].message.content
