import datetime as dt

from rumorz_llms.agents.autonomous_agent.rumorz_agent import RumorzAgent
from smartpy.utility import dt_util
from rumorz.client import RumorzClient
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from datetime import datetime, timedelta
import asyncio

rumorz = RumorzClient(api_url="http://localhost:8000")

def get_log_content(log):
    tools_emojis = {
        "AlertUser": "👋",
        "ThinkAndPlan": "🤔",
        "ExecuteOrders": "🪙",
        "UpdateWatchlist": "📋",
        "UpdateMemory": "🧠",
        "Sleep": "😴",
        "GetTokensSocialRanking": "🌐",
        "SearchEntities": "🔍",
        "GetEntitySummaryUpdate": "📊"
    }
    tool_descriptions = {
        "AlertUser": "Alerting user",
        "ThinkAndPlan": "Thinking",
        "ExecuteOrders": "Executing orders",
        "UpdateWatchlist": "Updating watchlist",
        "UpdateMemory": "Updating brain",
        "Sleep": "Sleeping",
        "GetTokensSocialRanking": "Calling the Graph",
        "SearchEntities": "Graph API",
        "GetEntitySummaryUpdate": "Updating entity summary"
    }
    content = None
    match log['tool_name']:
        case 'ThinkAndPlan':
            content = log['arguments']['reasoning']
        case 'ExecuteOrders':
            content = f"Executed order: {log['arguments']['order']}"
        case 'SearchEntities':
            content = f"Searching entities: {log['arguments']}"
        case 'GetTokensSocialRanking':
            arguments = ", ".join([f"{k}: {v}" for k, v in log['arguments'].items()])
            content = f"Fetching Graph ranking by : {arguments}"
        case 'UpdateWatchlist':
            content = f"Updating Feed with: {log['arguments']}"
        case 'UpdateMemory':
            content = f"{log['arguments']['key']} updated to: \n {log['arguments']['value']}"
        case 'Sleep':
            content = f"{log['arguments']['reasoning']}"
        case 'AlertUser':
            content = f"{log['arguments']['message']}"
        case 'GetEntitySummaryUpdate':
            content = f"Entity summary update: {log['arguments']}"

    if content is None:
        print(f"Unknown tool: {log['tool_name']}")
    return {
        "timestamp": log["timestamp"],
        "content": f'<b style="color:white;">[ {tools_emojis.get(log['tool_name'], '🔧')} {tool_descriptions.get(log['tool_name'], "Performing action")} ]</b> {content}'
    }


st.set_page_config(layout="wide")
st_autorefresh(interval=5000, key="data_refresh")

if 'last_agent_refresh_timestamp' not in st.session_state:
    st.session_state.last_agent_refresh_timestamp = (datetime.utcnow() - timedelta(days=19)).isoformat()
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'page' not in st.session_state:
    st.session_state.page = 1

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
    .no-border {
        border: none!important;
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
    <div class="header no-border">
        <img src="https://i.postimg.cc/s2P93CGN/blue-logo-no-text-svg.png" alt="Logo" />
        <div class="info">
            <h1>rumorz.io</h1>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


agent_id='fcbae6ae-acd9-4cfe-8a9e-cfbc1fe669a7'
st.session_state.agent_id = agent_id

if 'agent_id' in st.session_state:
    data = rumorz.agent.get_state(id=st.session_state.agent_id)
    new_logs = rumorz.agent.get_logs(
        id=st.session_state.agent_id,
        from_timestamp=st.session_state.last_agent_refresh_timestamp,
        to_timestamp=datetime.utcnow().isoformat(),
        limit=10,
        page=1
    )
    st.session_state.logs = [get_log_content(log) for log in new_logs] + st.session_state.logs
    st.session_state.last_agent_refresh_timestamp = datetime.utcnow().isoformat()
    
    brain = data['brain']
    short_term_memory = brain.get("short_term_memory", {})
    long_term_memory = brain.get("long_term_memory", {})
    trading_strategy = long_term_memory.get("trading_strategy", "")
    portfolio_summary = brain.get("portfolio_summary", {})
    watch_list = brain.get("watch_list", {}).get("entities", [])
    session_start = brain.get("session_start", "N/A")
    session_duration = brain.get("session_duration", "N/A")
    risk_tolerance = brain.get("risk_tolerance", "N/A")
    initial_goal = brain.get("initial_goal", "N/A")
    name = brain.get("name", "N/A")
    personality = brain.get("personality", "N/A")
    st.markdown(
        f"""
        <div class="header">
            <img src="https://i.postimg.cc/wxbw3H3t/kai-avatar.png" alt="Kai" className="w-12 h-12 rounded-full mr-4" />
            <div class="info">
<h1>{name}</h1>
        <p>Asset class: <span style="color:gray;">Cryptomarkets</span></p>
        <p>Goal: <span style="color:gray;">{initial_goal}</span></p>
        <p>Risk Tolerance: <span style="color:gray;">{risk_tolerance}</span></p>
            </div>
        </div>
        """.format(risk_tolerance),
        unsafe_allow_html=True
    )
    # Add a Divider
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Activity")
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="scrollable-container">', unsafe_allow_html=True)
            for log in st.session_state.logs:
                st.markdown(f'<div class="log-box">{log["content"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        if st.button("Load more"):
            older_logs = rumorz.agent.get_logs(
                agent_id=st.session_state.agent_id,
                from_timestamp=str(dt_util.toDatetime(st.session_state.logs[-1]['timestamp'])-dt.timedelta(days=10)),
                to_timestamp=str(st.session_state.logs[-1]['timestamp']),
                limit=10,
                page=st.session_state.page * 10
            )
            st.session_state.logs.extend([get_log_content(log) for log in older_logs])
            st.session_state.page += 1
            st.rerun()
    with col2:
        tabs = st.tabs(["Market conditions", "Trading strategy","Portfolio", "Tracked entities"])
        with tabs[0]:
            st.markdown("**Short term**")
            st.write(short_term_memory.get("market_conditions", ""))
            st.markdown("**Long term**")
            st.write(long_term_memory.get("market_conditions", ""))
        with tabs[1]:
            st.markdown(trading_strategy)
        with tabs[2]:
            st.subheader("Portfolio Summary")
            st.write(f"Total PnL: {portfolio_summary.get('total_pnl', 0)}")
            st.write("Last 5 Trades:")
            for trade in portfolio_summary.get("last_5_trades", []):
                st.write(trade)
            st.write("PnL by Symbol:")
            for symbol, pnl in portfolio_summary.get("pnl_by_symbol", {}).items():
                st.write(f"{symbol}: {pnl}")
        with tabs[3]:
            for entity in watch_list:
                st.write(entity)

