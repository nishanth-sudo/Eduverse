import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

# Get database URL from environment variable
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create SQLAlchemy engine with SSL requirements
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Enable connection health checks
    pool_size=5,        # Set connection pool size
    max_overflow=10     # Maximum number of connections that can be created beyond pool_size
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for declarative models
Base = declarative_base()

# Define History model
class History(Base):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Create all tables
def init_db():
    Base.metadata.create_all(bind=engine)

# Get database session
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

# Save chat history
def save_history(history_data):
    db = get_db()
    try:
        history = History(
            question=history_data['question'],
            answer=history_data['answer'],
            user_id=history_data['user_id'],
            timestamp=datetime.fromisoformat(history_data['timestamp'])
        )
        db.add(history)
        db.commit()
        db.refresh(history)
        return history
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

# Get user history
def get_user_history(user_id):
    db = get_db()
    try:
        history = db.query(History).filter(History.user_id == str(user_id)).all()
        return [{
            'id': str(h.id),  # Convert ID to string
            'question': h.question,
            'answer': h.answer,
            'user_id': h.user_id,
            'timestamp': h.timestamp.isoformat()
        } for h in history]
    finally:
        db.close()