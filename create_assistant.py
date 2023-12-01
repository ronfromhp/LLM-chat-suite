import json
from openai import AsyncOpenAI
import asyncio
import os
from dotenv import load_dotenv
from langchain.agents import load_tools, initialize_agent
from langchain.agents.openai_assistant import OpenAIAssistantRunnable
from langchain.chat_models import ChatOpenAI
from langchain.tools.wolfram_alpha import WolframAlphaQueryRun
from langchain.utilities.wolfram_alpha import WolframAlphaAPIWrapper
load_dotenv()

wolfram_api_wrapper = WolframAlphaAPIWrapper(wolfram_alpha_appid=os.environ.get("WOLFRAM_ALPHA_APPID"))
api_key = os.environ.get("OPENAI_API_KEY")
client = AsyncOpenAI(api_key=api_key)
tools = [
        {"type": "code_interpreter"},
        {
            "type": "function",
            "function": {
                    "name": "get_current_weather",
                    "description": "Get the current weather in a given location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state, e.g. San Francisco, CA",
                            },
                            "unit": {
                                "type": "string",
                                "description": "The unit of measurement for the temperature, e.g. Farenheit",
                            },
                        },
                        "required": ["location"],
                    }
            }
        },
        {
            "type": "function",
            "function": {
                    "name": "get_taxi_booking_information",
                    "description": "Get information required from the user to book a taxi for them if the user intends to book a taxi.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "pickup_location": {
                                "type": "string",
                                "description": "The pickup location of the user.",
                            },
                            "dropoff_location": {
                                "type": "string",
                                "description": "The dropoff location of the user.",
                            },
                            "pickup_time": {
                                "type": "string",
                                "description": "The pickup time of the user.",
                            },
                            "number_of_passengers": {
                                "type": "number",
                                "description": "The number of passengers.",
                            },
                        },
                        "required": ["pickup_location", "dropoff_location", "pickup_time", "number_of_passengers"],
                    }
            }
        }
    ]
    
tools = [WolframAlphaQueryRun(api_wrapper=wolfram_api_wrapper)]
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
    # assistant_id = await client.beta.assistants.create(
    #     name="Math Tutor",
    #     instructions=instructions,
    #     tools=tools,
    #     model="gpt-4-1106-preview",

    # )
    assistant = OpenAIAssistantRunnable.create_assistant(
        name = "Math Tutor",
        instructions = instructions,
        tools = tools,
        model = "gpt-4-1106-preview",
    )
    print("langchain assistant created", assistant)
    # print(assistant_id)
    assistant_name = "your assistent's name"
    # append key vallue pair to assistants.json
    assistant_dict = json.load(open("assistants.json", "r"))
    assistant_dict[assistant_name] = assistant.assistant_id
    json.dump(assistant_dict, open("assistants.json", "w"))

    # SAVE IT IN .env


asyncio.run(create())
