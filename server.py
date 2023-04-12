from fastapi import FastAPI
from pydantic import BaseModel
from Salai import PassPromptToSelfBot

class Prompt(BaseModel):
    prompt: str

app = FastAPI()

@app.post("/send_prompt")
async def send_prompt(prompt_data: Prompt):
    prompt = prompt_data.prompt
    response = await PassPromptToSelfBot(prompt)
    return {"message": "Image creation initiated"}

def run_server():
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8269, log_level="info", reload=True)
