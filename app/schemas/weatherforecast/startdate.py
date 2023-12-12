import datetime

from pydantic import BaseModel, Field


class StartDate(BaseModel):
    start_date: datetime.date = Field(
        ..., description="予報レポート日開始", alias="startDate", example="2021-01-01"
    )

    class Config:
        allow_population_by_field_name = True
