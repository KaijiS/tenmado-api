from typing import Optional
import datetime

from fastapi import APIRouter, Depends, Query

from schemas.weatherforecast.weatherforecastresponse import WeatherForecastResponse
from services import weatherforecastservice

router = APIRouter()


# @router.get("/", response_model=WeatherForecastResponse)
@router.get("/")
async def get_weather_forcast(
    large_area_code: str = Query(..., alias="largeAreaCode"),
    report_date_from: datetime.date = Query(..., alias="reportDateFrom"),
    report_date_to: datetime.date = Query(..., alias="reportDateTo"),
    report_days: int = Query(..., alias="reportDays"),
):
    # ) -> WeatherForecastResponse:
    """
    天気予報の情報を返す
    """
    return weatherforecastservice.get_weather_forcast(
        large_area_code=large_area_code,
        report_date_from=report_date_from,
        report_date_to=report_date_to,
        report_days=report_days,
    )
