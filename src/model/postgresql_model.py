# -*- coding:utf-8 -*-
'''
Author: Zella
Date: 2022-09-14 00:02:12
LastEditors: Zella
LastEditTime: 2022-09-20 13:19:48
FilePath: /databricks-loader-python/src/model/postgresql_model.py
Description: postgresql singleton model
'''
import psycopg2
import psycopg2.extras
import logging


class Singleton(type):
    """
    @description: Singleton
    """
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance


class PostgreSQLModel(metaclass=Singleton):
    """
    @description: DatabricksModel
    """

    # database: the database name (only as keyword argument)
    # user: user name used to authenticate
    # password: password used to authenticate
    # host: database host address (defaults to UNIX socket if not provided)
    # port: connection port number (defaults to 5432 if not provided)
    def __init__(self, database, user, password, host, port):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = psycopg2.connect(database=database,
                                           user=user,
                                           password=password,
                                           host=host,
                                           port=port)

    def get_conn(self):
        '''
        description: use connection
        '''
        return self.connection

    def reconnect(self):
        '''
        description: reconnect connection
        '''
        self.connection = psycopg2.connect(database=self.database,
                                           user=self.user,
                                           password=self.password,
                                           host=self.host,
                                           port=self.port)
        return self.connection

    def select(self, columns, table_name, where_sql):
        """
        @description: query data for columns
        """
        try:
            ssql = "SELECT {} FROM {} WHERE {}".format(
                columns, table_name, where_sql)
            cursor = self.connection.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute(ssql)
            result = cursor.fetchall()
            return result
        except Exception as ex:
            logging.exception(ex)
        finally:
            cursor.close()

    def select_raw(self, query):
        """
        @description: query data for raw statement
        """
        cursor = self.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def insertmany_duplicate(self, columns, table_name, values, duplicate_columns):
        """
        @description: insert or duplicate update multiple rows
        """
        # INSERT INTO table (id, field, field2) VALUES (1, A, X), (2, B, Y), (3, C, Z)
        # ON DUPLICATE KEY UPDATE field=VALUES(Col1), field2=VALUES(Col2);
        pass
