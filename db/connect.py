import pymysql

from settings.develop import DB_SETTINGS


# DB との接続を確立する
class ConnectDB:

    def __init__(self, settings=DB_SETTINGS):
        self._connection = self._connect(settings)

    def _connect(self, settings):
        return pymysql.connect(**settings)


if __name__ == '__main__':
    print(ConnectDB())
