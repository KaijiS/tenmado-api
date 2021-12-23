import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class Forecast(BaseModel):

    forecast_target_date: datetime.date = Field(
        ..., description="予報対象日", alias="forecastTargetDate", example="2021-01-02"
    )
    weather: str = Field(..., description="天気", alias="weather", example="晴れのち雨")
    pop: str = Field(..., description="降水確率", alias="pop", example="0/20/60/80")
    reliability: Optional[str] = Field(
        ..., description="信頼度", alias="reliability", example="A"
    )
    lowest_temperature: float = Field(
        ..., description="最低気温", alias="lowestTemperature", example="12.1"
    )
    lowest_temperature_lower: Optional[float] = Field(
        ..., description="最低気温下限", alias="lowestTemperatureLower", example="10.5"
    )
    lowest_temperature_upper: Optional[float] = Field(
        ..., description="最低気温上限", alias="lowestTemperatureUpper", example="13.1"
    )
    highest_temperature: float = Field(
        ..., description="最高気温", alias="highestTemperature", example="16.1"
    )
    highest_temperature_lower: Optional[float] = Field(
        ..., description="最高気温下限", alias="highestTemperatureLower", example="17.5"
    )
    highest_temperature_upper: Optional[float] = Field(
        ..., description="最高気温上限", alias="highestTemperatureUpper", example="15.1"
    )

    class Config:
        allow_population_by_field_name = True
