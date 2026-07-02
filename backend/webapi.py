import os
from data_fetcher import agent_executor
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from  pydantic import BaseModel
import uvicorn
# Get backend directory path
backend_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(backend_dir, "static")
os.makedirs(static_dir, exist_ok=True)

app = FastAPI(title="FinAI Agent API")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

class ChatRequest(BaseModel):
    query: str

@app.post("/analyze")
async def analyze_query(request: ChatRequest):
    chart_path = os.path.join(static_dir, "financial_chart.png")
    if os.path.exists(chart_path):
        os.remove(chart_path)
    result = agent_executor.invoke({"messages": [("user", request.query)]})
    extracted_text = result["messages"][-1].content
    if os.path.exists(chart_path):
        return {
            "status": "success",
            "answer": extracted_text,
            "chart_url": "/static/financial_chart.png"
        }
    else:
        return {
            "status": "success",
            "answer": extracted_text,
            "chart_url": None
        }




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)