# -*- coding:utf-8 -*-
'''
Author: Zella
Date: 2022-09-13 12:52:40
LastEditors: Zella
LastEditTime: 2022-09-14 11:08:52
FilePath: /databricks-loader-python/src/dataloader.py
Description: 
'''
import time
import setting
from model.postgresql_model import PostgreSQLModel
from model.databricks_model import DatabricksModel

if __name__ == '__main__':
    setting.load_settings(is_dev=True)
