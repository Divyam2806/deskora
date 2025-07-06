from sqlalchemy import create_engine, Column, String, Integer, Text, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy import update
from datetime import datetime


# Connect to file-based SQLite database
# create a connection to db
engine = create_engine("sqlite:///assistant_memory.db", echo=False)

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

#  Table 1: User Facts
class UserFact(Base):
    __tablename__ = 'facts'
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)
    value = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

#  Table 2: Preferences (e.g., tone = "casual")
class Preference(Base):
    __tablename__ = 'preferences'
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)
    value = Column(String)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

#  Table 3: Feedback (e.g., “That was too robotic.”)
class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True)
    input = Column(Text)
    response = Column(Text)
    sentiment = Column(String)  # like "positive", "negative", "neutral"
    created_at = Column(DateTime, default=func.now())

# Create the tables if they don't exist
def init_db():
    Base.metadata.create_all(engine)

# helper functions
def set_fact(key: str, value: str):

    # Check if fact exists
    existing = session.query(UserFact).filter_by(key=key).first()

    if existing:
        if existing.value != value:
            existing.value = value
            session.commit()
            print(f"[MEMORY] Updated fact: {key} = {value}")
    else:
        new_fact = UserFact(key=key, value=value)
        session.add(new_fact)
        session.commit()
        print(f"[MEMORY] Set fact: {key} = {value}")

    session.close()

def get_fact(key: str) -> str | None:
    fact = session.query(UserFact).filter_by(key=key).first()
    return fact.value if fact else None

def get_all_facts() -> dict:
    facts = session.query(UserFact).all()
    return {f.key: f.value for f in facts}

