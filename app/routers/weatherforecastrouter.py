from typing import Optional
import datetime

from fastapi import APIRouter, Depends, Query

from schemas.weatherforecast.weatherforecastresponse import WeatherForecastResponse
from schemas.weatherforecast.startdateresponse import StartDateResponse
from services import weatherforecastservice

router = APIRouter()


@router.get("/", response_model=WeatherForecastResponse)
async def get_weather_forcast(
    large_area_code: str = Query(..., alias="largeAreaCode"),
    report_date_from: datetime.date = Query(..., alias="reportDateFrom"),
    report_date_to: datetime.date = Query(..., alias="reportDateTo"),
    forecastdays: int = Query(..., alias="forecastdays"),
) -> WeatherForecastResponse:
    """
    天気予報の情報を返す
    """
    return weatherforecastservice.get_weather_forcast(
        large_area_code=large_area_code,
        report_date_from=report_date_from,
        report_date_to=report_date_to,
        forecastdays=forecastdays,
    )


@router.get("/startdate", response_model=StartDateResponse)
async def get_weather_forcast() -> StartDateResponse:
    """
    天気予報の取得開始日を返す
    """
    return weatherforecastservice.get_start_date()
