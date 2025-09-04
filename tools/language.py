from .utils.admin_state import State
from .utils.util import llm
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
from prompt_file import LANGUAGE_PROMPT,LANGUAGE_CHECK_PROMPT

async def check_language(state:State):

    prompt = ChatPromptTemplate.from_template(LANGUAGE_CHECK_PROMPT)

    chain = {"user_query": itemgetter("user_query") | RunnablePassthrough()} | prompt | llm | StrOutputParser()

    response = await chain.ainvoke({"user_query": state.get('user_query')})

    state['language'] = response
    
    return state

async def language_converter(state:State):

    prompt = ChatPromptTemplate.from_template(LANGUAGE_PROMPT)


    chain = {"language": itemgetter("language") | RunnablePassthrough(), "input_sentences": itemgetter("input_sentences") | RunnablePassthrough() } | prompt | llm | StrOutputParser()

    response = await chain.ainvoke({"input_sentences":state.get('restaurant'),"language":state.get('language')})

    state['final_response'] = response

    return state