from pydantic import BaseModel
from pydantic import Field

from schemas.weatherforecast.meteorogicalobservatory import MeteorogicalObservatory


class MeteorogicalObservatoryResponse(BaseModel):

    meteorologicalObservatories: list[MeteorogicalObservatory] = Field(...)

    class Config:
        allow_population_by_field_name = True


"""
{
    'meteorologicalObservatories': [
        {
            'meteorologicalObservatoryCode': '040000',
            'meteorologicalObservatoryName': '仙台管区気象台',
            'largeAreas': [
                {
                    'largeAreaCode': '040010',
                    'largeAreaName': '東部',
                },
                {
                    'largeAreaCode': '040020',
                    'largeAreaName': '西部',
                }
            ]
        },
        {
            'meteorologicalObservatoryCode': '040000',
            'meteorologicalObservatoryName': '福島地方気象台',
            'largeAreas': [
                {
                    'largeAreaCode': '070100',
                    'largeAreaName': '中通り・浜通り',
                },
                {
                    'largeAreaCode': '070030',
                    'largeAreaName': '会津',
                }
            ]
        }
    ]
}
"""
