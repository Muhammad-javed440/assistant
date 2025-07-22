import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Initialize FastAPI app
app = FastAPI()

# Allow frontend origins (adjust for your frontend deployment)
origins = [
    "http://localhost:3000",                # Local dev
    "https://code-wave-44.vercel.app",      # Deployed frontend
]

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Step 1: Provider
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Step 2: Model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider,
)

# Step 3: Endpoint
@app.post("/run-agent")
async def run_agent(request: Request):
    data = await request.json()
    user_input = data.get("message", "")

    agent = Agent(name="AI Assistant", instructions="You are a helpful assistant and help users with their queries in all fields.", model=model)
    result = await Runner.run(agent, user_input)

    return {"output": result.final_output}


# Step 4: Run the app with correct port (for Railway/Render/Vercel)
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))  # Railway/Render will set PORT env
    uvicorn.run("main:app", host="0.0.0.0", port=port)
