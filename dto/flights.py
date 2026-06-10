from pydantic import BaseModel, Field

class FlightOption(BaseModel):
    airline: str = Field(description="Name of the airline")
    flight_number: str = Field(description="Flight identifier code")
    
    # Departure details
    departure_date: str = Field(description="Departure date in YYYY-MM-DD format")
    departure_time: str = Field(description="Local departure time (e.g., 23:15)")
    
    # Arrival details (Crucial for red-eyes!)
    arrival_date: str = Field(description="Arrival date in YYYY-MM-DD format. Note if this is next-day.")
    arrival_time: str = Field(description="Local arrival time at the destination (e.g., 08:30)")
    
    price: float = Field(description="Total price of the flight in INR")

class FlightResponse(BaseModel):
    origin: str
    destination: str
    requested_date: str = Field(description="The date the user originally requested to fly")
    options: list[FlightOption] = Field(description="List of available flight choices")