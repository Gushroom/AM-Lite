from sqlalchemy import create_engine, Column, Integer, String, DateTime, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone
import os

engine = create_engine('sqlite:///db/am_lite.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class LLMApi(Base):
    __tablename__ = 'llm_apis'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    _api_key = Column("api_key", String, nullable=False)
    api_type = Column(String, nullable=False)  # e.g., "OpenAI", "Claude", etc.
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    last_used_at = Column(DateTime, nullable=True)
    is_active = Column(Integer, default=True)
    

class RPATask(Base):
    __tablename__ = 'rpa_tasks'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(TEXT)
    workspace_dir = Column(String, nullable=False)  # Directory where task files are stored
    code_entry_point = Column(String, nullable=False)  # Main file to execute
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    last_run_at = Column(DateTime, default=None)
    interval = Column(Integer, nullable=False)  # Interval in minutes
    status = Column(String, default="idle")  # Task status
    log_file = Column(String, nullable=True)  # Path to the task log file

Base.metadata.create_all(engine)
