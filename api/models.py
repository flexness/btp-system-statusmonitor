from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Association table for service dependencies
service_dependencies = Table('service_dependencies', Base.metadata,
    Column('service_id', Integer, ForeignKey('services.id'), primary_key=True),
    Column('dependent_service_id', Integer, ForeignKey('services.id'), primary_key=True)
)

# Association table for service tags
service_tags = Table('service_tags', Base.metadata,
    Column('service_id', Integer, ForeignKey('services.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

# Service model
class Service(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    status = Column(String)
    description = Column(String)
    endpoint = Column(String)
    version = Column(String)
    contact = Column(String)

    # Relationships
    depends_on_services = relationship('Service',
                                       secondary=service_dependencies,
                                       primaryjoin=(service_dependencies.c.service_id == id),
                                       secondaryjoin=(service_dependencies.c.dependent_service_id == id),
                                       backref='dependent_services')

    tags = relationship('Tag', secondary=service_tags, backref='services')

# Tag model
class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __repr__(self):
        return f"<Tag(name='{self.name}')>"

# Example of initializing the database
if __name__ == '__main__':
    from sqlalchemy import create_engine
    DATABASE_URL = "sqlite:///main.db"
    engine = create_engine(DATABASE_URL, echo=True)
    Base.metadata.create_all(engine)