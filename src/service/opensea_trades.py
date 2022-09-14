# -*- coding:utf-8 -*-
'''
Author: Zella
Date: 2022-09-13 15:09:19
LastEditors: Zella
LastEditTime: 2022-09-14 11:08:36
FilePath: /databricks-loader-python/src/service/opensea_trades.py
Description:
'''
import json
import os
import sys
import time
import setting
from model.postgresql_model import PostgreSQLModel
from model.databricks_model import DatabricksModel


class OpenseaTrades(object):
    """
    @description: opensea_trades
    """

    def __init__(self):
        pass

    def offline_dump(self):
        # 1. query if history data exists
        end_date = time.strftime(
            "%Y-%m-%d", time.localtime(int(time.time()) - 1 * setting.MONTH_SECORNDS))
        end_datetime = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.strptime(end_date, "%Y-%m-%d"))

        start_date = time.strftime(
            "%Y-%m-%d", time.localtime(int(time.time()) - 6 * setting.MONTH_SECORNDS))
        start_datetime = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.strptime(start_date, "%Y-%m-%d"))

        pg_model = PostgreSQLModel(**setting.POSTGRESQL_SETTINGS)
        count_result = pg_model.select_raw(
            "SELECT COUNT(*) FROM opensea_trades WHERE block_time <= timestamp '%s'" % end_datetime)

        if not count_result:
            return

        count = count_result[0]["count"]
        if count > 0:
            return

        # 2. load history data utill
        dbt_model = DatabricksModel(**setting.DATABRICKS_SETTINGS)
        count_result = dbt_model.select_raw(
            """SELECT date_format(block_time, 'yyyy-MM') as date, count(*) as count \
            FROM opensea_trades WHERE block_time > '%s' AND block_time < '%s' \
            GROUP BY date SORT BY date"""
            % (start_datetime, end_datetime)
        )
        for row in count_result:
            print(row.asDict())

    def online_dump(self):
        # 1. query postgresql database lastest time
        # 查询当前postgresql数据库最新的数据

        # 2. load history data from lastest_time to now_time
        # 存下postgresql数据库最新的数据 和 当前时间之间的这段数据
        pass

    def offline_load(self):
        # 导入数据(可能多个文件)

        # 文件改名标记bak
        pass

    def online_load(self):
        # 导入数据(可能多个文件)

        # 文件改名标记bak
        pass
