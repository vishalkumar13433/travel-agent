from pydantic import BaseModel, Field

class RoomOption(BaseModel):
    room_type: str = Field(description="Type of room (e.g., Standard King, Deluxe Suite, Ocean View)")
    max_occupancy: int = Field(description="Maximum number of guests allowed in this room")
    price_per_night: float = Field(description="Cost per night for this room tier in INR")
    total_stay_price: float = Field(description="Total cost for the entire date range in INR")
    description: str = Field(description="Brief text detailing bed types or views")

class HotelOption(BaseModel):
    name: str = Field(description="Name of the hotel property")
    star_rating: int = Field(description="Star rating from 1 to 5")
    amenities: list[str] = Field(description="Top amenities provided by the hotel")
    available_rooms: list[RoomOption] = Field(description="List of rooms that can accommodate the guest count")

class HotelResponse(BaseModel):
    destination: str = Field(description="City or region searched")
    check_in_date: str = Field(description="Check-in date in YYYY-MM-DD format")
    check_out_date: str = Field(description="Check-out date in YYYY-MM-DD format")
    number_of_guests: int = Field(description="Total number of people traveling")
    options: list[HotelOption] = Field(description="List of available hotels matching criteria")