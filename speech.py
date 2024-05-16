from fastapi import FastAPI
from langchain_openai import ChatOpenAI

app = FastAPI(
    title="Langchain Server",
    version="1.0",
    description="A simple API Server"
)

llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key="YOUR_OPEN_AI_KEY")

@app.post("/voice_assistant")
async def voice_assistant(text: str, query: str = ""):
    # You can add your logic here to process the text and query
    # Example:
    response = llm.ask(question=text, messages=[("system", "System's role"), ("human", "Give Your Requirement")])
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8002)








