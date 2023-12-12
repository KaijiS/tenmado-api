import datetime

from fastapi import APIRouter, Query
from schemas.weatherforecast.kubun import Kubun
from schemas.weatherforecast.largearea import LargeArea
from schemas.weatherforecast.startdate import StartDate
from schemas.weatherforecast.weatherforecast import WeatherForecast
from services import weatherforecastservice

router = APIRouter()


@router.get("/", response_model=WeatherForecast)
async def get_weather_forcast(
    meteorological_observatory_name: str = Query(
        ..., alias="meteorologicalObservatoryName"
    ),
    large_area_code: str = Query(..., alias="largeAreaCode"),
    report_date: datetime.date = Query(..., alias="reportDate"),
) -> WeatherForecast:
    """
    天気予報の情報を返す
    """
    return weatherforecastservice.get_weather_forcast(
        meteorological_observatory_name=meteorological_observatory_name,
        large_area_code=large_area_code,
        report_date=report_date,
    )


@router.get("/largearea", response_model=list[LargeArea])
async def get_largearea(
    meteorological_observatory_name: str = Query(
        ..., alias="meteorologicalObservatoryName"
    ),
    report_date: datetime.date = Query(..., alias="reportDate"),
) -> list[LargeArea]:
    """
    天気予報の取得開始日を返す
    """
    return weatherforecastservice.get_largearea(
        meteorological_observatory_name=meteorological_observatory_name,
        report_date=report_date,
    )


@router.get("/startdate", response_model=StartDate)
async def get_start_date(
    meteorological_observatory_name: str = Query(
        ..., alias="meteorologicalObservatoryName"
    )
) -> StartDate:
    """
    天気予報の取得開始日を返す
    """
    return weatherforecastservice.get_start_date(
        meteorological_observatory_name=meteorological_observatory_name
    )


@router.get("/kubun", response_model=list[Kubun])
async def get_kubun() -> list[Kubun]:
    """
    予報区分、気象台
    """
    return weatherforecastservice.get_kubun()
