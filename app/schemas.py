# app/schemas.py

from pydantic import BaseModel

class WeatherBase(BaseModel):
    city: str
    region: str
    country: str
    latitude: float
    longitude: float
    temperature: float
    feels_like: float
    humidity: int
    condition_text: str
    condition_icon: str
    wind_speed: float
    wind_degree: int
    wind_dir: str
    pressure_mb: float
    precip_mm: float
    cloud: int
    uv: float
    datetime: str

    class Config:
        from_attributes = True
