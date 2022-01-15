from pydantic import BaseModel
from pydantic import Field


class LargeArea(BaseModel):

    large_area_code: str = Field(
        ..., description="ラージエリアコード(地方コード)", alias="largeAreaCode", example="111111"
    )

    large_area_name: str = Field(
        ..., description="ラージエリア名(地方名)", alias="largeAreaName", example="西部"
    )

    class Config:
        allow_population_by_field_name = True
