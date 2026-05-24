# AI-Agent-Governance-and-Monitoring-Engine

A lightweight, end‑to‑end project demonstrating how to safely monitor and control
AI agent actions using a policy engine, backend API, SQLite logging, and a
Streamlit dashboard.

This project simulates an AI agent attempting actions (read_file, write_file,
run_command, etc.) and evaluates each action against a custom policy engine.
All decisions are logged and visualized in a clean, modern dashboard.

# 1. Project Overview
Modern AI agents can take actions that interact with files, systems, or external
resources. This project demonstrates how to enforce safety by:

• Intercepting every agent action  
• Evaluating it through a policy engine  
• Allowing or blocking the action  
• Logging the result  
• Displaying everything in a real‑time dashboard  

It provides a transparent, auditable view of agent behavior, similar to how
enterprise AI governance systems work.

# 2. System Architecture

The project consists of three components:

1. FastAPI Backend (policy engine + logging)
   - Endpoint: POST /action
   - Validates actions against policy rules
   - Logs all actions to SQLite (actions.db)

2. Simulated Agent
   - Generates random actions
   - Sends them to the backend at:
     http://127.0.0.1:8000/action
   - Receives allow/block decisions

3. Streamlit Dashboard
   - Displays total actions, allowed actions, blocked percentage
   - Shows a detailed table of all logged actions
   - Uses color‑coded badges for clarity

# 3. Features

• Real‑time monitoring of agent behavior  
• Policy‑based allow/block decisions  
• SQLite logging for auditability  
• Clean Streamlit dashboard with:
  - Metrics
  - Colour coded badges

# 4. How to Run the Project

Step 1 — Install dependencies:
    pip install fastapi uvicorn streamlit pandas sqlite3

Step 2 — Start the backend API:
    uvicorn main:app --reload

Step 3 — Run the simulated agent:
    python simulate_agent.py

Step 4 — Launch the dashboard:
    streamlit run dashboard.py

# 5. Policy Engine Logic

The backend enforces simple safety rules such as:

• Block dangerous commands (e.g., "rm -rf /")  
• Block access to restricted files (e.g., secrets.txt, config.json)  
• Allow safe actions (e.g., reading logs, writing output files)

Each decision includes a human‑readable reason.

# 6. Database Schema

SQLite table: agent_actions

Columns:
- id (integer, primary key)
- action_type (text)
- target (text)
- allowed (integer: 1 = allowed, 0 = blocked)
- reason (text)

# 7. Dashboard Preview

The dashboard displays:

• Total Actions  
• Allowed  
• Blocked (%)  
• Recent Agent Actions table  

Each row includes:
- Action type
- Target
- Decision badge (Allowed / Blocked)
- Policy reason

# 8. Future Enhancements
 
• Adding rolebased policy rules  
• Integrating a real LLM agent instead of a simulator  

# Steps to execute this projects

STEP 1 — Activate virtual environment

In **Command Prompt**, run:
venv\Scripts\activate.bat


STEP 2 — Starting the FastAPI backend

Run:
uvicorn main:app --reload

This starts the API at:

http://127.0.0.1:8000

STEP 3 — Running the simulated agent

Open a **second terminal**, activate venv again:
venv\Scripts\activate.bat

Then run:
python simulate_agent.py

This will start sending actions to the backend.

STEP 4 — Starting the Streamlit dashboard

Open a **third terminal**, activate venv again:
venv\Scripts\activate.bat

Then run:
streamlit run dashboard.py

The dashboard will open at:
http://localhost:8501

# Output
<img width="2046" height="1213" alt="image" src="https://github.com/user-attachments/assets/8eb56196-abe8-4fdd-a19d-ed3e7a538ae8" />
