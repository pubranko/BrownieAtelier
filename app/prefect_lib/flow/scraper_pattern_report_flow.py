import os
import sys
from datetime import datetime
# from prefect import Flow
# from prefect import Flow, task, Parameter
from prefect.core.flow import Flow
from prefect.core.parameter import Parameter
from prefect.core.parameter import DateTimeParameter
from prefect.tasks.control_flow.conditional import ifelse
from prefect.engine import signals
from prefect.utilities.context import Context
path = os.getcwd()
sys.path.append(path)
from prefect_lib.common_module.flow_status_change import flow_status_change
from prefect_lib.task.scraper_pattern_report_task import ScrapyingPatternReportTask

'''
各スクレイピング項目の抽出パターンの使用状況をレポートとして出力する。
'''
with Flow(
    name='[STATS_003] Scraper pattern info report flow',
    state_handlers=[flow_status_change],
) as flow:
    report_term = Parameter('report_term', default='weekly', required=True)()   # レポート期間 : daily, weekly, monthly, yearly
    base_date = DateTimeParameter('base_date', required=False,)
    task = ScrapyingPatternReportTask()
    result = task(report_term=report_term,
                  base_date=base_date,)