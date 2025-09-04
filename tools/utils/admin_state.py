from typing import TypedDict
from pydantic import BaseModel, Field

class State(TypedDict):

    user_query : str 
    messages : list[str]
    plan : str
    restaurant : list[str]
    language: str
    keyword : str
    location : str
    classifier : str 
    response : str
    final_response : str


    
class Review(BaseModel):

    place_name : list[str] = Field(default='')
    place_url : list[str] = Field(default='')
    total_reviewers : list[str] = Field(default='')
    rating : list[str] = Field(default='')
    blogging : list[str] = Field(default='')
    time_schedule_opening : list[str] = Field(default='')
    time_schedule_closed : list[str] = Field(default='')
