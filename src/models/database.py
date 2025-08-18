"""
Optional database models for storing investigation results
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class Investigation(Base):
    """Database model for scientific investigations"""
    __tablename__ = "investigations"
    
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    domain = Column(String(50))
    hypothesis_statement = Column(Text)
    hypothesis_confidence = Column(Float)
    mathematical_model = Column(Text)
    experiment_parameters = Column(JSON)
    experimental_results = Column(JSON)
    supports_hypothesis = Column(Boolean)
    final_conclusion = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    execution_time = Column(Float)  # seconds

class AgentPerformance(Base):
    """Database model for agent performance metrics"""
    __tablename__ = "agent_performance"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String(50), nullable=False)
    operation = Column(String(100), nullable=False)
    execution_time = Column(Float)
    memory_usage = Column(Float)
    success = Column(Boolean)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Database utility functions
def create_database():
    """Create database tables"""
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./scientific_investigations.db")
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    return engine

def get_session():
    """Get database session"""
    engine = create_database()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()