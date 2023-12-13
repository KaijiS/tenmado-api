import datetime

from pydantic import BaseModel, Field
from schemas.weatherforecast.forecast import Forecast


class WeatherForecast(BaseModel):
    meteorological_observatory_name: str = Field(
        ..., description="気象台名", alias="meteorologicalObservatoryName", example="〇〇気象台"
    )
    large_area_code: str = Field(
        ...,
        description="地域コード",
        alias="largeAreaCode",
        example="00000",
    )
    large_area_name: str = Field(
        ...,
        description="地域名",
        alias="largeAreaName",
        example="〇〇地方",
    )
    # city_code: str = Field(
    #     ...,
    #     description="都市コード",
    #     alias="cityCode",
    #     example="11111",
    # )
    city_name: str = Field(
        ...,
        description="都市名",
        alias="cityName",
        example="〇〇市",
    )
    report_date: datetime.date = Field(
        ..., description="予報レポート日", alias="reportDate", example="2021-01-01"
    )
    forecasts: list[Forecast] = Field(...)

    class Config:
        allow_population_by_field_name = True
