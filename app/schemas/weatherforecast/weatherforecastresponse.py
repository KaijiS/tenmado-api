import datetime

from pydantic import BaseModel
from pydantic import Field

from schemas.weatherforecast.report import Report


class WeatherForecastResponse(BaseModel):

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
    city_code: str = Field(
        ...,
        description="都市コード",
        alias="cityCode",
        example="11111",
    )
    city_name: str = Field(
        ...,
        description="都市名",
        alias="cityName",
        example="〇〇市",
    )
    report_date_from: datetime.date = Field(
        ..., description="予報レポート日開始", alias="reportDateFrom", example="2021-01-01"
    )
    report_date_to: datetime.date = Field(
        ..., description="予報レポート日終了", alias="reportDateTo", example="2021-01-03"
    )
    report_days: int = Field(..., description="予報レポート日数", alias="reportDays", example=3)
    reports: list[Report] = Field(...)

    class Config:
        allow_population_by_field_name = True
