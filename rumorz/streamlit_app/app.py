import os
import streamlit as st
from rumorz.client import RumorzClient

rumorz = RumorzClient(api_key=os.environ['RUMORZ_API_KEY'], api_url='http://localhost:8000')
data = rumorz.agent.get_state(id='36a5e6ba-160d-45bf-b28a-bea369e0136f')
logs = rumorz.agent.get_logs(agent_id='36a5e6ba-160d-45bf-b28a-bea369e0136f', page=1, limit=10)

def get_log_content(log):
    if log['tool_name'] == 'ThinkAndPlan':
        return log['arguments']['reasoning']
    elif log['tool_name'] == 'ExecuteOrders':
        return f"Executed order: {log['arguments']['order']}"

logs = [get_log_content(log) for log in logs]






short_term_memory = data.get("short_term_memory", {})
long_term_memory = data.get("long_term_memory", {})
portfolio_summary = data.get("portfolio_summary", {})
watch_list = data.get("watch_list", {}).get("entities", [])
personality = data.get("personality", "N/A")
session_start = data.get("session_start", "N/A")
session_duration = data.get("session_duration", "N/A")
risk_tolerance = data.get("risk_tolerance", "N/A")

st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
    body {
        background-color: black;
        color: gray;
    }
    .header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 0;
    }
    .header img {
        border-radius: 50%;
        width: 80px;
        height: 80px;
    }
    .header .info {
        flex-grow: 1;
        margin-left: 20px;
    }
    .header .info h1 {
        margin: 0;
        font-size: 24px;
        color: white;
    }
    .header .info p {
        margin: 5px 0;
        font-size: 16px;
    }
    h1, h2, h3, h4, h5, h6 {
        color: white;
    }
    .log-box {
        border: 1px solid gray;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
        word-wrap: break-word;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="header">
        <img src="https://i.postimg.cc/wxbw3H3t/kai-avatar.png" alt="Kai" className="w-12 h-12 rounded-full mr-4" />
        <div class="info">
            <h1>Kai</h1>
            <p>Asset class: Cryptomarkets</p>
            <p>Goal: Trade crypto and generate 100% return per month consistently</p>
            <p>Risk Tolerance: {}</p>
        </div>
    </div>
    """.format(risk_tolerance),
    unsafe_allow_html=True
)

col1, col2 = st.columns([1, 2])

with col1:
    st.header("Logs")
    for log in logs:
        st.markdown(f'<div class="log-box">{log["content"]}</div>', unsafe_allow_html=True)

with col2:
    tabs = st.tabs(["Memory", "Portfolio", "Watch list", "Personality", "Session Details", "Risk Tolerance"])
    with tabs[0]:
        st.subheader("Short term")
        st.write(short_term_memory.get("notes", ""))
        st.subheader("Market Conditions")
        st.write(short_term_memory.get("market_conditions", ""))
        st.subheader("Long term")
        st.write(long_term_memory.get("notes", ""))
        st.subheader("Trading Strategy")
        st.write(long_term_memory.get("trading_strategy", ""))
        st.subheader("Market Conditions")
        st.write(long_term_memory.get("market_conditions", ""))
    with tabs[1]:
        st.subheader("Portfolio Summary")
        st.write(f"Total PnL: {portfolio_summary.get('total_pnl', 0)}")
        st.write("Last 5 Trades:")
        for trade in portfolio_summary.get("last_5_trades", []):
            st.write(trade)
        st.write("PnL by Symbol:")
        for symbol, pnl in portfolio_summary.get("pnl_by_symbol", {}).items():
            st.write(f"{symbol}: {pnl}")
    with tabs[2]:
        st.subheader("Watch list")
        for entity in watch_list:
            st.write(entity)
    with tabs[3]:
        st.subheader("Personality")
        st.write(personality)
    with tabs[4]:
        st.subheader("Session Details")
        st.write(f"Start: {session_start}")
        st.write(f"Duration: {session_duration}")