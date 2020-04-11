import pymysql


class DB:
    def __init__(self, host, username, password, database, port):
        self.connection_data = {
            'host': host,
            'username': username,
            'password': password,
            'database': database,
            'port': port
        }

    def __connect(self):
        self.connection = pymysql.connect(
            self.connection_data['host'],
            self.connection_data['username'],
            self.connection_data['password'],
            self.connection_data['database'],
            self.connection_data['port']
        )
        self.cursor = self.connection.cursor()

    def test(self):
        try:
            self.__connect()
        except pymysql.err.OperationalError:
            return False

        with self.cursor as cursor:
            cursor.execute("""SELECT * FROM `test`""")

        rows = cursor.fetchall()
        return rows
