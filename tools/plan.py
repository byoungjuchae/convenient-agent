from .utils.admin_state import State
from .utils.util import llm
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from prompt_file import PLANNER_PROMPT
from operator import itemgetter


async def planner(state: State):

    prompt = ChatPromptTemplate.from_template(PLANNER_PROMPT)

    chain = {"user_query": itemgetter("user_query") |  RunnablePassthrough()} | prompt | llm | StrOutputParser()

    response = await chain.ainvoke({"user_query":state['user_query']})

    state['plan'] = response

    return state