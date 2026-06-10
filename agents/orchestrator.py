from pydantic_ai import Agent, RunContext
from dto.flights import FlightOption, FlightResponse
from dto.hotels import HotelResponse
from dto.itinerary import FullItinerary
from agents.flight import flight_agent
from agents.itenary import itinerary_agent
from agents.hotel import hotel_agent
import os
import logfire
from dotenv import load_dotenv

load_dotenv()

logfire.configure()

orchestrator_agent = Agent(
    'gemini-3.1-flash-lite',
    system_prompt=(
        "You are the Lead Travel Concierge. Coordinate booking steps cleanly:\n"
        "1. Find flights. Inspect options and select the best fit.\n"
        "2. Crucial: Identify the flight's *arrival_date*. Use this as your hotel check-in date.\n"
        "3. Find hotels for the duration. Choose a valid room category.\n"
        "4. Generate a day-by-day plan.\n"
        "5. Compile everything into a clear, comprehensive summary report for the customer."
    )
)

# This tool belongs to the Orchestrator, allowing it to delegate to the Flight Agent
@orchestrator_agent.tool
async def search_flights(
    ctx: RunContext[None], 
    origin: str, 
    destination: str, 
    travel_date: str
) -> FlightResponse:
    """
    Search for available flights between an origin and destination for a specific date.
    
    Args:
        origin: The departure airport city (e.g., 'Pune').
        destination: The arrival airport city (e.g., 'Tokyo').
        travel_date: The date of travel in YYYY-MM-DD format.
    """
    print(f"\n[Handoff] ✈️ Delegating flight search to Flight Specialist for src: {origin} to dest: {destination} on {travel_date}...")
    
    # Run the sub-agent asynchronously
    result = await flight_agent.run(
        f"Find flights from {origin} to {destination} on {travel_date}"
    )
    print(f"\nresult: {result}")
    
    # Return the validated structured data back to the Orchestrator
    return result.output

@orchestrator_agent.tool
async def search_hotels(ctx: RunContext[None], destination: str, check_in: str, check_out: str, guests: int) -> HotelResponse:
    # 1. The Orchestrator calls the Hotel Agent with strict arguments
    print(f"\n[Handoff] ✈️ Delegating hotel search to hotel Specialist for dest: {destination} to check in: {check_in} and checkout on {check_out} for {guests} guests ....")
    
    res = await hotel_agent.run(
        f"Find hotels in {destination} from {check_in} to {check_out} for {guests} guests"
    )
    # 2. Returns a fully validated HotelResponse object back to the Orchestrator
    return res.output

@orchestrator_agent.tool
async def generate_itinerary(ctx: RunContext[None], destination: str, total_days: int, trip_style: str) -> FullItinerary:
    """Generate a daily sightseeing plan matching a preferred travel vibe."""
    print(f"📡 [Handoff] Orchestrator invoking Itinerary Agent for a {total_days}-day {trip_style} trip...")
    res = await itinerary_agent.run(f"Create a {total_days} day {trip_style} itinerary for {destination}")
    return res.output