# app/crud.py

from sqlalchemy.orm import Session
from app import models

def get_weather_by_city_and_datetime(db: Session, city: str, datetime_str: str):
    return db.query(models.Weather).filter(
        models.Weather.city == city,
        models.Weather.datetime == datetime_str
    ).first()

def create_weather(db: Session, weather: dict):
    db_weather = models.Weather(**weather)
    db.add(db_weather)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    db.refresh(db_weather)
    return db_weather
