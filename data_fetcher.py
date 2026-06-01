from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import yfinance as yf
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

load_dotenv()
plt.clf()
@tool
def plot_financial_trends(ticker:str):
    """Generates and saves a line chart showing the total revenue and net income trends over the past 4 years for a given stock ticker symbol."""
    ticker_data = yf.Ticker(ticker)
    income_stmt = ticker_data.income_stmt
    total_revenue=income_stmt.loc["Total Revenue"]
    net_income=income_stmt.loc["Net Income"]
    dates=total_revenue.index
    plt.plot(dates, total_revenue, label="Total Revenue", marker='o')
    plt.plot(dates, net_income, label="Net Income", marker='s')
    plt.xlabel("Reporting Date")
    plt.ylabel("Value in USD ($)")
    plt.title(f"{ticker} Financial Trends (Past 4 Years)")
    plt.legend()  # This reads the 'label' strings we defined in step 3 and draws a key box
    plt.grid(True)  # Adds gridlines to make it easier to trace values with your eyes
    plt.savefig("static/financial_chart.png", bbox_inches='tight')
    plt.close()
    return "Chart saved successfully as financial_chart.png"

@tool
def get_financial_metrics(ticker: str) -> dict | str:
    """Fetches the most recent total revenue and net income for a given stock market ticker symbol"""
    ticker_data = yf.Ticker(ticker)
    income_stmt = ticker_data.income_stmt
    
    if income_stmt is None or income_stmt.empty:
        return f"Error: Could not retrieve financial statements for ticker '{ticker}'."
        
    if "Total Revenue" not in income_stmt.index or "Net Income" not in income_stmt.index:
        return f"Error: Required metrics (Total Revenue or Net Income) not found for '{ticker}'."
        
    total_revenue = income_stmt.loc["Total Revenue"]
    net_income = income_stmt.loc["Net Income"]
    
    if total_revenue.empty or net_income.empty:
        return f"Error: Financial metrics are empty for ticker '{ticker}'."
        
    result_dict = {
        "revenue": total_revenue.iloc[0],
        "income": net_income.iloc[0]
    }
    return result_dict

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
tools = [get_financial_metrics,plot_financial_trends]

agent_executor = create_agent(
    model, 
    tools=tools, 
    system_prompt="You are a precise financial AI agent."
)



