1. USER PROMPT: "I have $1500 for a 4-day solo adventure in Tokyo next week."
       │
       ▼
2. ORCHESTRATOR AGENT: Parses constraints (Budget: $1500, Days: 4, Style: Adventure).
       │
       ├─▶ 3. Calls Flight Agent ──▶ Returns: `FlightResult` (Cost: $600)
       │
       ├─▶ 4. Calls Hotel Agent ──▶ Returns: `HotelResult` (Cost: $400)
       │
       │   [Orchestrator calculates: $1500 - $600 - $400 = $500 remaining]
       │
       ├─▶ 5. Calls Itinerary Agent ──▶ Returns: `ItineraryResult` (4-day plan)
       │
       ▼
6. ORCHESTRATOR AGENT: Synthesizes the structured data into a finalized, human-readable Markdown itinerary.
       │
       ▼
7. FINAL OUTPUT TO USER