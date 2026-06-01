from data_fetcher import agent_executor
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from  pydantic import BaseModel
import uvicorn
app=FastAPI(title="FinAI Agent API")
app.mount("/static", StaticFiles(directory="static"), name="static")
class ChatRequest(BaseModel):
    query: str
@app.post("/analyze")
async def analyze_query(request: ChatRequest):
    result = agent_executor.invoke({"messages": [("user", request.query)]})
    extracted_text = result["messages"][-1].content

    return {"status": "success",
        "answer": extracted_text,
        "chart_url": "http://localhost:8000/static/financial_chart.png"}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)