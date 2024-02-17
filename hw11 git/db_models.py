from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , declarative_base


engine = create_engine('sqlite:///hw11.db', echo=False)
DBSession = sessionmaker(bind=engine)
session = DBSession()
Base = declarative_base()


class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(100), nullable=True)
    email = Column(String(50), nullable=True)
    phone = Column(String(13), nullable=True)
    birthday = Column(String(10), nullable=True)
    inform = Column(String, nullable=True)


Base.metadata.create_all(engine)
Base.metadata.bind = engine

session.close()
print("Tables created")