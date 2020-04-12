import pymysql


class DataBase:
    def __init__(self, host, username, password, database, port):
        self.connection_data = {
            'host': host,
            'username': username,
            'password': password,
            'database': database,
            'port': port
        }
        self.connection = self.cursor = None

    def connect(self):
        self.connection = pymysql.connect(
            self.connection_data['host'],
            self.connection_data['username'],
            self.connection_data['password'],
            self.connection_data['database'],
            self.connection_data['port']
        )
        self.cursor = self.connection.cursor()
        return self.cursor, self.connection

    def __default_check(self, check_var=None, check_type=None):
        self.connect()
        if check_var is None:
            pass
        else:
            try:
                check_type(check_var)
            except:
                return False

        return True

    def add_user_to_bd(self, user_id, user_name):
        state = self.add_user_to_info(user_id)
        state2 = self.add_user_to_logged(user_id, user_name)
        return state and state2

    def add_user_to_info(self, user_id):
        state = self.check_user_in_info(user_id)
        if self.__default_check(user_id, int) and user_id is not None:
            try:
                with self.cursor as cursor:
                    if not state:
                        cursor.execute("""INSERT INTO `user_info` (UserID)
                                                 VALUES ({})""".format(user_id))
                        self.connection.commit()
                        return True
                    else:
                        return False
            except:
                return False

    def add_user_to_logged(self, user_id, user_name):
        state = self.check_user_logged(user_id)
        if self.__default_check(user_id, int) and user_id is not None:
            try:
                with self.cursor as cursor:
                    if not state:
                        cursor.execute("""INSERT INTO `logged_users` (UserID, UserName)
                                         VALUES ({}, '{}')""".format(user_id, user_name))
                        self.connection.commit()
                        return True
                    else:
                        return False

            except:
                return False

    def check_user_in_info(self, user_id):
        if self.__default_check(user_id, int) and user_id is not None:
            with self.cursor as cursor:
                cursor.execute("""SELECT ID FROM `user_info` WHERE UserID={}""".format(user_id))

            row = cursor.fetchall()
            if len(row):
                return True

        return False

    def check_user_logged(self, user_id):
        if self.__default_check(user_id, int) and user_id is not None:
            with self.cursor as cursor:
                cursor.execute("""SELECT ID FROM `logged_users` WHERE UserID={}""".format(user_id))

            row = cursor.fetchall()
            if len(row):
                return True

        return False

    def get_user_city(self, user_id):
        if self.__default_check(user_id, int) and id is not None:
            with self.cursor as cursor:
                cursor.execute("""SELECT UserCity, UserRegion FROM `user_info` WHERE UserID={}""".format(user_id))

            row = cursor.fetchone()
            if row is not None and row[0] is not None and row[1] is None:
                return row[0], False
            elif row is not None and row[0] is not None and row[1] is not None:
                return row
        return False

    def get_user_state(self, user_id):
        if self.__default_check(user_id, int) and id is not None:
            with self.cursor as cursor:
                cursor.execute("""SELECT UserState FROM `user_info` WHERE UserID={}""".format(user_id))

            row = cursor.fetchone()
            if row is not None:
                return row[0]

        return False

    def set_user_state(self, user_id, state):
        if self.__default_check(user_id, int) and user_id is not None:
            try:
                state = int(state)
                with self.cursor as cursor:
                    cursor.execute("""UPDATE `user_info` SET UserState={} WHERE UserID={}""".format(state, user_id))
                    self.connection.commit()
                    return True
            except:
                return False

        return False

