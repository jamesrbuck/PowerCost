"""
Handles database activities.
"""

import logging
import mysql.connector
from mysql.connector import Error

class PonderosaDB:
    """
    A single class that handles database activities.
    """
    def __init__(self, db_config):
        """
        Initializes the database connection manager.
        """
        self.db_config = db_config
        self.conn = None

    def __enter__(self):
        """
        Connect to the database when PonderosaDB class is instantiated.
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Automatically close connection on context exit of PonderosaDB class.
        """
        self.close()

    def connect(self):
        """
        Establish a new connection to the database.
        """
        try:
            self.conn = mysql.connector.connect(**self.db_config)
            if not self.conn.is_connected():
                raise ConnectionError("Connection to MySQL failed.")
            logging.info("PEU: Database connection established")
        except Error as err:
            logging.error("PEU: Database connection error: %s", err)
            raise

    def close(self):
        """
        Close the connection if it is open.
        """
        if self.conn and self.conn.is_connected():
            self.conn.close()
            logging.debug("PEU: Database connection closed.")

    def insert_usage(self, date_str, hour_str, kwh):
        """
        Insert an hourly usage record into the database.

        Parameters:
        - date_str: Date in 'YYYY-MM-DD' format
        - hour_str: Time in 'HH:00:00' format
        - kwh: Decimal or float kWh value
        """
        if not self.conn or not self.conn.is_connected():
            raise RuntimeError("Database not connected.")

        insert_stmt = (
            "INSERT INTO usage_e (UDate, UTime, kWh) "
            "VALUES (%s, %s, %s)"
        )
        values = (date_str, hour_str, kwh)

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(insert_stmt, values)
                self.conn.commit()
                logging.debug(
                    "PEU: INSERT: insert_stmt = %s, values = date_str=%s, hour_str=%s, kwh=%s",
                    insert_stmt, date_str, hour_str, kwh)
        except Error as err:
            logging.error("Failed to insert usage data: %s", err)
            self.conn.rollback()
            raise

    def __str__(self):
        '''
        Return setting as a string for debugging.
        '''
        return (
            f"DB User = {self.db_config.get('user')}, "
            f"Host = {self.db_config.get('host')}, "
            f"Database = {self.db_config.get('database')}"
        )
