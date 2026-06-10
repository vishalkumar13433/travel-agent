from pydantic_ai import Agent, RunContext
from datetime import datetime
from data.hotel_mock import HotelResponse
from dotenv import load_dotenv
from tavily import TavilyClient
import os

load_dotenv()
tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

hotel_agent = Agent(
    'gemini-3.1-flash-lite',
    output_type=HotelResponse,
    system_prompt="You are an accommodation specialist. Search and return hotels meeting the date and occupancy limits."
)

hotel_extractor_agent = Agent(
    'gemini-3.1-flash-lite',
    output_type=HotelResponse,
    system_prompt=(
        "You are an expert hospitality data parser. Your task is to extract real-world "
        "hotel availability from raw web search content.\n\n"
        "RULES:\n"
        "1. Identify the hotel names, star ratings, and listed amenities.\n"
        "2. Parse or extrapolate at least 1-2 distinct room choices per hotel (e.g., 'Standard King', 'Deluxe Room').\n"
        "3. Calculate the 'total_stay_price' programmatically based on the nightly rate "
        "   and the requested duration between check-in and check-out dates.\n"
        "4. Strict Data Safety: Ensure all room price metrics are parsed as float values."
    )
)

@hotel_agent.tool
async def fetch_hotels_db(ctx: RunContext[None], destination: str, check_in: str, check_out: str, guests: int) -> HotelResponse:
    """Queries Tavily for live hotel properties, rates, and rooms, filtering by constraints."""
    
    # Calculate stay length for explicit context instruction
    nights = max((datetime.strptime(check_out, "%Y-%m-%d") - datetime.strptime(check_in, "%Y-%m-%d")).days, 1)
    
    # 1. Engineer a specific, trend-seeking search query
    query = f"best hotels in {destination} room types pricing per night {check_in} stay"
    raw_search_data = tavily_client.search(query=query, search_depth="advanced")

    # print(f"\n\n hotel response received from tavily is \n--------------\n {raw_search_data} \n -------------\n")

    print(f"🧠 [Parsing] extracting hotel information...")
    
    # 2. Extract and join raw text components from the search response
    snippets = []
    for result in raw_search_data.get("results", []):
        snippets.append(f"Hotel Source: {result.get('title')} ({result.get('url')})\nData: {result.get('content')}")
    unstructured_context = "\n\n---\n\n".join(snippets)
    
    # 3. Request the extractor agent to clean and build our object
    print(f"🧠 [Parsing] Extractor Agent processing hotel layout maps into schemas...")
    extraction_prompt = (
        f"Context from travel indexes:\n{unstructured_context}\n\n"
        f"Isolate hotels in {destination} accommodating {guests} guests from {check_in} to {check_out} ({nights} nights)."
    )
    
    extraction_result = await hotel_extractor_agent.run(extraction_prompt)
    # 4. Return the fully validated Pydantic object
    resp =  extraction_result.output
    print(f"Hotel response: {resp}")
    
    # 4. Return the fully compliant Pydantic structure to the Orchestrator
    return resp