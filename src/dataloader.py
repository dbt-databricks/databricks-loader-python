# -*- coding:utf-8 -*-
'''
Author: Zella
Date: 2022-09-13 12:52:40
LastEditors: Zella
LastEditTime: 2022-09-19 04:52:45
FilePath: /databricks-loader-python/src/dataloader.py
Description: 
'''
import os
import time
import setting
import logging
from model.postgresql_model import PostgreSQLModel
from model.databricks_model import DatabricksModel
from service.opensea_trades import OpenseaTrades

from apscheduler.schedulers.blocking import BlockingScheduler


logging.basicConfig(level=logging.INFO,  # 控制台打印的日志级别
                    filename=setting.Settings["logpath"] + "/schedule.log",
                    filemode='a',
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    )


def online_task():
    index = OpenseaTrades().online_dump()
    OpenseaTrades().online_load(index)


if __name__ == '__main__':
    setting.load_settings(env="production")
    scheduler = BlockingScheduler()

    # 每10分钟在线执行任务
    scheduler.add_job(online_task, 'cron', minute='*/10')

    # try:
    #     scheduler.start()
    # except (KeyboardInterrupt, SystemExit) as ex:
    #     logging.exception(ex)

    # 离线任务
    OpenseaTrades().offline_dump(start_date="2022-01-01 00:00:00",
                                 end_date="2022-09-18 00:00:00")

    OpenseaTrades().offline_load()

    while True:
        time.sleep(5)
        logging.info("just sleep for nothing")
