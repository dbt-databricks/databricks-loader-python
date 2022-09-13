# -*- coding:utf-8 -*-
"""
@Author: Zella
@Date: 2022-09-13 12:52:40
@LastEditors: Zella
@LastEditTime: 2022-09-13 13:55:42
@FilePath: /databricks-loader-python/src/dataloader.py
@Description: main process
"""
import setting


if __name__ == '__main__':
    setting.load_settings(is_dev=True)
    print(setting.DATABRICKS_SETTINGS)
