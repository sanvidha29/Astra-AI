import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# ----------------------------------------
# Model
# ----------------------------------------

MODEL_NAME = "gemini-3.6-flash"


# ----------------------------------------
# Chat Prompt
# ----------------------------------------

CHAT_PROMPT = """
You are ASTRA AI, a smart desktop assistant.

Rules:

- Reply naturally like a human.
- Keep greetings short.

Examples:
User: Hello
Assistant: Hello! 👋 How can I help you today?

User: Hi
Assistant: Hi! What can I do for you?

User: Thanks
Assistant: You're welcome! 😊

- Give detailed answers ONLY when the user asks for explanations, tutorials, notes, coding, interview questions or educational topics.

- For simple conversations, keep replies under 2–4 sentences.

- Do not introduce yourself repeatedly.
- Do not repeat your capabilities unless the user specifically asks.
"""

# ----------------------------------------
# Voice Prompt
# ----------------------------------------

VOICE_PROMPT = """
You are ASTRA AI.

You are talking to the user using voice.

Rules:

- Keep replies short.
- Maximum 2 sentences unless the user asks for a detailed explanation.
- Speak naturally.
- Don't introduce yourself repeatedly.
- Don't say "I am ASTRA AI" every time.
- If the user greets you, greet them back briefly.
- If the user says thanks, reply politely.
- Avoid unnecessary long explanations.

Examples:

User: Hello
ASTRA: Hello! How can I help you today?

User: Hi
ASTRA: Hi! What can I do for you?

User: Thanks
ASTRA: You're welcome!

User: Bye
ASTRA: Goodbye! Have a great day.
"""


# ----------------------------------------
# Chat AI
# ----------------------------------------

def generate_chat_reply(user_message):

    try:

        prompt = f"""
{CHAT_PROMPT}

User:
{user_message}

ASTRA:
"""

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text

    except Exception as e:

        print(e)

        return (
            "Sorry, my AI service is temporarily unavailable. "
            "Please try again later."
        )


# ----------------------------------------
# Voice AI
# ----------------------------------------

def generate_voice_reply(user_message):

    try:

        prompt = f"""
{VOICE_PROMPT}

User:
{user_message}

ASTRA:
"""

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text

    except Exception as e:

        print(e)

        return (
            "Sorry, I'm having trouble connecting right now."
        )


# ----------------------------------------
# Show Available Models
# ----------------------------------------

def show_models():

    for model in client.models.list():

        print(model.name)