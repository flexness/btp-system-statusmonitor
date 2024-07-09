from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# adjust if needed
DATABASE_URL = "sqlite:///main.db"

### SQLAlchemy db setup

# echo=True will print all/tons sql-statements to the console
engine = create_engine(DATABASE_URL, echo=True)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

Base = declarative_base()

# imported in run.py to init DB setup on app startup (if not existing)
def init_db():
    from api.models import Tag 
    from api.models import Service 
    Base.metadata.create_all(engine)
    