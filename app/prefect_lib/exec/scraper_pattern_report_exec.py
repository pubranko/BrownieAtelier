from datetime import datetime

# from prefect_lib.flow.scraper_pattern_report_flow import flow
from prefect_lib.flows.scraper_pattern_report_flow import \
    scraper_pattern_report_flow
from shared.settings import TIMEZONE

# flow.run(parameters=dict(
#     report_term='daily',
#     # report_term='weekly',
#     #report_term='monthly',
#     #report_term='yearly',
#     base_date=datetime(2023, 3, 20).astimezone(TIMEZONE),   # 左記基準日の前日分のデータが対象となる。
# ))

scraper_pattern_report_flow(
    # report_term='daily',
    # report_term='weekly',
    report_term="monthly",
    # report_term='yearly',
    base_date=datetime(2023, 6, 27).astimezone(TIMEZONE),  # 左記基準日の前日分のデータが対象となる。
)
