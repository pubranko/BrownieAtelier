from copy import deepcopy
from datetime import date, datetime, time
from typing import Any, Final, Literal, Optional, Tuple

from dateutil.relativedelta import relativedelta
from prefect_lib.flows import START_TIME
from pydantic import BaseModel, Field, validator
from shared.settings import TIMEZONE


############################################
# 定数
# ※クラス内で定義したかったが、その場合クラス内で参照できなかった。
#   次善の策としてモジュール定数側で定義。
############################################
class StatsAnalysisReportConst:
    """StatsAnalysisReportInputクラスに関する定数"""

    START_TIME: Final[str] = "start_time"
    REPORT_TERM: Final[str] = "report_term"
    TOTALLING_TERM: Final[str] = "totalling_term"
    BASE_DATE: Final[str] = "base_date"
    REPORT_TERM__DAILY: Final[str] = "daily"
    REPORT_TERM__WEEKLY: Final[str] = "weekly"
    REPORT_TERM__MONTHLY: Final[str] = "monthly"
    REPORT_TERM__YEARLY: Final[str] = "yearly"
    TOTALLING_TERM__DAILY: Final[str] = "daily"
    TOTALLING_TERM__WEEKLY: Final[str] = "weekly"
    TOTALLING_TERM__MONTHLY: Final[str] = "monthly"
    TOTALLING_TERM__YEARLY: Final[str] = "yearly"


class StatsAnalysisReportInput(BaseModel):
    report_term: str = Field(..., title="レポート期間")
    totalling_term: str = Field(..., title="集計期間")
    base_date: Optional[date] = None

    def __init__(self, **data: Any):
        """あとで"""
        super().__init__(**data)

    """
    定義順にチェックされる。
    valuesにはチェック済みの値のみが入るため順序は重要。(単項目チェック、関連項目チェックの順で定義するのが良さそう。)
    """

    ##################################
    # 単項目チェック、省略時の値設定
    ##################################
    @validator(StatsAnalysisReportConst.REPORT_TERM)
    def report_term_check(cls, value: str, values: dict) -> str:
        if value:
            assert isinstance(value, str), "文字列型以外がエラー"
            # 本番には3ヶ月以上のデータ残さないからyearlyはいらないかも、、、
            # if value not in ['daily', 'weekly', 'monthly', 'yearly']:
            if value not in [
                StatsAnalysisReportConst.REPORT_TERM__DAILY,
                StatsAnalysisReportConst.REPORT_TERM__WEEKLY,
                StatsAnalysisReportConst.REPORT_TERM__MONTHLY,
                StatsAnalysisReportConst.REPORT_TERM__YEARLY,
            ]:
                raise ValueError("レポート期間の指定ミス。daily, weekly, monthly, yearlyで入力してください。")
        return value

    @validator(StatsAnalysisReportConst.TOTALLING_TERM)
    def totalling_term_check(cls, value: str, values: dict) -> str:
        if value:
            assert isinstance(value, str), "文字列型以外がエラー"
            # 本番には3ヶ月以上のデータ残さないからyearlyはいらないかも、、、
            # if value not in ['daily', 'weekly', 'monthly', 'yearly']:
            if value not in [
                StatsAnalysisReportConst.TOTALLING_TERM__DAILY,
                StatsAnalysisReportConst.TOTALLING_TERM__WEEKLY,
                StatsAnalysisReportConst.TOTALLING_TERM__MONTHLY,
                StatsAnalysisReportConst.TOTALLING_TERM__YEARLY,
            ]:
                raise ValueError("レポート期間の指定ミス。daily, weekly, monthly, yearlyで入力してください。")
        return value

    ###################################
    # 関連項目チェック
    ###################################

    #####################################
    # カスタマイズデータ
    #####################################
    def base_date_get(self, start_time: datetime) -> Tuple[datetime, datetime]:
        """
        レポート期間(report_term)と基準日(base_date)を基に基準期間(base_date_from, base_date_to)を取得する。
        ※基準日(base_date)=基準期間to(base_date_to)となる。
        """
        # start_time: datetime = self.start_time
        # base_date = self.base_date
        if self.base_date:
            # base_date_to = self.base_date
            base_date_to = datetime.combine(self.base_date, time.min, TIMEZONE)
        else:
            base_date_to = start_time.replace(hour=0, minute=0, second=0, microsecond=0)

        if self.report_term == StatsAnalysisReportConst.REPORT_TERM__DAILY:
            base_date_from = base_date_to - relativedelta(days=1)
        elif self.report_term == StatsAnalysisReportConst.REPORT_TERM__WEEKLY:
            base_date_from = base_date_to - relativedelta(weeks=1)
        elif self.report_term == StatsAnalysisReportConst.REPORT_TERM__MONTHLY:
            base_date_from = base_date_to - relativedelta(months=1)
        else:
            base_date_from = base_date_to - relativedelta(years=1)

        return (base_date_from, base_date_to)

    def datetime_term_list(self) -> list[tuple[datetime, datetime]]:
        """
        レポート期間を集計期間単位で区切ったタプルを作成する。それをリストに格納して返す。
        [(from, to), (from, to),,,]
        """
        term_list: list[tuple[datetime, datetime]] = []
        base_date_from, base_date_to = self.base_date_get(START_TIME)

        if self.totalling_term == StatsAnalysisReportConst.TOTALLING_TERM__DAILY:
            term = relativedelta(days=1)
        elif self.totalling_term == StatsAnalysisReportConst.TOTALLING_TERM__WEEKLY:
            term = relativedelta(weeks=1)
        elif self.totalling_term == StatsAnalysisReportConst.TOTALLING_TERM__MONTHLY:
            term = relativedelta(months=1)
        else:
            term = relativedelta(years=1)

        calc_date_from = deepcopy(base_date_to) - term
        calc_date_to = deepcopy(base_date_to)
        while calc_date_from >= base_date_from:
            term_list.append((calc_date_from, calc_date_to))
            calc_date_from = calc_date_from - term
            calc_date_to = calc_date_to - term

        return term_list
