import pymysql

from settings.develop import DB_SETTINGS


class ConnectDB:

    def __init__(self, settings=DB_SETTINGS):
        self._connection = pymysql.connect(**settings)
        self.cursor = self._connection.cursor()

    def close(self):
        try:
            if self.cursor:
                self.cursor.close()

            if self._connection:
                self._connection.close()

        except:
            raise Exception


if __name__ == '__main__':
    c = ConnectDB()
    c.close()
