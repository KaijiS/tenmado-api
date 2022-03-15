from pydantic import BaseModel
from pydantic import Field

from schemas.weatherforecast.kubun import Kubun
from schemas.weatherforecast.flattenkubun import FlattenKubun


class KubunResponse(BaseModel):

    kubuns: list[Kubun] = Field(...)
    flattenkubuns: list[FlattenKubun]

    class Config:
        allow_population_by_field_name = True
