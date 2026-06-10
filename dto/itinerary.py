from pydantic import BaseModel, Field

class ItineraryDay(BaseModel):
    day_number: int = Field(description="Sequential day number starting from 1")
    activities: list[str] = Field(description="List of planned activities or landmarks")

class FullItinerary(BaseModel):
    destination: str
    trip_style: str = Field(description="Vibe of the trip (e.g., Adventure, Relaxing)")
    days: list[ItineraryDay] = Field(description="Day-by-day breakdown")