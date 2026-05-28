# Agentic AI Financial Analyst 📈🤖

An autonomous, multi-tool AI agent built to extract, analyze, and visualize real-time stock market data. 

Unlike standard LLM wrappers, this project utilizes a modern graph-based state machine (LangGraph) to enable an LLM to reason through complex financial queries, autonomously trigger Python-based data pipelines, and formulate human-readable insights.

## Core Architecture
* **The Cognitive Engine:** Google Gemini 2.5 Flash acts as the orchestrator, utilizing LLM Function Calling to decide when external data is required.
* **The Orchestration Loop:** Built with **LangGraph** using the ReAct (Reason + Act) paradigm, moving away from legacy LangChain AgentExecutors for robust state management.
* **The Data Pipeline:** Custom Python tools built on `yfinance` and `pandas` fetch real-time income statements, fortified with production-grade error handling for missing indices or empty DataFrames.
* **The Visualization Layer:** A headless `matplotlib` backend (`Agg`) dynamically generates historical trend charts in memory, completely side-stepping thread-safety issues caused by asynchronous agent loops.

## Tech Stack
* **AI/Orchestration:** LangGraph, LangChain Core, Google Generative AI (Gemini 2.5 Flash)
* **Data Engineering:** yfinance, Pandas
* **Visualization:** Matplotlib (Headless Agg Backend)
* **Environment:** Python 3.10+

## Local Setup
1. Clone the repository: `git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git`
2. Create a virtual environment: `python -m venv .venv`
3. Activate the environment and install dependencies: `pip install -r requirements.txt`
4. Create a `.env` file in the root directory and add your Google API Key: `GOOGLE_API_KEY=your_api_key_here`
5. Run the agent: `python data_fetcher.py`

## Current Capabilities (v1.0-core)
* Fetch real-time total revenue and net income for any ticker.
* Autonomously plot 4-year historical financial trends and save as a local `.png`.
* Gracefully handle invalid ticker symbols and missing API data.
