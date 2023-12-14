import datetime
import os
from typing import Any

import pytz
from google.cloud import firestore

db = firestore.Client()
base_doc = db.collection("env").document(
    "prd" if os.environ.get("_ENV") == "prd" else "dev"
)


def findbymeteorologicalobservatorynameandlargeareacode(
    meteorological_observatory_name: str,
    large_area_code: str,
    report_date: datetime.date,
) -> list[Any]:
    docs = (
        base_doc.collection("week_weather_temps")
        .where("meteorological_observatory_name", "==", meteorological_observatory_name)
        .where("large_area_code", "==", large_area_code)
        .where(
            "report_date",
            "==",
            pytz.timezone("Asia/Tokyo").localize(
                datetime.datetime.combine(report_date, datetime.time(9, 0, 0))
            ),
        )
        .order_by("forecast_target_date")
    ).stream()

    return [doc.to_dict() for doc in docs]


def findlargeareabymeteorologicalobservatorynameandreportdate(
    meteorological_observatory_name: str, report_date: datetime.date
):
    return [
        doc.to_dict()
        for doc in (
            base_doc.collection("week_weather_temps")
            .where(
                "meteorological_observatory_name", "==", meteorological_observatory_name
            )
            .where(
                "report_date",
                "==",
                pytz.timezone("Asia/Tokyo").localize(
                    datetime.datetime.combine(report_date, datetime.time(9, 0, 0))
                ),
            )
            .order_by("large_area_code")
            .stream()
        )
    ]


def findstartdatebymeteorologicalobservatoryname(
    meteorological_observatory_name,
) -> datetime.datetime:
    return [
        doc.to_dict()
        for doc in (
            base_doc.collection("week_weather_temps")
            .where(
                "meteorological_observatory_name", "==", meteorological_observatory_name
            )
            .order_by("report_date")
            .limit(1)
            .stream()
        )
    ][0]["report_date"]


def findkubun() -> list[Any]:
    return [
        largearea.to_dict()
        for largearea in base_doc.collection("kubun_mo")
        .order_by("kubun_code")
        .order_by("meteorological_observatory_code")
        .stream()
    ]
