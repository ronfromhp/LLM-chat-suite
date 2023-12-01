from langchain.chains.llm import LLMChain, PromptTemplate
from langchain.chat_models import ChatOpenAI
import chainlit as cl
import os
template = """{question}
"""

os.environ["ASSISTANT_ID"] = 'asst_MQ6N7UnG0FBgoQN62UY9xEel'

@cl.on_chat_start
def main():
  # Instantiate the chain for that user session
  prompt = PromptTemplate(template=template, input_variables=["question"])
  llm_chain = LLMChain(prompt=prompt, llm=ChatOpenAI(temperature=0), verbose=True)  
  
  # Store the chain in the user session
  cl.user_session.set("llm_chain", llm_chain)


@cl.on_message
async def on_message(message: cl.Message):
    chain = cl.user_session.get("llm_chain")  # type: LLMChain

    res = await chain.arun(
        question=message.content, callbacks=[cl.LangchainCallbackHandler()]
    )

    await cl.Message(content=res).send()
  
  