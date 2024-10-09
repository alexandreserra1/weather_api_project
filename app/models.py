# app/models.py

from sqlalchemy import Column, Integer, String, Float, UniqueConstraint
from app.database import Base

class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    region = Column(String)
    country = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    temperature = Column(Float)
    feels_like = Column(Float)
    humidity = Column(Integer)
    condition_text = Column(String)
    condition_icon = Column(String)
    wind_speed = Column(Float)
    wind_degree = Column(Integer)
    wind_dir = Column(String)
    pressure_mb = Column(Float)
    precip_mm = Column(Float)
    cloud = Column(Integer)
    uv = Column(Float)
    datetime = Column(String, index=True)

    __table_args__ = (
        UniqueConstraint('city', 'datetime', name='_city_datetime_uc'),
    )
