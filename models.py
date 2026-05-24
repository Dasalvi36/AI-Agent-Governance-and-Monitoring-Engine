from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class AgentAction(Base):
    __tablename__ = "agent_actions"

    id = Column(Integer, primary_key=True, index=True)
    action_type = Column(String, index=True)      # e.g., "read_file", "write_file", "run_command"
    target = Column(String)                       # e.g., "logs.txt", "/etc/passwd"
    allowed = Column(Boolean, default=True)       # True if allowed, False if blocked
    reason = Column(String)                       # Why allowed/blocked
