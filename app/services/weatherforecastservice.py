import datetime
import math
import json

from schemas.weatherforecast.weatherforecastresponse import WeatherForecastResponse
from schemas.weatherforecast.report import Report
from schemas.weatherforecast.forecast import Forecast
from schemas.weatherforecast.startdateresponse import StartDateResponse
from schemas.weatherforecast.meteorologicalobservatoryresponse import (
    MeteorologicalObservatoryResponse,
)
from schemas.weatherforecast.kubunresponse import KubunResponse
from schemas.weatherforecast.kubun import Kubun
from schemas.weatherforecast.flattenkubun import FlattenKubun
from schemas.weatherforecast.meteorologicalobservatory import MeteorologicalObservatory
from schemas.weatherforecast.largearea import LargeArea
from repositories import weekweatherrepository


def get_weather_forcast(
    large_area_code: str,
    report_date_from: datetime.date,
    report_date_to: datetime.date,
    forecastdays: int,
) -> WeatherForecastResponse:
    """
    気象予報情報を取得する
    parameters
        larage_area_code: str: 地域コード
        report_date_from: datetime.date: レポート日開始
        report_date_to: datetime.date: レポート日終了
        forecastdays: int: 各レポート日に対する予報対象日数
    returns
        WeatherForecastResponse
    """

    # 天気コードとその内容のマッピング情報をjsonファイルから取得
    with open("constants/TELOPS.json") as f:
        TELOPS = json.load(f)

    # 天気画像ベースURL
    WEATHER_FIG_URL_BASE = (
        "https://www.jma.go.jp/bosai/forecast/img/{weather_fig_filename}"
    )

    # 週予報情報を取得
    weekweathers = weekweatherrepository.findbylargeareacode(
        large_area_code=large_area_code,
        report_date_from=report_date_from,
        report_date_to=report_date_to,
        forecastdays=forecastdays,
    )

    # レスポンススキーマへ入れ替え
    reports = []
    for index, weekweather_source in enumerate(weekweathers):

        if index == 0:
            meteorological_observatory_name = weekweather_source[
                "meteorological_observatory_name"
            ]
            large_area_code = weekweather_source["large_area_code"]
            large_area_name = weekweather_source["large_area_code"]
            city_code = weekweather_source["city_code"]
            city_name = weekweather_source["city_name"]

        forecasts = []
        for forecast_source in weekweather_source["forecast"]:

            forcast = Forecast(
                forecast_target_date=forecast_source["forecast_target_date"],
                weather_code=forecast_source["weather_code"],
                weather=TELOPS[forecast_source["weather_code"]][3],
                weather_fig_url=WEATHER_FIG_URL_BASE.format(
                    weather_fig_filename=TELOPS[forecast_source["weather_code"]][0]
                ),
                pop=forecast_source["pop"],
                reliability=forecast_source["reliability"],
                lowest_temperature=forecast_source["lowest_temperature"],
                lowest_temperature_lower=forecast_source["lowest_temperature_lower"],
                lowest_temperature_upper=forecast_source["lowest_temperature_upper"],
                highest_temperature=forecast_source["highest_temperature"],
                highest_temperature_lower=forecast_source["highest_temperature_lower"],
                highest_temperature_upper=forecast_source["highest_temperature_upper"],
            )
            forecasts.append(forcast)

        report = Report(
            report_date=weekweather_source["report_datetime"],
            forecast_target_date_from=forecasts[0].forecast_target_date,
            forecast_target_date_to=forecasts[-1].forecast_target_date,
            forecastdays=forecastdays,
            forecasts=forecasts,
        )
        reports.append(report)

    weatherforecastresponse = WeatherForecastResponse(
        meteorological_observatory_name=meteorological_observatory_name,
        large_area_code=large_area_code,
        large_area_name=large_area_name,
        city_code=city_code,
        city_name=city_name,
        report_date_from=report_date_from,
        report_date_to=report_date_to,
        report_days=(report_date_to - report_date_from).days + 1,
        reports=reports,
    )

    return weatherforecastresponse


def get_start_date(large_area_code: str) -> StartDateResponse:

    start_date = weekweatherrepository.findstartdatebylargeareacode(large_area_code)
    startdateresponse = StartDateResponse(start_date=start_date)
    return startdateresponse


def get_meteorological_observatory() -> MeteorologicalObservatoryResponse:

    largeareas_firestoreschema = weekweatherrepository.findmeteorologicalobservatory()

    # 気象台コードと気象台名を取得し、ユニークを取る
    meteorological_observatory_unique_list = [
        dict(s)
        for s in set(
            [
                frozenset(
                    {
                        "meteorological_observatory_code": largearea_firestoreschema[
                            "meteorological_observatory_code"
                        ],
                        "meteorological_observatory_name": largearea_firestoreschema[
                            "meteorological_observatory_name"
                        ],
                    }.items()
                )
                for largearea_firestoreschema in largeareas_firestoreschema
            ]
        )
    ]
    # 並び替え
    meteorological_observatory_unique_list = sorted(
        meteorological_observatory_unique_list,
        key=lambda x: x["meteorological_observatory_code"],
        reverse=False,
    )

    meteorological_observatories = []
    for meteorological_observatory_unique in meteorological_observatory_unique_list:

        large_areas = [
            LargeArea(
                large_area_code=largearea_firestoreschema["large_area_code"],
                large_area_name=largearea_firestoreschema["large_area_name"],
            )
            for largearea_firestoreschema in largeareas_firestoreschema
            if largearea_firestoreschema["meteorological_observatory_code"]
            == meteorological_observatory_unique["meteorological_observatory_code"]
        ]

        meteorological_observatories.append(
            MeteorologicalObservatory(
                meteorological_observatory_code=meteorological_observatory_unique[
                    "meteorological_observatory_code"
                ],
                meteorological_observatory_name=meteorological_observatory_unique[
                    "meteorological_observatory_name"
                ],
                large_areas=large_areas,
            )
        )

    meteorological_observatory_response = MeteorologicalObservatoryResponse(
        meteorological_observatories=meteorological_observatories
    )

    return meteorological_observatory_response


def get_kubun() -> KubunResponse:

    kubuns_firestoreschema = weekweatherrepository.findkubun()

    kubuns = []
    flatten_kubuns = []
    for kubun_firestoreschema in kubuns_firestoreschema:

        meteorological_observatories = []
        for meteorological_observatory in kubun_firestoreschema[
            "meteorological_observatory"
        ]:

            large_areas = []
            for large_area in meteorological_observatory["large_areas"]:

                large_areas.append(
                    LargeArea(
                        large_area_code=large_area["large_area_code"],
                        large_area_name=large_area["large_area_name"],
                    )
                )

                flatten_kubuns.append(
                    FlattenKubun(
                        kubun_code=kubun_firestoreschema["kubun_code"],
                        kubun_name=kubun_firestoreschema["kubun_name"],
                        meteorological_observatory_code=meteorological_observatory[
                            "meteorological_observatory_code"
                        ],
                        meteorological_observatory_name=meteorological_observatory[
                            "meteorological_observatory_name"
                        ],
                        large_area_code=large_area["large_area_code"],
                        large_area_name=large_area["large_area_name"],
                    )
                )

            meteorological_observatories.append(
                MeteorologicalObservatory(
                    meteorological_observatory_code=meteorological_observatory[
                        "meteorological_observatory_code"
                    ],
                    meteorological_observatory_name=meteorological_observatory[
                        "meteorological_observatory_name"
                    ],
                    large_areas=large_areas,
                )
            )

        kubuns.append(
            Kubun(
                kubun_code=kubun_firestoreschema["kubun_code"],
                kubun_name=kubun_firestoreschema["kubun_name"],
                meteorological_observatories=meteorological_observatories,
            )
        )

    return KubunResponse(kubuns=kubuns, flattenkubuns=flatten_kubuns)
