# app/api/endpoints.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints para Weather
@router.get("/weather/", response_model=List[schemas.WeatherBase])
def read_weather(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    weather_data = db.query(crud.models.Weather).offset(skip).limit(limit).all()
    return weather_data

@router.get("/weather/{weather_id}", response_model=schemas.WeatherBase)
def read_weather_by_id(weather_id: int, db: Session = Depends(get_db)):
    weather = db.query(crud.models.Weather).filter(crud.models.Weather.id == weather_id).first()
    if weather is None:
        raise HTTPException(status_code=404, detail="Dados climáticos não encontrados")
    return weather

@router.get("/weather/city/{city_name}", response_model=List[schemas.WeatherBase])
def read_weather_by_city(city_name: str, db: Session = Depends(get_db)):
    weather_records = db.query(crud.models.Weather).filter(crud.models.Weather.city.ilike(f"%{city_name}%")).all()
    if not weather_records:
        raise HTTPException(status_code=404, detail="Nenhum dado climático encontrado para a cidade especificada")
    return weather_records
