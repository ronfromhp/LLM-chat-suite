import json
from openai import AsyncOpenAI
import asyncio
import os
from dotenv import load_dotenv
from langchain.agents import Tool
from langchain.agents.openai_assistant import OpenAIAssistantRunnable
from langchain.tools.wolfram_alpha import WolframAlphaQueryRun
from langchain.utilities.wolfram_alpha import WolframAlphaAPIWrapper
from langchain.utilities import SerpAPIWrapper

load_dotenv()

wolfram_api_wrapper = WolframAlphaAPIWrapper(wolfram_alpha_appid=os.environ.get("WOLFRAM_ALPHA_APPID"))
api_key = os.environ.get("OPENAI_API_KEY")
client = AsyncOpenAI(api_key=api_key)

search = SerpAPIWrapper()

tools = [
    {"type": "code_interpreter"},
    WolframAlphaQueryRun(api_wrapper=wolfram_api_wrapper),
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events. You should ask targeted questions",
    ),
    ]

print(tools)

async def create():

    instructions2 = """
You are a sophisticated chatbot designed to converse with users and help answer their queries. When responding to users, your messages should be in the following format:

chatbot: [Your response based on the user's message and context.]
intent: [A JSON-encoded object explaining the user's underlying intent and any parameters extracted from their message.]

For instance, if a user asks "What's the weather like in New York today?", you should respond with:

chatbot: The current weather in New York is partly cloudy with a high of 18°C and a low of 8°C.
intent: {"intent": "get_weather", "parameters": {"location": "New York", "date": "today"}}

Please ensure your responses are informative, succinct, and the intent JSON is accurately reflecting the user's request.
"""

# ... your existing create function code ...
   
    instructions = """You are a personal math tutor. Write and run code to answer math questions.
Enclose math expressions in $$ (this is helpful to display latex). Example:

Given a formula below $$ s = ut + \frac{1}{2}at^{2} $$ Calculate the value of $s$ when $u = 10\frac{m}{s}$ and $a = 2\frac{m}{s^{2}}$ at $t = 1s$
"""
   
    assistant = OpenAIAssistantRunnable.create_assistant(
        name = "Math Tutor",
        instructions = instructions,
        tools = tools,
        model = "gpt-4-1106-preview",
    )
    print("langchain assistant created", assistant.assistant_id)
    assistant_name = "searchistant"
    # append key vallue pair to assistants.json
    def load_or_create_json(filename):
        try:
            return json.load(open(filename, "r"))
        except FileNotFoundError:
            return {}
    assistant_dict = load_or_create_json("assistants.json")
    assistant_dict[assistant_name] = assistant.assistant_id
    json.dump(assistant_dict, open("assistants.json", "w"))

asyncio.run(create())
