from pydantic_ai import Agent
from dto.itinerary import FullItinerary
from dotenv import load_dotenv

load_dotenv()

itinerary_agent = Agent(
    'gemini-3.1-flash-lite',
    output_type=FullItinerary,
    system_prompt="You are a local tour guide. Build a detailed, day-by-day list of activities reflecting the chosen travel vibe."
)