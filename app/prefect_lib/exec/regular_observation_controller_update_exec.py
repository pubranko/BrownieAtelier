from prefect_lib.flows.regular_observation_controller_update_flow import regular_observation_controller_update_flow
from prefect_lib.flows.regular_observation_controller_update_const import RegularObservationControllerUpdateConst

regular_observation_controller_update_flow(
    register = RegularObservationControllerUpdateConst.REGISTER_ADD,
    # register = RegularObservationControllerUpdateConst.REGISTER_DELETE,
    spiders_name=[
        # 'asahi_com_sitemap',
        # 'epochtimes_jp_crawl',
        # 'jp_reuters_com_crawl',
        # 'kyodo_co_jp_sitemap',
        # 'mainichi_jp_crawl',
        # 'nikkei_com_crawl',
        'sankei_com_sitemap',
        # 'yomiuri_co_jp_sitemap',
    ],
)
