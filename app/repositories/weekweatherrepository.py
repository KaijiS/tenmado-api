import datetime

from google.cloud import firestore

db = firestore.Client()


def findbylargeareacode(
    large_area_code: str,
    report_date_from: datetime.date,
    report_date_to: datetime.date,
    report_days: int,
):
    weekweather_querydocumentsnapshots = (
        db.collection("weekweather")
        .where("large_area_code", "==", large_area_code)
        .where(
            "report_datetime",
            ">=",
            datetime.datetime.combine(report_date_from, datetime.time()),
        )
        .where(
            "report_datetime",
            "<=",
            datetime.datetime.combine(report_date_to, datetime.time())
            + datetime.timedelta(days=1),
        )
        .order_by("report_datetime")
    ).stream()

    weekweathers = []
    for weekweather_querydocumentsnapshot in weekweather_querydocumentsnapshots:
        weekweather = weekweather_querydocumentsnapshot.to_dict()

        forecast_querydocumentsnapshots = (
            weekweather_querydocumentsnapshot.reference.collection("forecasts")
            .order_by("forecast_target_date")
            .limit(report_days)
            .stream()
        )

        weekweather["forecast"] = [
            forecast_querydocumentsnapshot.to_dict()
            for forecast_querydocumentsnapshot in forecast_querydocumentsnapshots
        ]

        weekweathers.append(weekweather)

    return weekweathers
