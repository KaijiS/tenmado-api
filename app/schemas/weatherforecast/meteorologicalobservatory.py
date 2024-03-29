from pydantic import BaseModel, Field


class MeteorologicalObservatory(BaseModel):
    meteorological_observatory_code: str = Field(
        ...,
        description="気象台コード",
        alias="meteorologicalObservatoryCode",
        example="000000",
    )

    meteorological_observatory_name: str = Field(
        ..., description="気象台名", alias="meteorologicalObservatoryName", example="〇〇気象台"
    )

    class Config:
        allow_population_by_field_name = True
