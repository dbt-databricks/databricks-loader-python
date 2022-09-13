# -*- coding:utf-8 -*-
"""
@Author: Zella
@Date: 2022-09-13 14:18:05
@LastEditors: Zella
@LastEditTime: 2022-09-13 14:20:13
@FilePath: /databricks-loader-python/src/model/databricks_model.py
@Description: databricks singleton model
"""
from databricks import sql


class Singleton(type):
    """
    @description: Singleton
    """
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance


class DatabricksModel(metaclass=Singleton):
    """
    @description: DatabricksModel
    """

    def __init__(self, server_hostname, http_path, access_token, catalog, schema):
        self.connection = sql.connect(server_hostname=server_hostname,
                                      http_path=http_path,
                                      access_token=access_token,
                                      catalog=catalog,
                                      schema=schema
                                      )

    def select(self, columns, table_name, where_sql):
        """
        @description: query data for columns
        @return List[Row]
        """
        ssql = "SELECT {} FROM {} WHERE {}".format(
            columns, table_name, where_sql)
        cursor = self.connection.cursor()
        cursor.execute(ssql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def select_raw(self, query):
        """
        @description: query data for raw statement
        @return List[Row]
        """
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
