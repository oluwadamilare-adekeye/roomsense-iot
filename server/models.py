from sqlalchemy import Column, Integer, Float, Boolean, DateTime
from datetime import datetime
from database import Base

class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True)
    motion = Column(Boolean, nullable=False, default=False)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)