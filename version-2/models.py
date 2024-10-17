from sqlalchemy import Column, Integer, String, Date, Time
from database import Base

class SightingModel(Base):
    __tablename__ = "sightings"

    id = Column(Integer, primary_key=True, index=True)
    species = Column(String, index=True)
    location = Column(String)
    date = Column(Date)
    time = Column(Time)
