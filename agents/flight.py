from pydantic_ai import Agent, RunContext
from data.flight_mock import FlightResponse
from dotenv import load_dotenv
from tavily import TavilyClient
import os

load_dotenv()
tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

flight_agent = Agent(
    'gemini-3.1-flash-lite',
    output_type=FlightResponse, # Forces agent to return exactly this structure
    system_prompt=(
        "You are an expert flight routing agent. Your job is to "
        "find flightusing the requested parameters and return the available options. "
        "Do not alter the prices or flight details"
    )
)

flight_extractor_agent = Agent(
    'gemini-3.1-flash-lite', 
    output_type=FlightResponse,
    system_prompt=(
        "You are an advanced data extraction utility. Your sole job is to read messy, "
        "unstructured web search results and map them cleanly into the required FlightResponse schema.\n\n"
        "CRITICAL RULES:\n"
        "1. Extract exact flight numbers and airline names. If a flight number isn't found, "
        "   synthesize a predictable one based on the airline (e.g., AI-UNKNOWN).\n"
        "2. Parse dates strictly into YYYY-MM-DD. Look closely at departure times; if a flight departs "
        "   late at night (e.g., 11:15 PM) and has a long duration, compute the arrival_date as the NEXT day.\n"
        "3. Convert all prices to floats (e.g., 'Rs 620' becomes 620.0). If a price is missing, skip that option."
    )
)
@flight_agent.tool
async def fetch_flights_from_db(ctx: RunContext[None], origin: str, destination: str, travel_date: str) -> FlightResponse:
    # query = f"flights from {origin} to {destination} on {travel_date} with prices and departure and arrival time in IST. Include only 1 flight with the asked info. Prefer non stop over layover flights."

    query = f"{origin} {destination} flight schedule timetable flight number departure arrival price"
    print(f"🌐 [Web Search] Querying Tavily: '{query}'...")

    response = tavily_client.search(query=query, search_depth="basic")
    # print(f"\n\n response received from tavily is \n--------------\n {response} \n -------------\n")

    print(f"🧠 [Parsing] extracting flight information...")
    extraction_prompt = (
        f"Context from the web:\n{response} to extract flight info \n\n"
    )
    
    extraction_result = await flight_extractor_agent.run(extraction_prompt)
    
    # 4. Return the fully validated Pydantic object
    resp =  extraction_result.output
    print(f"Flight response: {resp}")
    return resp