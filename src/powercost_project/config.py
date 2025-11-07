"""
This modules contains both config class: DatabaseConfig and SetupConfig.
"""

import os
from configparser import ConfigParser, NoSectionError, NoOptionError
import logging

class DatabaseConfig:
    """
    MySQL database configuration settings.
    """
    def __init__(self, config):
        try:
            #self.user = config.get('database', 'dbUser')
            #self.password = config.get('database', 'dbPassword')

            self.user     = os.getenv("POWERCOST_USER")
            self.password = os.getenv("POWERCOST_PASS")
            if (self.user is None or self.password is None):
                raise Exception("ERROR: $POWERCOST_USER and/or $POWERCOST_PASS is not set in env!")

            self.host = config.get('database', 'dbHost')
            self.name = config.get('database', 'dbName')
            self.raise_on_warnings = config.getboolean('database', 'dbRaiseOnWarnings')
        except (NoSectionError, NoOptionError) as e:
            logging.error("DatabaseConfig error: %s", e)
            raise

    def as_dict(self):
        """
        It returns a dictionary of database settings for debugging
        purposes for debugging purposes
        """
        return {
            'user': self.user,
            'password': self.password,
            'host': self.host,
            'database': self.name,
            'raise_on_warnings': self.raise_on_warnings
        }


class SetupConfig:
    """
    Class to handle logging, port configuration settings.
    """
    def __init__(self, config, start_ts):
        try:
            self.log_dir = config.get('setup', 'log_dir')
            self.log_file = f"PEU_{start_ts}_log.txt"
            self.port = config.get('setup', 'the_port')
            self.log_level = config.get('setup','log_level')
            self.running_file = config.get('setup','running_file')
            self.stop_file = config.get('setup','stop_file')
        except (NoSectionError, NoOptionError) as e:
            logging.error("SetupConfig error: %s", e)
            raise


class PonderosaConfig:
    """
    Class is the entry point into acquiring all configuration settings.  It references
    SetupConfig and DatabaseConfig.
    """
    def __init__(self, ini_file, start_ts):
        self.ini_file = ini_file
        self.start_ts = start_ts

        config = ConfigParser()
        config.read(ini_file)

        self.setup = SetupConfig(config, start_ts)
        self.database = DatabaseConfig(config)

    @property
    def running_file(self):
        """
        Returns: running_file
        """
        return self.setup.running_file

    @property
    def stop_file(self):
        """
        Returns: stop_file
        """
        return self.setup.stop_file

    @property
    def log_dir(self):
        """
        Returns: log_dir
        """
        return self.setup.log_dir

    @property
    def log_file(self):
        """
        Returns: log_file
        """
        return self.setup.log_file

    @property
    def log_level(self):
        """
        Returns: log_level
        """
        return self.setup.log_level

    @property
    def the_port(self):
        """
        Returns: port to EMU-2 device
        """
        return self.setup.port

    @property
    def db_config(self):
        """
        Returns: database configuration settings as a dictionary.
        """
        return self.database.as_dict()

    def __str__(self):
        return (
            f"log_dir = \"{self.log_dir}\"\n"
            f"log_file = \"{self.log_file}\"\n"
            f"the_port = \"{self.the_port}\"\n"
            f"startTS = \"{self.start_ts}\"\n"
            f"dbConfig = {self.db_config}"
        )
