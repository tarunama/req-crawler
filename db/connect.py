import pymysql

from settings.develop import DB_SETTINGS, DB_TABLES, DB_ROWS


class ConnectDB:

    def __init__(self, settings=DB_SETTINGS):
        self._connection = pymysql.connect(**settings)
        self.cursor = self._connection.cursor()
        db = DB_SETTINGS.get('db')
        if db:
            self.cursor.execute('use {0}'.format(db))
        table_count = self.cursor.execute('show tables')
        if table_count == 0:
            self.create_init_table()

    def create_init_table(self):
        tables = DB_TABLES
        for table in tables:
            try:
                cols = DB_ROWS.get(table)
                cols_str = ','.join(cols)
                sql = "CREATE TABLE {0}({1});".format(table, cols_str)
                self.cursor.execute(sql)
            except:
                self.close()

    def close(self):
        try:
            self.cursor.close()
            self._connection.close()
        except:
            raise Exception


if __name__ == '__main__':
    c = ConnectDB()
    c.close()
