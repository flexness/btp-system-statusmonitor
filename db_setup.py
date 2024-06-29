from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLAlchemy setup
DATABASE_URL = "sqlite:///main.db"
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

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

# Create or update the database schema
def setup_database():
    Base.metadata.create_all(engine)

    # Create initial data
    session = Session()

    # Tags data
    tags_data = [
        Tag(name='SAP'),
        Tag(name='ABAP'),
        Tag(name='SAP HANA'),
        Tag(name='SAP Fiori'),
        Tag(name='Exchange'),
        Tag(name='Citrix'),
        Tag(name='PEPPOL'),
        Tag(name='Custom Interface'),
        Tag(name='API'),
        Tag(name='External Service')
        # Add more tags as needed
    ]
    session.add_all(tags_data)
    session.commit()

    # Services data with dependencies and tags
    service1 = Service(name='Service 1', status='Running', description='Example service 1', endpoint='/api/service1', version='1.0', contact='John Doe')
    service2 = Service(name='Service 2', status='Running', description='Example service 2', endpoint='/api/service2', version='2.0', contact='Jane Smith')
    service3 = Service(name='Service 3', status='Stopped', description='Example service 3', endpoint='/api/service3', version='3.0', contact='Alice Brown')
    service4 = Service(name='Service 4', status='Running', description='Example service 4', endpoint='/api/service4', version='1.5', contact='Bob Green')

    # Setting up multiple dependencies
    service1.depends_on_services.extend([service2, service3])  # Service 1 depends on Service 2 and Service 3
    service2.depends_on_services.append(service4)  # Service 2 depends on Service 4

    # Assigning tags to services
    service1.tags.extend([tags_data[0], tags_data[1]])  # Service 1 tagged with 'SAP' and 'ABAP'
    service2.tags.append(tags_data[8])  # Service 2 tagged with 'API'
    service3.tags.append(tags_data[9])  # Service 3 tagged with 'External Service'

    # Add services to session and commit changes
    session.add_all([service1, service2, service3, service4])
    session.commit()

    session.close()

setup_database()