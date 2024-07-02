from sqlalchemy import Column, Integer, String, Table, ForeignKey, UniqueConstraint, CheckConstraint

from sqlalchemy.orm import relationship, validates

from database import Base

# Association table for service dependencies
service_dependencies = Table('service_dependencies', Base.metadata,
    Column('service_id', Integer, ForeignKey('services.id'), primary_key=True),
    Column('dependent_service_id', Integer, ForeignKey('services.id'), primary_key=True)  ,  
    UniqueConstraint('service_id', 'dependent_service_id', name='unique_service_dependency'),
    CheckConstraint('service_id != dependent_service_id', name='check_no_self_dependency')

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

    tags = relationship('Tag', secondary=service_tags, backref='services')

    # Relationships
    depends_on_services = relationship('Service',
                                       secondary=service_dependencies,
                                       primaryjoin=(service_dependencies.c.service_id == id),
                                       secondaryjoin=(service_dependencies.c.dependent_service_id == id),
                                       backref='dependent_services')
    
    @validates('depends_on_services')
    def validate_no_circular_dependency(self, key, dependent_service):
        if dependent_service.id == self.id:
            raise ValueError("A service cannot depend on itself.")
        if self._has_circular_dependency(dependent_service):
            raise ValueError("Circular dependency detected.")
        return dependent_service
    
    def _has_circular_dependency(self, dependent_service):
        # Simple depth-first search (DFS) to detect a circular dependency
        visited = set()
        stack = [dependent_service]

        while stack:
            current_service = stack.pop()
            if current_service.id == self.id:
                return True
            if current_service.id not in visited:
                visited.add(current_service.id)
                stack.extend(current_service.depends_on_services)

        return False
    
# Tag model
class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __repr__(self):
        return f"<Tag(name='{self.name}')>"
