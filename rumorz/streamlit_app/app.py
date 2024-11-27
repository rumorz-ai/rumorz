import os
from rumorz.client import RumorzClient
import streamlit as st

rumorz = RumorzClient()

data = rumorz.agent.get_state(id='36a5e6ba-160d-45bf-b28a-bea369e0136f')
def get_logs(page, limit=10):
    return rumorz.agent.get_logs(agent_id='36a5e6ba-160d-45bf-b28a-bea369e0136f', page=page, limit=limit)
def get_log_content(log):
    tools_emojis = {
        "AlertUser": "🚨",
        "ThinkAndPlan": "🧠",
        "ExecuteOrders": "💼",
        "UpdateWatchlist": "📋",
        "UpdateMemory": "📝",
        "Sleep": "😴",
        "GetTokensSocialRanking": "🌐",
        "SearchEntities": "🔍",
        "GetEntitySummaryUpdate": "📊"
    }
    tool_descriptions = {
        "AlertUser": "Alerting user",
        "ThinkAndPlan": "Thinking and planning",
        "ExecuteOrders": "Executing orders",
        "UpdateWatchlist": "Updating watchlist",
        "UpdateMemory": "Updating memory",
        "Sleep": "Sleeping",
        "GetTokensSocialRanking": "Calling the Graph",
        "SearchEntities": "Calling the Graph",
        "GetEntitySummaryUpdate": "Updating entity summary"
    }
    match log['tool_name']:
        case 'ThinkAndPlan':
            content = log['arguments']['reasoning']
        case 'ExecuteOrders':
            content = f"Executed order: {log['arguments']['order']}"
        case 'SearchEntities':
            content = f"Searching entities: {log['arguments']}"
        case 'GetTokensSocialRanking':
            arguments = ", ".join([f"{k}: {v}" for k, v in log['arguments'].items()])
            content = f"Graph ranking by : {arguments}"
        case 'UpdateWatchlist':
            content = f"Updated watchlist with: {log['arguments']}"
        case 'UpdateMemory':
            content = f"{log['arguments']['horizon'].replace('_',' ').capitalize()} {log['arguments']['key']}  changed to \n {log['arguments']['value']}"
        case 'Sleep':
            content = f"{log['arguments']['reasoning']}"
        case 'AlertUser':
            content = f"{log['arguments']['message']}"
        case 'GetEntitySummaryUpdate':
            content = f"Entity summary update: {log['arguments']}"
    return {
        "timestamp": log["timestamp"],
        "content": f'<b style="color:white;">[ {tools_emojis.get(log['tool_name'], '🔧')} {tool_descriptions.get(log['tool_name'], "Performing action")} ]</b> {content}'
    }
page = st.session_state.get('page', 1)
logs = [get_log_content(log) for log in get_logs(page)]
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
        margin-top: -50px;
    }
    .header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 20px;
        border: 2px solid #1d222b;
        margin-bottom:30px;
        border-radius: 10px;
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
        border: 1px solid #1d222b;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
        word-wrap: break-word;
        color:gray;
    }
    .divider {
        border-top: 2px solid 1d222b;
        margin: 10px 0;
    }
    .scrollable-container {
        max-height: 400px;
        overflow-y: auto;
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
<h1>Kai <span style="color:gray;">by Rumorz.io</span></h1>
<p>Asset class: <span style="color:gray;">Cryptomarkets</span></p>
<p>Goal: <span style="color:gray;">Trade crypto and generate 100% return per month consistently</span></p>
<p>Risk Tolerance: <span style="color:gray;">{}</span></p>
        </div>
    </div>
    """.format(risk_tolerance),
    unsafe_allow_html=True
)
col1, col2 = st.columns([1, 1])
with col1:
    st.subheader("Activity")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="scrollable-container">', unsafe_allow_html=True)
        for log in logs:
            st.markdown(f'<div class="log-box">{log["content"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    if st.button("Load more"):
        st.session_state.page = page + 1
        st.rerun()
with col2:
    tabs = st.tabs(["Market conditions", "Trading strategy", "Personality", "Portfolio", "Watch list", "Session Details"])
    with tabs[0]:
        st.markdown("**Short term**")
        st.write(short_term_memory.get("market_conditions", ""))
        st.markdown("**Long term**")
        st.write(long_term_memory.get("market_conditions", ""))
    with tabs[1]:
        st.markdown("**Strategy**")
        st.markdown(long_term_memory.get("trading_strategy", ""))
    with tabs[2]:
        st.markdown("**Personality**")
        st.write(personality)
    with tabs[3]:
        st.subheader("Portfolio Summary")
        st.write(f"Total PnL: {portfolio_summary.get('total_pnl', 0)}")
        st.write("Last 5 Trades:")
        for trade in portfolio_summary.get("last_5_trades", []):
            st.write(trade)
        st.write("PnL by Symbol:")
        for symbol, pnl in portfolio_summary.get("pnl_by_symbol", {}).items():
            st.write(f"{symbol}: {pnl}")
    with tabs[4]:
        st.subheader("Watch list")
        for entity in watch_list:
            st.write(entity)
    with tabs[5]:
        st.subheader("Session Details")
        st.write(f"Start: {session_start}")
        st.write(f"Duration: {session_duration}")