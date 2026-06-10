import asyncio
from agents.orchestrator import orchestrator_agent

async def main():
    user_query = (
        "I want to plan a trip from Agra to Bengaluru departing on 2026-07-01. "
        "I will be returning on 2026-07-07. There are 2 travelers, and we are going on office onsite."
    )
    
    print("🚀 Initializing Multi-Agent Concierge Pipeline...")
    final_package = await orchestrator_agent.run(user_query)
    
    print("\n==============================================")
    print("✨ FINAL CONCIERGE PROPOSAL SUMMARY ✨")
    print("==============================================")
    print(final_package.output)

if __name__ == "__main__":
    asyncio.run(main())