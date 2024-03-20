from news_crawl.spiders.extensions_class.extensions_sitemap import \
    ExtensionsSitemapSpider


class YomiuriCoJpSitemapSpider(ExtensionsSitemapSpider):
    name: str = "yomiuri_co_jp_sitemap"
    allowed_domains: list = ["yomiuri.co.jp"]
    sitemap_urls: list = [
        "https://www.yomiuri.co.jp/sitemap-news-latest.xml",
        "https://www.yomiuri.co.jp/sitemap-news-past-1.xml",
        "https://www.yomiuri.co.jp/sitemap-news-past-2.xml",
        "https://www.yomiuri.co.jp/sitemap-news-past-3.xml",
        "https://www.yomiuri.co.jp/sitemap-news-past-4.xml",
        "https://www.yomiuri.co.jp/sitemap-news-past-5.xml",
        "https://www.yomiuri.co.jp/sitemap-news-past-6.xml",
        "https://www.yomiuri.co.jp/sitemap-news-past-7.xml",
    ]
    # sitemap_urls: list = ['https://www.yomiuri.co.jp/sitemap.xml']
    # sitemap_urls: list = ['https://www.yomiuri.co.jp/sitemap-news-past-1.xml']
    _domain_name: str = "yomiuri_co_jp"  # 各種処理で使用するドメイン名の一元管理
    _spider_version: float = 1.0

    # https://www.yomiuri.co.jp/sitemap-pt-post-2021-09-04.xml
    # sitemap_follow = ['/sitemap-pt-post-']
    # https://www.yomiuri.co.jp/sitemap-news-latest.xml
    ###一時にOFF ########################sitemap_follow = ['/sitemap-news-latest']

    sitemap_type = "google_news_sitemap"  # googleのニュースサイトマップ用にカスタマイズしたタイプ

    known_pagination_css_selectors: list[str] = [
        ".p-article-wp-pager a[href]",
    ]

    # selenium_mode: bool = True
    # sitemap_rules = [(r'.*', 'selenium_parse')]
