from prefect import task, get_run_logger
from prefect_lib.flows import START_TIME
from BrownieAtelierNotice.mail_send import mail_send


@task
def sync_check_notice_result_task(
        response_async_list: list,
        response_async_domain_aggregate: dict,
        master_async_list: list,
        master_async_domain_aggregate: dict,
        solr_async_list: list,
        solr_async_domain_aggregate: dict):
    '''各同期チェック結果にエラーがあった場合メールで通知'''

    # ロガー取得
    logger = get_run_logger()   # PrefectLogAdapter

    title: str = f'【クローラー同期チェック：非同期発生】{START_TIME.isoformat()}'
    message: str = ''
    # クロールミス分のurlがあれば
    if len(response_async_list) > 0:
        # メール通知用メッセージ追記
        message = f'{message}以下のドメインでクローラーで対象となったにもかかわらず、crawler_responseに登録されていないケースがあります。\n'
        for item in response_async_domain_aggregate.items():
            if item[1] > 0:
                message = message + item[0] + ' : ' + str(item[1]) + ' 件\n'

    # スクレイピングミス分のurlがあれば
    if len(master_async_list) > 0:
        # メール通知用メッセージ追記
        message = f'{message}以下のドメインでcrawler_responseにあるにもかかわらず、news_clip_master側に登録されていないケースがあります。\n'
        for item in master_async_domain_aggregate.items():
            if item[1] > 0:
                message = message + item[0] + ' : ' + str(item[1]) + ' 件\n'

    # solrへの送信ミス分のurlがあれば
    if len(solr_async_list) > 0:
        # メール通知用メッセージ追記
        message = f'{message}以下のドメインでnews_clip_masterにあるにもかかわらず、solr_news_clip側に登録されていないケースがあります。\n'
        for item in solr_async_domain_aggregate.items():
            if item[1] > 0:
                message = message + item[0] + ' : ' + str(item[1]) + ' 件\n'

    # エラーがあった場合エラー通知を行う。
    if not message == '':
        mail_send(title, message, logger)
