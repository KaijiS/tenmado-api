import datetime

from google.cloud import firestore

db = firestore.Client()


def findbylargeareacode(
    large_area_code: str,
    report_date_from: datetime.date,
    report_date_to: datetime.date,
):
    weekweather_collection = (
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
    )
    weekweather = weekweather_collection.get()
    return weekweather
