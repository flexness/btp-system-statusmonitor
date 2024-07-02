from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Replace with your actual database URL
DATABASE_URL = "sqlite:///main.db"

# echo=True will print all SQL statements to the console
engine = create_engine(DATABASE_URL, echo=False)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

Base = declarative_base()

def init_db():
    """Create tables if they don't exist."""
    from api.models import Tag 
    from api.models import Service 
    Base.metadata.create_all(engine)
    