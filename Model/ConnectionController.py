import sqlite3


class ConnectionController:
    def __init__(self):
        self.__required_for_connection = 0
        self.__connection = None

    def require_connection(self, base_address):
        if self.__required_for_connection == 0:
            self.__connection = sqlite3.connect(base_address)
        self.__required_for_connection += 1
        return self.__connection.cursor()

    def drop_connection(self):
        self.__required_for_connection -= 1
        if self.__required_for_connection == 0:
            self.__connection.commit()
            self.__connection.close()


if __name__ == "__main__":
    pass
