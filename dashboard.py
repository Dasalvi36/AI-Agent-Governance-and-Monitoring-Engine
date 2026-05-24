import sqlite3
import pandas as pd
import streamlit as st


st.markdown("""
<style>
    /* Hide Streamlit hamburger menu */
    #MainMenu {visibility: hidden;}

    /* Hide Streamlit header */
    header {visibility: hidden;}

    /* Hide Streamlit footer (optional) */
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


st.set_page_config(page_title="AI Agent Governance & Monitoring Engine", layout="wide")

st.markdown("""
<style>

    /* Force Streamlit into TRUE light mode */
    :root, html, body, .stApp {
        color-scheme: light !important;
        background-color: white !important;
        color: black !important;
    }

    /* Reset ALL text to black */
    *, div, span, p, label, h1, h2, h3, h4, h5, h6 {
        color: black !important;
    }

    /* Fix metric cards (no more long bars) */
    .stMetric {
        background-color: #f8f9fa !important;
        padding: 16px !important;
        border-radius: 10px !important;
        border: 1px solid #ddd !important;
        text-align: center !important;
        width: 100% !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
    }

    /* Fix table borders */
    table, th, td {
        border: 1px solid #ccc !important;
        border-collapse: collapse !important;
        padding: 6px !important;
        color: black !important;
    }

    /* Badge styling */
    .badge-allowed {
        background-color: #d4edda;
        color: #155724;
        padding: 4px 8px;
        border-radius: 6px;
        font-weight: 600;
    }
    .badge-blocked {
        background-color: #f8d7da;
        color: #721c24;
        padding: 4px 8px;
        border-radius: 6px;
        font-weight: 600;
    }

</style>
""", unsafe_allow_html=True)

# LOAD DATA

def load_logs():
    conn = sqlite3.connect("actions.db")
    try:
        df = pd.read_sql_query(
            "SELECT id, action_type, target, allowed, reason FROM agent_actions ORDER BY id DESC",
            conn
        )
    except:
        df = pd.DataFrame(columns=["id", "action_type", "target", "allowed", "reason"])
    conn.close()
    return df

df = load_logs()

# TABLE
st.set_page_config(page_title="AI Agent Governance & Monitoring Engine", layout="wide")

st.markdown("""
<style>

    /* Force Streamlit into TRUE light mode */
    :root, html, body, .stApp {
        color-scheme: light !important;
        background-color: white !important;
        color: black !important;
    }

    /* Reset ALL text to black */
    *, div, span, p, label, h1, h2, h3, h4, h5, h6 {
        color: black !important;
    }

    /* Fix metric cards (no more long bars) */
    .stMetric {
        background-color: #f8f9fa !important;
        padding: 16px !important;
        border-radius: 10px !important;
        border: 1px solid #ddd !important;
        text-align: center !important;
        width: 100% !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
    }

    /* Fix table borders */
    table, th, td {
        border: 1px solid #ccc !important;
        border-collapse: collapse !important;
        padding: 6px !important;
        color: black !important;
    }

    /* Badge styling */
    .badge-allowed {
        background-color: #d4edda;
        color: #155724;
        padding: 4px 8px;
        border-radius: 6px;
        font-weight: 600;
    }
    .badge-blocked {
        background-color: #f8d7da;
        color: #721c24;
        padding: 4px 8px;
        border-radius: 6px;
        font-weight: 600;
    }

</style>
""", unsafe_allow_html=True)

# TITLE
st.title("AI Agent Governance & Monitoring Engine")
st.markdown("Monitor what your agent is trying to do and how the policy engine responds.")


# LOAD DATA
def load_logs():
    conn = sqlite3.connect("actions.db")
    try:
        df = pd.read_sql_query(
            "SELECT id, action_type, target, allowed, reason FROM agent_actions ORDER BY id DESC",
            conn
        )
    except:
        df = pd.DataFrame(columns=["id", "action_type", "target", "allowed", "reason"])
    conn.close()
    return df

df = load_logs()

# METRICS
col1, col2, col3 = st.columns(3)

total = len(df)
allowed = int((df["allowed"] == 1).sum()) if total else 0
blocked = int((df["allowed"] == 0).sum()) if total else 0
blocked_pct = round((blocked / total) * 100, 1) if total else 0

col1.metric("Total Actions", total)
col2.metric("Allowed", allowed)
col3.metric("Blocked (%)", f"{blocked_pct}%")

#st.markdown("---")

# TABLE

st.subheader("Recent Agent Actions")

if df.empty:
    st.info("No actions logged yet.")
else:
    # Add decision badges
    df["decision"] = df["allowed"].apply(
        lambda x: "<span class='badge-allowed'>Allowed</span>"
        if x else "<span class='badge-blocked'>Blocked</span>"
    )

    df_display = df[["id", "action_type", "target", "decision", "reason"]].rename(
        columns={
            "id": "ID",
            "action_type": "Action Type",
            "target": "Target",
            "decision": "Decision",
            "reason": "Policy Reason"
        }
    )

    st.write(df_display.to_html(escape=False, index=False), unsafe_allow_html=True)
