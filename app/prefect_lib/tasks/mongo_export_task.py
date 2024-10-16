import os
import pickle
from datetime import datetime
from typing import Any

from BrownieAtelierMongo.collection_models.asynchronous_report_model import \
    AsynchronousReportModel
from BrownieAtelierMongo.collection_models.controller_model import \
    ControllerModel
from BrownieAtelierMongo.collection_models.crawler_logs_model import \
    CrawlerLogsModel
from BrownieAtelierMongo.collection_models.crawler_response_model import \
    CrawlerResponseModel
from BrownieAtelierMongo.collection_models.mongo_model import MongoModel
from BrownieAtelierMongo.collection_models.news_clip_master_model import \
    NewsClipMasterModel
from BrownieAtelierMongo.collection_models.scraped_from_response_model import \
    ScrapedFromResponseModel
from BrownieAtelierMongo.collection_models.stats_info_collect_model import \
    StatsInfoCollectModel
from prefect import get_run_logger, task
from prefect_lib.flows import START_TIME
from pymongo import ASCENDING
from pymongo.cursor import Cursor


@task
def mongo_export_task(
    mongo: MongoModel,
    dir_path: str,  # export先のフォルダ名
    period_from: datetime,  # 月次エクスポートを行うデータの基準年月
    period_to: datetime,  # 月次エクスポートを行うデータの基準年月
    collections_name: list[str],
    crawler_response__registered: bool,
):
    """ """
    logger = get_run_logger()  # PrefectLogAdapter
    logger.info(
        f"=== 引数 : dir_path={dir_path} collections_name= {collections_name} period_from~to= {period_from} ~ {period_to}"
    )

    # バックアップフォルダ直下に基準年月ごとのフォルダを作る。
    # 同一フォルダへのエクスポートは禁止。
    if os.path.exists(dir_path):
        logger.error(f"=== backup_dirパラメータエラー : {dir_path} は既に存在します。")
        raise ValueError(dir_path)
    else:
        os.mkdir(dir_path)

    # タイムスタンプをファイル名にした空ファイルを作成。
    with open(f"{os.path.join(dir_path, START_TIME.isoformat())}", "w") as f:
        pass

    for collection_name in collections_name:
        # ファイル名 ＝ コレクション名
        file_path: str = os.path.join(dir_path, f"{collection_name}")

        sort_parameter: list = []
        collection = None
        conditions: list = []

        if collection_name == CrawlerResponseModel.COLLECTION_NAME:
            collection = CrawlerResponseModel(mongo)
            sort_parameter = [(CrawlerResponseModel.RESPONSE_TIME, ASCENDING)]
            conditions.append(
                {CrawlerResponseModel.CRAWLING_START_TIME: {"$gte": period_from}}
            )
            conditions.append(
                {CrawlerResponseModel.CRAWLING_START_TIME: {"$lte": period_to}}
            )
            if crawler_response__registered:
                conditions.append(
                    {
                        CrawlerResponseModel.NEWS_CLIP_MASTER_REGISTER: CrawlerResponseModel.NEWS_CLIP_MASTER_REGISTER__COMPLETE
                    }
                )  # crawler_responseの場合、登録完了のレコードのみ保存する。

        elif collection_name == ScrapedFromResponseModel.COLLECTION_NAME:
            collection = ScrapedFromResponseModel(mongo)
            sort_parameter = []
            conditions.append(
                {ScrapedFromResponseModel.SCRAPYING_START_TIME: {"$gte": period_from}}
            )
            conditions.append(
                {ScrapedFromResponseModel.SCRAPYING_START_TIME: {"$lte": period_to}}
            )

        elif collection_name == NewsClipMasterModel.COLLECTION_NAME:
            collection = NewsClipMasterModel(mongo)
            sort_parameter = [(NewsClipMasterModel.RESPONSE_TIME, ASCENDING)]
            conditions.append(
                {NewsClipMasterModel.SCRAPED_SAVE_START_TIME: {"$gte": period_from}}
            )
            conditions.append(
                {NewsClipMasterModel.SCRAPED_SAVE_START_TIME: {"$lte": period_to}}
            )

        elif collection_name == CrawlerLogsModel.COLLECTION_NAME:
            collection = CrawlerLogsModel(mongo)
            conditions.append({CrawlerLogsModel.START_TIME: {"$gte": period_from}})
            conditions.append({CrawlerLogsModel.START_TIME: {"$lte": period_to}})

        elif collection_name == AsynchronousReportModel.COLLECTION_NAME:
            collection = AsynchronousReportModel(mongo)
            conditions.append(
                {AsynchronousReportModel.START_TIME: {"$gte": period_from}}
            )
            conditions.append({AsynchronousReportModel.START_TIME: {"$lte": period_to}})

        elif collection_name == StatsInfoCollectModel.COLLECTION_NAME:
            collection = StatsInfoCollectModel(mongo)
            conditions.append({StatsInfoCollectModel.START_TIME: {"$gte": period_from}})
            conditions.append({StatsInfoCollectModel.START_TIME: {"$lte": period_to}})

        elif collection_name == ControllerModel.COLLECTION_NAME:
            collection = ControllerModel(mongo)

        if collection:
            filter: Any = {"$and": conditions} if conditions else None

            # エクスポート対象件数を確認
            record_count = collection.count(filter)
            logger.info(f"=== {collection_name} バックアップ対象件数 : {str(record_count)}")

            # ファイルにリストオブジェクトを追記していく
            with open(file_path, "ab") as file:
                pass  # 空ファイル作成

            records: Cursor = collection.find(filter=filter, sort=sort_parameter)
            record_list: list = [record for record in records]

            with open(file_path, "ab") as file:
                file.write(pickle.dumps(record_list))

        # 誤更新防止のため、ファイルの権限を参照に限定
        os.chmod(file_path, 0o444)
