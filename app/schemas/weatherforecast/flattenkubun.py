from pydantic import BaseModel
from pydantic import Field

from schemas.weatherforecast.meteorologicalobservatory import MeteorologicalObservatory


class FlattenKubun(BaseModel):

    kubun_code: str = Field(..., description="予報区分コード", alias="kubunCode", example="01")
    kubun_name: str = Field(..., description="予報区分名", alias="kubunName", example="北海道")
    meteorological_observatory_code: str = Field(
        ...,
        description="気象台コード",
        alias="meteorologicalObservatoryCode",
        example="000000",
    )
    meteorological_observatory_name: str = Field(
        ..., description="気象台名", alias="meteorologicalObservatoryName", example="〇〇気象台"
    )
    large_area_code: str = Field(
        ..., description="ラージエリアコード(地方コード)", alias="largeAreaCode", example="111111"
    )

    large_area_name: str = Field(
        ..., description="ラージエリア名(地方名)", alias="largeAreaName", example="西部"
    )

    class Config:
        allow_population_by_field_name = True
