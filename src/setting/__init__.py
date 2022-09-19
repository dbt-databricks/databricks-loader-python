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
MONTH_SECORNDS = 2592000  # 24 * 60 * 60 * 30
YEAR_SECORNDS = 946080000  # 365 * MONTH_SECORNDS


INTERVAL = {
    (0, 5000): "Monthly",
    (5000, 10000): "HalfMonth",
    (10000, 50000): "Weekly",
    (50000, MAX_INT32): "Dayly",
}

Settings = {
    "datapath": "./data",
    "logpath": "./log"
}


DATABRICKS_SETTINGS = {
    "server_hostname": "",
    "http_path": "",
    "access_token": "",
    "catalog": "",
    "schema": "",
}

POSTGRESQL_SETTINGS = {
    "database": "",
    "user": "",
    "password": "",
    "host": "",
    "port": "",
}


def load_settings(env="test"):
    """
    @description: load configurations from file
    """
    global Settings
    global INTERVAL
    global DATABRICKS_SETTINGS
    global POSTGRESQL_SETTINGS

    config_file = "/var/task/dataloader/src/config/main.toml"
    if env == "test":
        config_file = "/var/task/dataloader/src/config/testing.toml"
    elif env == "dev":
        config_file = "./config/dev.toml"

    config = toml.load(config_file)
    Settings["datapath"] = config["path"]["datapath"]
    Settings["logpath"] = config["path"]["logpath"]
    DATABRICKS_SETTINGS = load_databricks_settings(config_file)
    POSTGRESQL_SETTINGS = load_postgresql_settings(config_file)


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


def load_postgresql_settings(config_file):
    """
    @description: load postgresql auth configurations
    @params: config_file
    @return postgresql_settings
    """
    try:
        config = toml.load(config_file)
        postgresql_settings = {
            "database": config["postgresql"]["database"],
            "user": config["postgresql"]["user"],
            "password": config["postgresql"]["password"],
            "host": config["postgresql"]["host"],
            "port": config["postgresql"]["port"],
        }
        return postgresql_settings
    except Exception as ex:
        logging.exception(ex)
