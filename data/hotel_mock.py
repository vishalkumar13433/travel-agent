from datetime import datetime
from dto.hotels import HotelOption, HotelResponse, RoomOption

# Expanded mock inventory with multiple room types
MOCK_HOTEL_INVENTORY = {
    "TOKYO": {
        "name": "Shinjuku Granbell Hotel",
        "star_rating": 4,
        "amenities": ["Free Wi-Fi", "Rooftop Bar", "Metro Access"],
        "rooms": [
            {"room_type": "Standard Queen", "max_occupancy": 2, "price_per_night": 150.0, "description": "1 Queen bed, city view"},
            {"room_type": "Executive Suite", "max_occupancy": 4, "price_per_night": 350.0, "description": "2 King beds, separate living area"}
        ]
    },
    "GOA": {
        "name": "Taj Exotica Resort & Spa",
        "star_rating": 5,
        "amenities": ["Private Beach", "Golf Course", "Spa"],
        "rooms": [
            {"room_type": "Luxury Room Garden View", "max_occupancy": 3, "price_per_night": 220.0, "description": "1 King bed + 1 rollaway bed available"},
            {"room_type": "Plunge Pool Villa", "max_occupancy": 4, "price_per_night": 550.0, "description": "Private villa with dedicated plunge pool"}
        ]
    }
}

def mock_fetch_hotels(destination: str, check_in: str, check_out: str, guests: int) -> HotelResponse:
    """Queries hotel inventory, filters by occupancy, and calculates total stay costs."""
    dest_key = destination.upper()
    
    # Calculate total nights stayed
    date_format = "%Y-%m-%d"
    d1 = datetime.strptime(check_in, date_format)
    d2 = datetime.strptime(check_out, date_format)
    nights = (d2 - d1).days
    if nights <= 0:
        nights = 1 # Fallback edge case guard
        
    hotel_options = []
    
    # If destination matches our mock database
    if dest_key in MOCK_HOTEL_INVENTORY:
        data = MOCK_HOTEL_INVENTORY[dest_key]
        valid_rooms = []
        
        # Filter and construct rooms that fit the guest count
        for r in data["rooms"]:
            if r["max_occupancy"] >= guests:
                valid_rooms.append(RoomOption(
                    room_type=r["room_type"],
                    max_occupancy=r["max_occupancy"],
                    price_per_night=r["price_per_night"],
                    total_stay_price=r["price_per_night"] * nights,
                    description=r["description"]
                ))
        
        # Only add the hotel if it has rooms that can fit this party size
        if valid_rooms:
            hotel_options.append(HotelOption(
                name=data["name"],
                star_rating=data["star_rating"],
                amenities=data["amenities"],
                available_rooms=valid_rooms
            ))
    else:
        # Generic fallback option if user picks somewhere else
        hotel_options.append(HotelOption(
            name="Standard Global Inn",
            star_rating=3,
            amenities=["Free Wi-Fi"],
            available_rooms=[RoomOption(
                room_type="Standard Double",
                max_occupancy=4,
                price_per_night=100.0,
                total_stay_price=100.0 * nights,
                description="2 Double beds"
            )]
        ))
        
    return HotelResponse(
        destination=destination,
        check_in_date=check_in,
        check_out_date=check_out,
        number_of_guests=guests,
        options=hotel_options
    )