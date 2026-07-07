import mysql.connector

from sqlalchemy import create_engine
from sqlalchemy.engine import URL

from config.config import Config


class Database:

    def __init__(self):

        self.connection = None
        self.engine = None

    def connect(self):

        self.connection = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            port=int(Config.DB_PORT)
        )

        connection_url = URL.create(
            drivername="mysql+mysqlconnector",
            username=Config.DB_USER,
            password=Config.DB_PASSWORD,
            host=Config.DB_HOST,
            port=int(Config.DB_PORT),
            database=Config.DB_NAME,
        )

        self.engine = create_engine(connection_url)

        print("Connected to MySQL")

    def disconnect(self):

        if self.connection:
            self.connection.close()

        if self.engine:
            self.engine.dispose()