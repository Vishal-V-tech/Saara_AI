from dotenv import load_dotenv
import os
from prompt import Instruction_behaviour, Instruction_greeting
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    google,
    noise_cancellation,
)

load_dotenv(".env")


# --- ADD THESE DEBUG LINES ---
google_api_key = os.getenv("GOOGLE_API_KEY")
print(f"GOOGLE_API_KEY loaded: {google_api_key}")
if google_api_key is None:
    print("Warning: GOOGLE_API_KEY is not set!")
# --- END DEBUG LINES ---

class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="You are a helpful voice AI assistant.")


async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
    llm=google.beta.realtime.RealtimeModel(
        model="gemini-2.0-flash-exp",
        voice="Puck",
        temperature=0.8,
        instructions=Instruction_behaviour,
    ),
)
    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            # For telephony applications, use `BVCTelephony` instead for best results
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await session.generate_reply(
        instructions=Instruction_greeting
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))