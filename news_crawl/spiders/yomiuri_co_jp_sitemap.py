from news_crawl.spiders.extensions_class.extensions_sitemap import ExtensionsSitemapSpider


class YomiuriCoJpSitemapSpider(ExtensionsSitemapSpider):
    name: str = 'yomiuri_co_jp_sitemap'
    allowed_domains: list = ['yomiuri.co.jp']
    sitemap_urls: list = ['https://www.yomiuri.co.jp/sitemap.xml']
    _domain_name: str = 'yomiuri_co_jp'        # 各種処理で使用するドメイン名の一元管理
    _spider_version: float = 1.0

    # https://www.yomiuri.co.jp/sitemap-pt-post-2021-09-04.xml
    sitemap_follow = ['/sitemap-pt-post-']
