import datetime
from typing import Any

from google.cloud import firestore

db = firestore.Client()


def findbylargeareacode(
    large_area_code: str,
    report_date_from: datetime.date,
    report_date_to: datetime.date,
    forecastdays: int,
) -> dict[str:Any]:

    # firestoreメモ
    # Reference 概念
    # Snapshot 実態

    # 「collecion reference」(db.collection)に対してwhereやorder系を実施すると 「query」という概念を取得(クエリ命令のみ)
    # それに対しstream()を実行するとクエリが実行され、実態である「query document snapshot」を要素とする配列を取得する
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
            # 1日後の 00時00分00秒までが範囲
            datetime.datetime.combine(report_date_to, datetime.time())
            + datetime.timedelta(days=1),
        )
        .order_by("report_datetime")
    ).stream()

    weekweathers = []
    for weekweather_querydocumentsnapshot in weekweather_querydocumentsnapshots:
        # snapshot(実態を辞書に)
        weekweather = weekweather_querydocumentsnapshot.to_dict()

        forecast_querydocumentsnapshots = (
            # snapshotのreferenceに対してcollection(subcollection)を指定して上述同様にqueryの実行
            weekweather_querydocumentsnapshot.reference.collection("forecasts")
            .order_by("forecast_target_date")
            .limit(forecastdays)
            .stream()
        )

        weekweather["forecast"] = [
            forecast_querydocumentsnapshot.to_dict()
            for forecast_querydocumentsnapshot in forecast_querydocumentsnapshots
        ]

        weekweathers.append(weekweather)

    return weekweathers


def findstartdatebylargeareacode(large_area_code) -> datetime.date:

    return [
        weekweather_querydocumentsnapshots.to_dict()
        for weekweather_querydocumentsnapshots in (
            db.collection("weekweather")
            .where("large_area_code", "==", large_area_code)
            .order_by("report_datetime")
            .limit(1)
            .stream()
        )
    ][0]["report_datetime"]


def findmeteorologicalobservatory() -> dict[str:Any]:

    return [
        largearea.to_dict()
        for largearea in db.collection("largearea")
        .order_by("meteorological_observatory_code")
        .stream()
    ]
