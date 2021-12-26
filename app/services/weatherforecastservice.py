import datetime
import math
import json

from schemas.weatherforecast.weatherforecastresponse import WeatherForecastResponse
from schemas.weatherforecast.report import Report
from schemas.weatherforecast.forecast import Forecast
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
                weather=TELOPS[forecast_source["weather_code"]][3],
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
