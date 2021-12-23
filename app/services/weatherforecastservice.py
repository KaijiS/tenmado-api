import datetime

from schemas.weatherforecast.weatherforecastresponse import WeatherForecastResponse
from repositories import weekweatherrepository


def get_weather_forcast(
    large_area_code: str,
    report_date_from: datetime.date,
    report_date_to: datetime.date,
    report_days: int,
) -> WeatherForecastResponse:
    """
    気象予報情報を取得する
    parameters
        larage_area_code: str: 地域コード
        report_date_from: datetime.date: レポート日開始
        report_date_to: datetime.date: レポート日終了
        report_days: int: 各レポート日に対する予報対象日数
    returns
        WeatherForecastResponse
    """
    weekweathers = weekweatherrepository.findbylargeareacode(
        large_area_code=large_area_code,
        report_date_from=report_date_from,
        report_date_to=report_date_to,
        report_days=report_days,
    )

    # weatherforecastresponse = WeatherForecastResponse()

    return weekweathers
