import google.generativeai as genai
from datetime import date
import requests
from utils.tools_use import ToolsUse
from utils.function_use import CallableFunction
from dotenv import load_dotenv
import os
load_dotenv()


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class Agent:
    def __init__(self):
        self.serp_api_key = os.getenv("SERP_API_KEY")
        model = genai.GenerativeModel('gemini-1.5-flash', tools=ToolsUse().tools)
        self.chat = model.start_chat()

    


    def mission_prompt(self,prompt:str):

        today = date.today()

        return f"""
        Thought: I need to understand the user's request and determine if I need to use any tools to assist them. And I always recommend some event ans hotel to user with minimal information.
        Action: 
        - I will use the event and hotel APIs and event API to get the information.
        - I always recommend some event and hotel to user with minimal information.
        - I always respond to the user's request with the information I have gathered without mention the tools I used.

        [QUESTION] 
        {prompt}

        [DATETIME]
        {today}

        """.strip()



    def answer(self,user_prompt):
        prompt = self.mission_prompt(user_prompt)
        response = self.chat.send_message(prompt)
        fcs = response.candidates[0].content.parts

        result_event = None
        result_hotel = None

        parts = []

        for fc in fcs:
            fc = fc.function_call
            if fc.name == "event_api":
                result_event = CallableFunction().event_api(fc.args['query'], fc.args.get('htichips', "date:today"))
                parts.append( genai.protos.Part(
                        function_response=genai.protos.FunctionResponse(
                            name='event_api',
                            response={'result': result_event}
                        )
                    ))
            elif fc.name == "hotel_api":
                result_hotel = CallableFunction().hotel_api(fc.args['query'], fc.args['check_in_date'], fc.args['check_out_date'])
                parts.append( genai.protos.Part(
                        function_response=genai.protos.FunctionResponse(
                            name='hotel_api',
                            response={'result': result_hotel}
                        )
                    ))
        if not parts:
            response = self.chat.send_message(user_prompt)
        else:
            response = self.chat.send_message(
                genai.protos.Content(
                    parts=parts
                )
            )
        return response.candidates[0].content.parts[0].text , fcs




