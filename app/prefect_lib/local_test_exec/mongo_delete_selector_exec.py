from datetime import date
from prefect.testing.utilities import prefect_test_harness
from BrownieAtelierMongo.collection_models.asynchronous_report_model import \
    AsynchronousReportModel
from BrownieAtelierMongo.collection_models.controller_model import \
    ControllerModel
from BrownieAtelierMongo.collection_models.crawler_logs_model import \
    CrawlerLogsModel
from BrownieAtelierMongo.collection_models.crawler_response_model import \
    CrawlerResponseModel
from BrownieAtelierMongo.collection_models.news_clip_master_model import \
    NewsClipMasterModel
from BrownieAtelierMongo.collection_models.scraped_from_response_model import \
    ScrapedFromResponseModel
from BrownieAtelierMongo.collection_models.stats_info_collect_model import \
    StatsInfoCollectModel
from prefect_lib.flows.mongo_delete_selector_flow import \
    mongo_delete_selector_flow

def test_exec():
    with prefect_test_harness():

        mongo_delete_selector_flow(
            collections_name=[
                CrawlerResponseModel.COLLECTION_NAME,
                ScrapedFromResponseModel.COLLECTION_NAME,  # 通常運用では不要なバックアップとなるがテスト用に実装している。
                NewsClipMasterModel.COLLECTION_NAME,
                CrawlerLogsModel.COLLECTION_NAME,
                AsynchronousReportModel.COLLECTION_NAME,
                ControllerModel.COLLECTION_NAME,
                StatsInfoCollectModel.COLLECTION_NAME,
            ],
            period_date_from=date(2024,12,1),  # 月次エクスポートを行うデータの基準年月
            period_date_to=date(2024,12,8),  # 月次エクスポートを行うデータの基準年月
            # crawler_response__registered=False,
        )

if __name__ == "__main__":
    test_exec()