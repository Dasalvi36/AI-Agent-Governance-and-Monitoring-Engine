from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
from models import AgentAction

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Agent Permission Monitor")

# Pydantic model for incoming actions
class ActionRequest(BaseModel):
    action_type: str  # "read_file", "write_file", "run_command"
    target: str       # file path, command, etc.

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Policy engine
def evaluate_policy(action_type: str, target: str):
    """
    Return (allowed: bool, reason: str)
    """

    # Defining restricted patterns
    restricted_files = ["config.json", "secrets.txt", "/etc/passwd"]
    dangerous_commands = ["rm -rf", "shutdown", "format", "del "]

    # Rule 1: Block writes to restricted files
    if action_type == "write_file":
        for rf in restricted_files:
            if rf in target:
                return False, f"Write to restricted file '{rf}' is not allowed."

    # Rule 2: Block reads of highly sensitive files
    if action_type == "read_file":
        for rf in restricted_files:
            if rf in target:
                return False, f"Read of restricted file '{rf}' is not allowed."

    # Rule 3: Block dangerous commands
    if action_type == "run_command":
        lower_target = target.lower()
        for cmd in dangerous_commands:
            if cmd in lower_target:
                return False, f"Command '{cmd}' is not allowed."

    # Default: allow
    return True, "Action allowed by policy."

@app.post("/action")
def handle_action(request: ActionRequest):
    # Evaluate policy
    allowed, reason = evaluate_policy(request.action_type, request.target)

    # Log to database
    db: Session = next(get_db())
    db_action = AgentAction(
        action_type=request.action_type,
        target=request.target,
        allowed=allowed,
        reason=reason
    )
    db.add(db_action)
    db.commit()
    db.refresh(db_action)

    return {
        "id": db_action.id,
        "allowed": allowed,
        "reason": reason
    }

@app.get("/actions")
def list_actions():
    db: Session = next(get_db())
    actions = db.query(AgentAction).all()
    return [
        {
            "id": a.id,
            "action_type": a.action_type,
            "target": a.target,
            "allowed": a.allowed,
            "reason": a.reason
        }
        for a in actions
    ]
