# Agentic AI Financial Analyst 📈🤖

An autonomous, multi-tool AI agent built to extract, analyze, and visualize real-time stock market data. 

This project utilizes a ReAct (Reason + Act) state machine to enable an LLM to reason through complex financial queries, autonomously trigger Python-based data pipelines, and serve human-readable insights through a decoupled web interface.

## Core Architecture
* **The Cognitive Engine:** Google Gemini 2.5 Flash acts as the orchestrator, utilizing strict LLM Function Calling to decide when external data is required.
* **The Orchestration Loop:** Built with core **LangChain Agents** (`create_agent`), the system loops through thoughts, actions, and observations to dynamically route requests to the correct Python tools.
* **The Data Pipeline:** Custom Python tools built on `yfinance` and `pandas` fetch real-time income statements, fortified with production-grade error handling for missing indices or empty DataFrames.
* **The Visualization Layer:** A headless `matplotlib` backend (`Agg`) dynamically generates historical trend charts in memory, completely side-stepping thread-safety issues caused by asynchronous background threads.
* **The Decoupled Web Layer:** A **FastAPI** REST microservice manages state (cleaning up old chart files) and exposes the agent's logic to the web, while a **Streamlit** client provides a responsive, interactive chat UI.

## Tech Stack
* **AI/Orchestration:** LangChain Core, Google Generative AI (Gemini 2.5 Flash)
* **Backend Web Server:** FastAPI, Uvicorn, Pydantic
* **Frontend Client:** Streamlit, Requests
* **Data Engineering & Visualization:** yfinance, Pandas, Matplotlib (Headless Agg)
* **Environment:** Python 3.10+

## Local Setup
1. Clone the repository: `git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git`
2. Create a virtual environment: `python -m venv .venv`
3. Activate the environment and install dependencies: `pip install -r requirements.txt`
4. Create an empty `static/` folder in the root directory to store generated charts.
5. Create a `.env` file in the root directory and add your Google API Key: `GOOGLE_API_KEY=your_api_key_here`

## Running the Application
Because this is a decoupled architecture, you must run the backend and frontend simultaneously in separate terminals.

**Terminal 1 (Backend):**
```bash

python webapi.py 

**Terminal 1 (Frontend):**
```bash
streamlit run stapp.py