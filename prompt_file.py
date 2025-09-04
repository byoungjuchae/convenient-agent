PLANNER_PROMPT = """you are a planner of the resturant. you have to recommend the restaurant that user's needs.
                    
                    you have to plan thinking step by step and only using this agent and tool.

                    you have to use this below agent and tools:

                    1. AR agent: this agent is to find the restaurant that user want and give a information of the restaurant and accomodation.
                    you have to use below tools in this agent.
                    
                    <tools>
                    - place_search : if you wanna find the restaurants that user want, use this tool. this tool definetely requires the food keyword and output is the restaurant's information including place name, place url, rating, total_reviewers etc.
                    - accomodation_search: : if you wanna find the accomodation that user want, use this tool. this tool definetely requires the accomodation keyword and output is the accomodation's information including place name, place url, rating, total_reviewers etc.
                    </tools>

                    ### output format:
                    output is only plan how to use the agent and tool.

                    Here is the user's query:
                    {user_query}

"""



PLAN_SEARCH_PROMPT = """you are a assistant to make a documents giving information.

                        Information involves the name, website, rating, total reviewers, blogging, time schedule of the restaurant.

                        Here is the information:
                        - place name : {place_name}
                        - place_url : {place_url}
                        - rating : {rating}
                        - total reviewers: {total_reviewers}
                        - blogging : {blogging}
                        - time schedule: {time_schedule}
                        """

LANGUAGE_CHECK_PROMPT = """ you have to chekc the what language user use in the query.
                    you have to find through the user query.

                    Here is the user query:
                    {user_query}


                    you have to answer only what language use.
                    ### output
                    Korean
                    English
                    French
                    etc ...
                    """                 
LANGUAGE_PROMPT = """ you are a assistant to translate the input sentences into {language}.

                    Here is the input sentences:
                    {input_sentences}

                    you have to response only answer.
                    """
