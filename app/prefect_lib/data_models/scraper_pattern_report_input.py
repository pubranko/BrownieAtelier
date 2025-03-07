from datetime import datetime
from typing import Any, Final, Literal, Optional, Tuple

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel, Field, validator


############################################
# 定数
# ※クラス内で定義したかったが、その場合クラス内で参照できなかった。
#   次善の策としてモジュール定数側で定義。
############################################
class ScraperPatternReportConst:
    START_TIME: Final[str] = "start_time"
    REPORT_TERM: Final[str] = "report_term"
    BASE_DATE: Final[str] = "base_date"
    REPORT_TERM__DAILY: Final[str] = "daily"
    REPORT_TERM__WEEKLY: Final[str] = "weekly"
    REPORT_TERM__MONTHLY: Final[str] = "monthly"
    REPORT_TERM__YEARLY: Final[str] = "yearly"


class ScraperPatternReportInput(BaseModel):
    """
    start_time,report_term,base_date
    """

    start_time: datetime = Field(..., title="開始時間")
    report_term: str = Field(..., title="レポート期間")
    base_date: Optional[datetime] = None

    def __init__(self, **data: Any):
        """
        あとで
        """
        super().__init__(**data)

    """
    定義順にチェックされる。
    valuesにはチェック済みの値のみが入るため順序は重要。(単項目チェック、関連項目チェックの順で定義するのが良さそう。)
    """

    ##################################
    # 単項目チェック、省略時の値設定
    ##################################
    @validator(ScraperPatternReportConst.START_TIME)
    def start_time_check(cls, value: datetime, values: dict) -> datetime:
        if value:
            assert isinstance(value, datetime), "日付型以外がエラー"
        return value

    @validator(ScraperPatternReportConst.REPORT_TERM)
    def report_term_check(cls, value: str, values: dict) -> str:
        if value:
            assert isinstance(value, str), "文字列型以外がエラー"
            # 本番には3ヶ月以上のデータ残さないからyearlyはいらないかも、、、
            if value not in [
                ScraperPatternReportConst.REPORT_TERM__DAILY,
                ScraperPatternReportConst.REPORT_TERM__WEEKLY,
                ScraperPatternReportConst.REPORT_TERM__MONTHLY,
                ScraperPatternReportConst.REPORT_TERM__YEARLY,
            ]:
                raise ValueError(
                    f"レポート期間の指定ミス。{ScraperPatternReportConst.REPORT_TERM__DAILY}, {ScraperPatternReportConst.REPORT_TERM__WEEKLY}, {ScraperPatternReportConst.REPORT_TERM__MONTHLY}, {ScraperPatternReportConst.REPORT_TERM__YEARLY}で入力してください。"
                )
        return value

    @validator(ScraperPatternReportConst.BASE_DATE)
    def base_date_check(
        cls, value: Optional[datetime], values: dict
    ) -> Optional[datetime]:
        if value:
            assert isinstance(value, datetime), "日時型以外がエラー"
        return value

    ###################################
    # 関連項目チェック
    ###################################

    #####################################
    # カスタマイズデータ
    #####################################
    def base_date_get(self) -> Tuple[datetime, datetime]:
        """
        レポート期間(report_term)と基準日(base_date)を基に基準期間(base_date_from, base_date_to)を取得する。
        ※基準日(base_date)=基準期間to(base_date_to)となる。
        """
        start_time: datetime = self.start_time
        # base_date = self.base_date
        if self.base_date:
            base_date_to = self.base_date
        else:
            base_date_to = start_time.replace(hour=0, minute=0, second=0, microsecond=0)

        if self.report_term == ScraperPatternReportConst.REPORT_TERM__DAILY:
            base_date_from = base_date_to - relativedelta(days=1)
        elif self.report_term == ScraperPatternReportConst.REPORT_TERM__WEEKLY:
            base_date_from = base_date_to - relativedelta(weeks=1)
        elif self.report_term == ScraperPatternReportConst.REPORT_TERM__MONTHLY:
            base_date_from = base_date_to - relativedelta(months=1)
        else:
            base_date_from = base_date_to - relativedelta(years=1)

        return (base_date_from, base_date_to)
