from typing import Optional
import datetime

from fastapi import APIRouter, Depends, Query

from schemas.weatherforecast.weatherforecastresponse import WeatherForecastResponse

router = APIRouter()


@router.get("/", response_model=WeatherForecastResponse)
async def get_weather_forcast(
    larage_area_code: str = Query(..., alias="largeAreaCode"),
    report_date_from: datetime.date = Query(..., alias="reportDateFrom"),
    report_date_to: datetime.date = Query(..., alias="reportDateTo"),
    report_days: int = Query(..., alias="reportDays"),
) -> WeatherForecastResponse:
    """
    天気予報の情報を返す
    """
    weatherforecastresponse = WeatherForecastResponse()
    return weatherforecastresponse
