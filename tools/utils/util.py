from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API")
KAKAO_API_KEY = os.getenv("KAKAO_MAP_API")
llm = ChatOpenAI(model='gpt-4o',openai_api_key=OPENAI_API_KEY)