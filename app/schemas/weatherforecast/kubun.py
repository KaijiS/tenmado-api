from pydantic import BaseModel, Field
from schemas.weatherforecast.meteorologicalobservatory import MeteorologicalObservatory


class Kubun(BaseModel):
    kubun_code: str = Field(..., description="予報区分コード", alias="kubunCode", example="01")
    kubun_name: str = Field(..., description="予報区分名", alias="kubunName", example="北海道")
    meteorological_observatories: list[MeteorologicalObservatory] = Field(
        ..., alias="meteorologicalObservatories"
    )

    class Config:
        allow_population_by_field_name = True


"""
[
    {
        kubun_code: '02',
        kubun_name: '東北'
        'meteorologicalObservatories': [
            {
                'meteorologicalObservatoryCode': '040000',
                'meteorologicalObservatoryName': '仙台管区気象台',
            },
            {
                'meteorologicalObservatoryCode': '040000',
                'meteorologicalObservatoryName': '福島地方気象台',
            }
        ]
    }
]
"""
