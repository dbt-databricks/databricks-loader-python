# -*- coding:utf-8 -*-
'''
Author: Zella
Date: 2022-09-13 15:09:19
LastEditors: Zella
LastEditTime: 2022-09-20 15:00:27
FilePath: /databricks-loader-python/src/service/opensea_trades.py
Description:
'''
import json
import os
import sys
import time
import logging
import setting
import psycopg2
from model.postgresql_model import PostgreSQLModel
from model.databricks_model import DatabricksModel


class OpenseaTrades(object):
    """
    @description: opensea_trades
    """

    def __init__(self):
        pass

    def offline_dump(self, start_date, end_date):
        # 1. query if history data exists
        if not os.path.exists(setting.Settings["datapath"] + "/offline"):
            os.makedirs(setting.Settings["datapath"] + "/offline")
        # 2. load history data utill
        dbt_model = DatabricksModel(**setting.DATABRICKS_SETTINGS)
        pg_model = PostgreSQLModel(**setting.POSTGRESQL_SETTINGS)
        count_result = dbt_model.select_raw(
            """SELECT date_format(block_time, 'yyyy-MM-dd') as date, count(*) as count \
            FROM opensea_trades WHERE block_time > '%s' AND block_time < '%s' \
            GROUP BY date SORT BY date"""
            % (start_date, end_date)
        )

        for row in count_result:
            row_dict = row.asDict()
            try:
                conn = pg_model.get_conn()
                cur = conn.cursor()
            except psycopg2.InterfaceError as ex:
                logging.exception(ex)
                # reconnect to database
                pg_model.reconnect()
            try:
                start = row_dict["date"] + " 00:00:00"
                end = row_dict["date"] + " 23:59:59"
                res = pg_model.select_raw(
                    """SELECT COUNT(*) FROM opensea_trades \
                    WHERE block_time >= timestamp '%s' AND block_time <= timestamp '%s'"""
                    % (start, end)
                )
                if not res:
                    continue
                pg_cnt = res[0]["count"]
                if pg_cnt == row_dict["count"]:
                    logging.info(
                        "date=%s no changes. databricks.count=%d postgresql.count=%d", row_dict["date"], row_dict["count"], pg_cnt)
                    continue
                logging.info(
                    "date=%s need update. databricks.count=%d postgresql.count=%d", row_dict["date"], row_dict["count"], pg_cnt)

                file_path = setting.Settings["datapath"] + \
                    "/offline/opensea_trades_%s.csv.loading" % row_dict["date"]
                fw = open(file_path, "w", encoding="utf-8")
                # dumps文件
                base_ts = time.mktime(time.strptime(
                    row_dict["date"], "%Y-%m-%d"))
                if 0 < row_dict["count"] < 5000:
                    # 整天
                    step = 1440
                    interval = list(range(0, 1441, int(step)))
                elif 5000 <= row_dict["count"] < 10000:
                    # 半天
                    step = 1440 / 2
                    interval = list(range(0, 1441, int(step)))
                elif 10000 <= row_dict["count"] < 50000:
                    step = 1440 / 12
                    interval = list(range(0, 1441, int(step)))
                else:
                    step = 1440 / 24
                    interval = list(range(0, 1441, int(step)))

                interval_date = [time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime(base_ts + x * 60)) for x in interval]
                for i in range(0, len(interval_date)-1):
                    ss = interval_date[i]
                    ee = interval_date[i+1]
                    res = dbt_model.select_raw(
                        """SELECT * FROM opensea_trades \
                        WHERE block_time >= '%s' AND block_time < '%s' \
                        """ % (ss, ee)
                    )
                    logging.info("[%s, %s] per_count=%d", ss, ee, len(res))
                    for r in res:
                        format_str = ",".join(["{}"] * 24) + "\n"
                        nft_project_name = r["nft_project_name"]
                        if r["nft_project_name"] is not None:
                            if r["nft_project_name"].find(',') != -1:
                                nft_project_name = r["nft_project_name"].replace(
                                    ',', ' ')
                        write_str = format_str.format(
                            r.tx_hash,
                            r.blockchain,
                            r.platform,
                            r.nft_token_id,
                            r.exchange_contract_address,
                            r.nft_contract_address,
                            r.erc_standard,
                            r.aggregator,
                            r.number_of_items,
                            r.trade_type,
                            r.buyer,
                            r.seller,
                            nft_project_name,
                            0 if r.currency_amount is None else r.currency_amount,
                            0 if r.usd_amount is None else r.usd_amount,
                            0 if r.eth_amount is None else r.eth_amount,
                            0 if r.original_currency_amount is None else r.original_currency_amount,
                            r.currency_symbol,
                            r.currency_contract,
                            r.original_currency_contract,
                            r.block_time,
                            r.block_number,
                            r.tx_from,
                            r.tx_to)
                        fw.write(write_str)
                fw.close()
                finish_path = file_path.strip(".loading")
                os.rename(file_path, finish_path)
            except Exception as ex:
                logging.exception(ex)
                with open(setting.Settings["datapath"] + "/offline/opensea_trades_%s.fail" %
                          row_dict["date"], 'a+', encoding='utf-8') as fail:
                    fail.write(repr(ex))

    def online_dump(self):
        # 1. query postgresql database lastest time
        # 查询当前postgresql数据库最新的数据
        baseline = time.strftime(
            "%Y-%m-%d", time.localtime(int(time.time())))
        baseline_datetime = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.strptime(baseline, "%Y-%m-%d"))
        baseline_timestamp = time.mktime(time.strptime(baseline, "%Y-%m-%d"))
        dbt_model = DatabricksModel(**setting.DATABRICKS_SETTINGS)
        pg_model = PostgreSQLModel(**setting.POSTGRESQL_SETTINGS)
        res = pg_model.select_raw(
            """SELECT max(block_time) as latest_time FROM opensea_trades \
            WHERE block_time >= timestamp '%s'
            """ % baseline_datetime
        )
        if not res:
            return

        latest_time = res[0]["block_time"]

        # 2. load history data from lastest_time to now_time
        # 存下postgresql数据库最新的数据 和 当前时间之间的这段数据

        if not os.path.exists(setting.Settings["datapath"] + "/online"):
            os.makedirs(setting.Settings["datapath"] + "/online")

        start_time = latest_time
        end_time = time.time()  # now_time
        index = int(end_time - baseline_timestamp) // int(10 * 60)

        res = dbt_model.select_raw(
            """SELECT * FROM opensea_trades \
            WHERE block_time >= '%s' AND block_time < '%s' \
            """ % (start_time, end_time)
        )
        logging.info("[%s, %s] row_count=%d", start_time, end_time, len(res))
        fw = open(setting.Settings["datapath"] + "/online/opensea_trades_%s_%d.csv" % (
            baseline, index), "w", encoding="utf-8")
        for r in res:
            format_str = ",".join(["{}"] * 24) + "\n"
            nft_project_name = r["nft_project_name"]
            if r["nft_project_name"] is not None:
                if r["nft_project_name"].find(',') != -1:
                    nft_project_name = r["nft_project_name"].replace(
                        ',', ' ')
            write_str = format_str.format(
                r.tx_hash,
                r.blockchain,
                r.platform,
                r.nft_token_id,
                r.exchange_contract_address,
                r.nft_contract_address,
                r.erc_standard,
                r.aggregator,
                r.number_of_items,
                r.trade_type,
                r.buyer,
                r.seller,
                nft_project_name,
                0 if r.currency_amount is None else r.currency_amount,
                0 if r.usd_amount is None else r.usd_amount,
                0 if r.eth_amount is None else r.eth_amount,
                0 if r.original_currency_amount is None else r.original_currency_amount,
                r.currency_symbol,
                r.currency_contract,
                r.original_currency_contract,
                r.block_time,
                r.block_number,
                r.tx_from,
                r.tx_to)
            fw.write(write_str)
        fw.close()
        return index

    def offline_load(self):
        '''
        description: 加载离线文件到db
        # 导入数据(可能多个文件)
        # 文件改名标记bak
        '''
        data_path = setting.Settings["datapath"] + "/offline"
        for files in os.listdir(data_path):
            ss = time.time()
            if files.endswith("succ") or files.endswith("fail") or files.endswith("loading"):
                logging.info("offline load skip %s", files)
                continue
            file_path = os.path.join(data_path, files)
            pg_model = PostgreSQLModel(**setting.POSTGRESQL_SETTINGS)
            try:
                conn = pg_model.get_conn()
                cur = conn.cursor()
                with open(file_path, "r", encoding="utf-8") as f:
                    # next(f)  # Skip the header row.
                    cur.copy_from(f, 'opensea_trades', sep=',')
                conn.commit()
                os.remove(file_path)
                with open(file_path + ".succ", 'a+', encoding='utf-8') as succ:
                    succ.truncate(0)
                logging.info("load %s cost: %.6f", files, time.time() - ss)
            except psycopg2.InterfaceError as ex:
                logging.exception(ex)
                # reconnect to database
                conn = pg_model.reconnect()
                cur = conn.cursor()
                with open(file_path, "r", encoding="utf-8") as f:
                    cur.copy_from(f, 'opensea_trades', sep=',')
                conn.commit()
                os.remove(file_path)
                with open(file_path + ".succ", 'a+', encoding='utf-8') as succ:
                    succ.truncate(0)
                logging.info("load %s cost: %.6f", files, time.time() - ss)
            except Exception as ex:
                logging.exception(ex)
                os.rename(file_path, file_path + ".fail")
                logging.info("load %s fail", files)

    def online_load(self, index=-1):
        # 导入数据(可能多个文件)

        # 文件改名标记bak
        pass
