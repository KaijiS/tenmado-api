import datetime

import pandas as pd
from repositories import weekweatherrepository
from schemas.weatherforecast.forecast import Forecast
from schemas.weatherforecast.kubun import Kubun
from schemas.weatherforecast.largearea import LargeArea
from schemas.weatherforecast.meteorologicalobservatory import MeteorologicalObservatory
from schemas.weatherforecast.startdate import StartDate
from schemas.weatherforecast.weatherforecast import WeatherForecast


def get_weather_forcast(
    meteorological_observatory_name: str,
    large_area_code: str,
    report_date: datetime.date,
) -> WeatherForecast:
    """
    気象予報情報を取得する
    parameters
        meteorological_observatory_name: str: 気象台名
        large_area_code: ラージエリアコード
        report_date: datetime.date: レポート日
    returns
        WeatherForecast
    """

    # 天気画像ベースURL
    WEATHER_FIG_URL_BASE = (
        "https://www.jma.go.jp/bosai/forecast/img/{weather_fig_filename}"
    )

    # 週予報情報を取得
    weekweathers = (
        weekweatherrepository.findbymeteorologicalobservatorynameandlargeareacode(
            meteorological_observatory_name=meteorological_observatory_name,
            large_area_code=large_area_code,
            report_date=report_date,
        )
    )

    # レスポンススキーマへ入れ替え
    forecasts = []
    for index, weekweather in enumerate(weekweathers):
        if index == 0:
            meteorological_observatory_name = weekweather[
                "meteorological_observatory_name"
            ]
            large_area_code = weekweather["large_area_code"]
            large_area_name = weekweather["large_area_name"]
            city_code = weekweather["city_code"]
            city_name = weekweather["city_name"]

        forcast = Forecast(
            forecast_target_date=weekweather["forecast_target_date"],
            weather_code=weekweather["weather_code"],
            weather=weekweather["weather_text"],
            weather_fig_url=WEATHER_FIG_URL_BASE.format(
                weather_fig_filename=weekweather["weather_code"] + ".svg"
            ),
            pop=weekweather["pop"],
            reliability=weekweather["reliability"],
            lowest_temperature=weekweather["lowest_temperature"],
            lowest_temperature_lower=weekweather["lowest_temperature_lower"],
            lowest_temperature_upper=weekweather["lowest_temperature_upper"],
            highest_temperature=weekweather["highest_temperature"],
            highest_temperature_lower=weekweather["highest_temperature_lower"],
            highest_temperature_upper=weekweather["highest_temperature_upper"],
        )
        forecasts.append(forcast)

    weatherforecast = WeatherForecast(
        meteorological_observatory_name=meteorological_observatory_name,
        large_area_code=large_area_code,
        large_area_name=large_area_name,
        city_code=city_code,
        city_name=city_name,
        report_date=report_date,
        forecasts=forecasts,
    )

    return weatherforecast


def get_largearea(
    meteorological_observatory_name: str, report_date: datetime.date
) -> list[LargeArea]:
    large_areas = (
        weekweatherrepository.findlargeareabymeteorologicalobservatorynameandreportdate(
            meteorological_observatory_name=meteorological_observatory_name,
            report_date=report_date,
        )
    )
    large_areas_df = pd.DataFrame(large_areas)[
        ["large_area_code", "large_area_name"]
    ].drop_duplicates()
    return [
        LargeArea(
            large_area_code=large_area["large_area_code"],
            large_area_name=large_area["large_area_name"],
        )
        for index, large_area in large_areas_df.iterrows()
    ]


def get_start_date(meteorological_observatory_name: str) -> StartDate:
    start_date = weekweatherrepository.findstartdatebymeteorologicalobservatoryname(
        meteorological_observatory_name
    )
    startdate = StartDate(start_date=start_date)
    return startdate


def get_kubun() -> list[Kubun]:
    kubun_meteorologicalobservatory_list = weekweatherrepository.findkubun()

    kubun_meteorologicalobservatory_df = pd.DataFrame(
        kubun_meteorologicalobservatory_list
    )

    kubun_df = kubun_meteorologicalobservatory_df[
        ["kubun_code", "kubun_name"]
    ].drop_duplicates()

    kubuns = []
    for _, kubun in kubun_df.iterrows():
        meteorological_observatories = []

        kubun_meteorologicalobservatory_tmp_df = kubun_meteorologicalobservatory_df[
            (kubun_meteorologicalobservatory_df["kubun_code"] == kubun["kubun_code"])
        ]

        for _, meteorological_observatory in kubun_meteorologicalobservatory_tmp_df[
            ["meteorological_observatory_code", "meteorological_observatory_name"]
        ].iterrows():
            meteorological_observatories.append(
                MeteorologicalObservatory(
                    meteorological_observatory_code=meteorological_observatory[
                        "meteorological_observatory_code"
                    ],
                    meteorological_observatory_name=meteorological_observatory[
                        "meteorological_observatory_name"
                    ],
                )
            )

        kubuns.append(
            Kubun(
                kubun_code=kubun["kubun_code"],
                kubun_name=kubun["kubun_name"],
                meteorological_observatories=meteorological_observatories,
            )
        )

    return kubuns
