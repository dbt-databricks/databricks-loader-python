# -*- coding:utf-8 -*-
"""
@Author: Zella
@Date: 2022-09-13 13:27:56
@LastEditors: Zella
@LastEditTime: 2022-09-13 13:41:19
@FilePath: /databricks-loader-python/src/setting/__init__.py
@Description: load configurations and global setting
"""
import logging
import toml


MAX_INT32 = 2147483647
MAX_UINT32 = 4294967295


INTERVAL = {
    (0, 5000): "Monthly",
    (5000, 10000): "HalfMonth",
    (10000, 50000): "Weekly",
    (50000, MAX_INT32): "Dayly",
}


DATABRICKS_SETTINGS = {
    "server_hostname": "",
    "http_path": "",
    "access_token": "",
    "catalog": "",
    "schema": "",
}


def load_settings(is_dev=False):
    """
    @description: load configurations from file
    """
    global INTERVAL
    global DATABRICKS_SETTINGS
    if is_dev:
        DATABRICKS_SETTINGS = load_databricks_settings(
            "./config/main.sample.toml")
    else:
        DATABRICKS_SETTINGS = load_databricks_settings(
            "./config/main.toml")


def load_databricks_settings(config_file):
    """
    @description: load databricks auth configurations
    @params: config_file
    @return databricks_settings
    """
    try:
        config = toml.load(config_file)
        databricks_settings = {
            "server_hostname": config["databricks"]["server_hostname"],
            "http_path": config["databricks"]["http_path"],
            "access_token": config["databricks"]["access_token"],
            "catalog": config["databricks"]["catalog"],
            "schema": config["databricks"]["schema"],
        }
        return databricks_settings
    except Exception as ex:
        logging.exception(ex)
