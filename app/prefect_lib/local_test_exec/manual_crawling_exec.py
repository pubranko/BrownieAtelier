import glob
import os
from prefect.testing.utilities import prefect_test_harness
from prefect_lib.flows.manual_crawling_flow import manual_crawling_flow


def test_exec():
    with prefect_test_harness():

        manual_crawling_flow(
            spider_names=[
                "sankei_com_sitemap",
                # "asahi_com_sitemap",
                # "kyodo_co_jp_sitemap",
                # "yomiuri_co_jp_sitemap",
                # "jp_reuters_com_sitemap",
                # "epochtimes_jp_crawl",
                # "mainichi_jp_crawl",
                # "nikkei_com_crawl",
            ],
            spider_kwargs=dict(
                debug=True,
                # continued = True,
                # crawl_point_non_update = True,
                page_span_from=2,
                page_span_to=2,
                lastmod_term_minutes_from=30,
                lastmod_term_minutes_to=0,
                # direct_crawl_urls = [],
                # url_pattern =  'https://www.yomiuri.co.jp/national/20220430-OYT1T50050',
            ),
            # following_processing_execution=False    # 後続処理実行(scrapying,news_clip_masterへの登録,solrへの登録)
            following_processing_execution=True  # 後続処理実行(scrapying,news_clip_masterへの登録,solrへの登録)
            # spider_kwargs={
            #     'debug': 'Yes',
            #     'pages': '1,1',
            #     'lastmod_period_minutes': '120,',
            #     #'lastmod_period_minutes': '3840,3780',
            #     #'continued':'Yes',
            #     # 'direct_crawl_urls':[],
            #     #'crawl_point_non_update':'Yes',
            #     #'url_pattern':'https://www.yomiuri.co.jp/national/20220430-OYT1T50050',
            #     #'url_pattern':'https://mainichi.jp/articles/20220607/k00/00m/050/362000c',
            #     #'url_pattern':'https://jp.reuters.com/article/euronext-tech-idJPKBN2NO0TB',
            #     #'url_pattern':'https://www.epochtimes.jp/2022/06/107648.html',
            # },
        )

if __name__ == "__main__":
    test_exec()

"""
{
    "spider_names": [
        "sankei_com_sitemap",
        "asahi_com_sitemap",
        "kyodo_co_jp_sitemap",
        "yomiuri_co_jp_sitemap",
        "jp_reuters_com_sitemap",
        "epochtimes_jp_crawl",
        "mainichi_jp_crawl",
        "nikkei_com_crawl"
    ],

    "spider_kwargs": {
        "debug": true,
        "page_span_from": 2,
        "page_span_to": 2,
        "lastmod_term_minutes_from": 90,
        "lastmod_term_minutes_to": 60
    },

    "following_processing_execution": true
}
"""
