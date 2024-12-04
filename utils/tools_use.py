import google.generativeai as genai

def event_api(query: str, htichips: str = "date:today"):
    URL = f"https://serpapi.com/search.json?api_key={SERP_API_KEY}&engine=google_events&q={query}&htichips={htichips}&hl=en&gl=us"
    response = requests.get(URL).json()
    return response["events_results"]

def hotel_api(query:str, check_in_date:str, check_out_date:int, hotel_class:int = 3, adults:int = 2):
    URL = f"https://serpapi.com/search.json?api_key={SERP_API_KEY}&engine=google_hotels&q={query}&check_in_date={check_in_date}&check_out_date={check_out_date}&adults={int(adults)}&hotel_class={int(hotel_class)}&currency=USD&gl=us&hl=en"
    response = requests.get(URL).json()
    
    return response["properties"]


class ToolsUse:
    def __init__(self):
        self.tools = genai.protos.Tool(
        function_declarations=[
            genai.protos.FunctionDeclaration(
                name="event_api",
                description="Retrieves event information based on a query and optional filters.",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "query": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="The query you want to search for (e.g., 'Events in Austin, TX')."
                        ),
                        "htichips": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="""Optional filters used for search. Default: 'date:today'.
                            
                            Options:
                            - 'date:today' - Today's events
                            - 'date:tomorrow' - Tomorrow's events
                            - 'date:week' - This week's events
                            - 'date:weekend' - This weekend's events
                            - 'date:next_week' - Next week's events
                            - 'date:month' - This month's events
                            - 'date:next_month' - Next month's events
                            - 'event_type:Virtual-Event' - Online events
                            """
                        )
                    },
                    required=["query"]
                )
            ),
            genai.protos.FunctionDeclaration(
                name="hotel_api",
                description="Retrieves hotel information based on location, dates, and optional preferences.",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "query": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Parameter defines the search query. You can use anything that you would use in a regular Google Hotels search."
                        ),
                        "check_in_date": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Check-in date in YYYY-MM-DD format (e.g., '2024-04-30')."
                        ),
                        "check_out_date": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Check-out date in YYYY-MM-DD format (e.g., '2024-05-01')."
                        ),
                        "hotel_class": genai.protos.Schema(
                            type=genai.protos.Type.INTEGER,
                            description="""Hotel class.

                            Options:
                            - 2: 2-star
                            - 3: 3-star
                            - 4: 4-star
                            - 5: 5-star
                            
                            For multiple classes, separate with commas (e.g., '2,3,4')."""
                        ),
                        "adults": genai.protos.Schema(
                            type=genai.protos.Type.INTEGER,
                            description="Number of adults. Only integers, no decimals or floats (e.g., 1 or 2)."
                        )
                    },
                    required=["query", "check_in_date", "check_out_date"]
                )
            )
        ]
    )