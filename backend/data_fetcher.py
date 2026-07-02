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
def plot_financial_trends(ticker: str) -> str:
    """Generates and saves a clean line chart showing total revenue and net income trends over the past 4 years for a given stock ticker symbol."""
    import matplotlib.ticker as mticker

    ticker_data = yf.Ticker(ticker)
    income_stmt = ticker_data.income_stmt

    if income_stmt is None or income_stmt.empty:
        return f"Error: Could not retrieve financial statements for ticker '{ticker}'."

    if "Total Revenue" not in income_stmt.index or "Net Income" not in income_stmt.index:
        return f"Error: Required metrics not found for '{ticker}'."

    total_revenue = income_stmt.loc["Total Revenue"]
    net_income = income_stmt.loc["Net Income"]

    # Sort dates chronologically (oldest to newest)
    total_revenue = total_revenue.sort_index()
    net_income = net_income.sort_index()

    # Format dates to just YYYY-MM-DD string to get rid of timestamps
    dates = [d.strftime('%Y-%m-%d') for d in total_revenue.index]

    # Create figure and primary axis
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot Total Revenue on the Left Y-Axis
    color_rev = '#1f77b4'  # Professional Blue
    ax1.plot(dates, total_revenue, label="Total Revenue", marker='o', color=color_rev, linewidth=2)
    ax1.set_xlabel("Reporting Date", fontweight='bold', labelpad=10)
    ax1.set_ylabel("Total Revenue (USD)", color=color_rev, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=color_rev)

    # Create a secondary Y-axis sharing the same X-axis for Net Income
    ax2 = ax1.twinx()
    color_inc = '#2ca02c'  # Professional Green
    ax2.plot(dates, net_income, label="Net Income", marker='s', color=color_inc, linewidth=2, linestyle='--')
    ax2.set_ylabel("Net Income (USD)", color=color_inc, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor=color_inc)

    # Formatter helper to convert large numbers into human-readable text (Billions/Millions)
    def financial_formatter(x, pos):
        if abs(x) >= 1e9:
            return f"${x * 1e-9:.1f}B"
        elif abs(x) >= 1e6:
            return f"${x * 1e-6:.1f}M"
        else:
            return f"${x:,.0f}"

    # Apply formatters to both Y-axes
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(financial_formatter))
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(financial_formatter))

    # Handle legends from both axes cleanly combined into one box
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

    # General layout adjustments
    plt.title(f"{ticker.upper()} Financial Trends (Past 4 Years)", fontsize=14, fontweight='bold', pad=15)
    ax1.grid(True, linestyle=':', alpha=0.6)

    # Rotate X-axis date labels slightly so they don't hit each other
    fig.autofmt_xdate()

    # Save chart with strict padding constraint to prevent cropped labels
    import os
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(backend_dir, "static")
    os.makedirs(static_dir, exist_ok=True)
    plt.savefig(os.path.join(static_dir, "financial_chart.png"), bbox_inches='tight', dpi=150)
    plt.close(fig)

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



