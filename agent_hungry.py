from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langgraph.checkpoint.memory import MemorySaver
from langchain.memory import RedisChatMessageHistory
from langchain_community.vectorstores import Milvus
from langchain_core.tools import tool
from tools.plan import planner
from tools.restaurant import rest_accomodation
from tools.language import check_language, language_converter
import pymilvus
from dotenv import load_dotenv
from operator import itemgetter
import os
import requests
from prompt_file import PLAN_SEARCH_PROMPT
import time
from tools.utils.admin_state import State


load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "hungry"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

history = RedisChatMessageHistory(
    url="redis://localhost:6379",
    ttl=3600,
    session_id="user_123"
)


# @tool(args_schema=Review)
# async def context_review(place_name: list[str], place_url : list[str], total_reviewers:list[str], rating: list[str], blogging: list[str], time_schedule : list[str]):
#     "if you want to know about the review of restaurant, use this tool. input document is the restaurant's information"
    
#     prompt = ChatPromptTemplate.from_template(PLAN_SEARCH_PROMPT)
#     chain = ({"place_name": itemgetter("place_name") | RunnablePassthrough(), "place_url":itemgetter("place_url") | RunnablePassthrough(),"rating": itemgetter("rating") | RunnablePassthrough(),"total_reviewers":itemgetter("total_reviewers") | RunnablePassthrough(), 
#         "blogging": itemgetter("blogging") | RunnablePassthrough(), "time_schedule": itemgetter("time_schedule") | RunnablePassthrough()}
#         | prompt | llm | StrOutputParser())
#     response = await chain.ainvoke({"place_name": place_name[0], "place_url": place_url[0],
#                 "rating":rating[0],"total_reviewers":total_reviewers[0],"blogging":blogging[0],
#                 "time_schedule": time_schedule_opening[0]})

#     return response



graph_builder = StateGraph(State)
graph_builder.add_node("planner",planner)
graph_builder.add_node("restaurant",rest_accomodation)
graph_builder.add_node("check_language",check_language)
graph_builder.add_node("language",language_converter)
graph_builder.add_edge("planner","restaurant")
graph_builder.add_edge("restaurant","check_language")
graph_builder.add_edge("check_language","language")
graph_builder.set_entry_point("planner")
checkpointer = MemorySaver()
graph = graph_builder.compile(checkpointer = checkpointer)



async def chatting(query:str):
    config = {"configurable": {"thread_id": "1","checkpoint_ns":"restaurant"}}
    asc = State(user_query=query)
    response = await graph.ainvoke(asc,config=config)

    res = response.get('final_response')
    print(res)
    return res

# def ranker(state: State):



# def responder(state: State):
    

