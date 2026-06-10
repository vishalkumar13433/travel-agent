from datetime import datetime, timedelta
from dto.flights import FlightOption, FlightResponse

def mock_fetch_flights(origin: str, destination: str, travel_date: str) -> FlightResponse:
    """Simulates querying a flight engine with accurate next-day arrival logic."""
    dest_key = destination.upper()
    
    # Let's calculate the "next day" date string for overnight flights
    current_date_obj = datetime.strptime(travel_date, "%Y-%m-%d")
    next_day_obj = current_date_obj + timedelta(days=1)
    next_day_str = next_day_obj.strftime("%Y-%m-%d")
    
    options = []
    
    if dest_key == "TOKYO":
        # Option 1: Same day arrival
        options.append(FlightOption(
            airline="Japan Airlines",
            flight_number="JL-708",
            departure_date=travel_date,
            departure_time="08:30 AM",
            arrival_date=travel_date, 
            arrival_time="04:15 PM",
            price=850.0
        ))
        # Option 2: OVERNIGHT FLIGHT (Lands the next day)
        options.append(FlightOption(
            airline="Air India",
            flight_number="AI-306",
            departure_date=travel_date,
            departure_time="11:15 PM",
            arrival_date=next_day_str,  # <--- Crucial: Lands +1 day!
            arrival_time="08:30 AM",
            price=620.0
        ))
    else:
        # Default fallback (Goa, etc. - usually same day)
        options.append(FlightOption(
            airline="IndiGo",
            flight_number="6E-2034",
            departure_date=travel_date,
            departure_time="06:00 AM",
            arrival_date=travel_date,
            arrival_time="08:45 AM",
            price=120.0
        ))
        
    return FlightResponse(origin=origin, destination=destination, requested_date=travel_date, options=options)