import requests

class CallableFunction:
    def __init__(self):
        self.serp_api_key = '3628fd5d71fb546e6e4bf3fc637a27ee660143fc1557a57e91291798f57b7679'
    def event_api(self,query: str, htichips: str = "date:today"):
        URL = f"https://serpapi.com/search.json?api_key={self.serp_api_key}&engine=google_events&q={query}&htichips={htichips}&hl=en&gl=us"
        response = requests.get(URL).json()
        return response["events_results"]

    def hotel_api(self,query:str, check_in_date:str, check_out_date:int, hotel_class:int = 3, adults:int = 2):
        URL = f"https://serpapi.com/search.json?api_key={self.serp_api_key}&engine=google_hotels&q={query}&check_in_date={check_in_date}&check_out_date={check_out_date}&adults={int(adults)}&hotel_class={int(hotel_class)}&currency=USD&gl=us&hl=en"
        response = requests.get(URL).json()
        
        return response["properties"]