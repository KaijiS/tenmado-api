import datetime

from pydantic import BaseModel
from pydantic import Field

from schemas.weatherforecast.forecast import Forecast


class Report(BaseModel):

    report_date: datetime.date = Field(
        ..., description="気象レポート日", alias="reportDate", example="2021-01-01"
    )
    forecast_target_date_from: datetime.date = Field(
        ..., description="予報対象日開始", alias="forecastTargetDateFrom", example="2021-01-02"
    )
    forecast_target_date_to: datetime.date = Field(
        ..., description="予報対象日終了", alias="forecastTargetDateTo", example="2021-01-08"
    )
    forecastdays: int = Field(
        ..., description="予報対象日数", alias="forecastdays", example=7
    )
    forecasts: list[Forecast] = Field(...)

    class Config:
        allow_population_by_field_name = True
