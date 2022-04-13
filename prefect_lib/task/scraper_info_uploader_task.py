import os
import sys
import glob
import json
from prefect.engine import state
from prefect.engine.runner import ENDRUN
from pydantic import ValidationError
path = os.getcwd()
sys.path.append(path)
from prefect_lib.settings import SCRAPER_INFO_BY_DOMAIN_DIR
from prefect_lib.task.extentions_task import ExtensionsTask
from prefect_lib.data_models.scraper_info_by_domain_data import ScraperInfoByDomainData
from models.scraper_info_by_domain_model import ScraperInfoByDomainModel


class ScraperInfoUploaderTask(ExtensionsTask):
    '''
    '''

    def run(self, **kwargs):
        ''''''
        self.logger.info(f'=== ScraperInfoUploaderTask run kwargs : {str(kwargs)}')

        scraper_info_by_domain_model = ScraperInfoByDomainModel(self.mongo)

        #scraper_info_by_domain_files: list = kwargs['scraper_info_by_domain_files']
        scraper_info_by_domain_files: list = []
        files: list = kwargs['scraper_info_by_domain_files']
        if len(kwargs['scraper_info_by_domain_files']) == 0:
            path = os.path.join(SCRAPER_INFO_BY_DOMAIN_DIR, '*.json')
            scraper_info_by_domain_files = glob.glob(path)
            self.logger.info(
                f'=== ScraperInfoUploaderTask run ファイル指定なし → 全ファイル対象 : {scraper_info_by_domain_files}')
        else:
            for file in files:
                scraper_info_by_domain_files.append(
                    os.path.join(SCRAPER_INFO_BY_DOMAIN_DIR, file))

        if len(scraper_info_by_domain_files) == 0:
            raise ENDRUN(state=state.Failed())

        for file_name in scraper_info_by_domain_files:
            self.logger.info(
                f'=== ScraperInfoUploaderTask run ファイルチェック : {file_name}')
            with open(file_name, 'r') as f:
                file = f.read()

            scraper_info: dict = json.loads(file)

            try:
                ScraperInfoByDomainData(scraper=scraper_info)
            except ValidationError as e:
                error_info: list = e.errors()
                self.logger.error(
                    f'=== ScraperInfoUploaderTask run エラー({file_name}) : {error_info[0]["msg"]}')
            else:
                scraper_info_by_domain_model.update(
                    filter={'domain': scraper_info['domain']},
                    record=scraper_info)

            # 処理の終わったファイルオブジェクトを削除
            del file, scraper_info

        # 終了処理
        self.closed()
        # return ''