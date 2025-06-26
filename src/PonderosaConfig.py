import os
from configparser import ConfigParser, NoSectionError, NoOptionError
import logging

class DatabaseConfig:
    def __init__(self, config):
        try:
            self.user = config.get('database', 'dbUser')
            self.password = config.get('database', 'dbPassword')
            self.host = config.get('database', 'dbHost')
            self.name = config.get('database', 'dbName')
            self.raise_on_warnings = config.getboolean('database', 'dbRaiseOnWarnings')
        except (NoSectionError, NoOptionError) as e:
            logging.error(f"DatabaseConfig error: {e}")
            raise

    def as_dict(self):
        return {
            'user': self.user,
            'password': self.password,
            'host': self.host,
            'database': self.name,
            'raise_on_warnings': self.raise_on_warnings
        }


class SetupConfig:
    def __init__(self, config, start_ts):
        try:
            self.log_dir = config.get('setup', 'log_dir')
            self.log_file = f"PEU_{start_ts}_log.txt"
            self.port = config.get('setup', 'the_port')
        except (NoSectionError, NoOptionError) as e:
            logging.error(f"SetupConfig error: {e}")
            raise


class PonderosaConfig:
    def __init__(self, ini_file, start_ts):
        self.ini_file = ini_file
        self.start_ts = start_ts

        config = ConfigParser()
        config.read(ini_file)

        self.setup = SetupConfig(config, start_ts)
        self.database = DatabaseConfig(config)

    @property
    def log_dir(self):
        return self.setup.log_dir

    @property
    def log_file(self):
        return self.setup.log_file

    @property
    def the_port(self):
        return self.setup.port

    @property
    def dbConfig(self):
        return self.database.as_dict()

    def __str__(self):
        return (
            f"log_dir = \"{self.log_dir}\"\n"
            f"log_file = \"{self.log_file}\"\n"
            f"the_port = \"{self.the_port}\"\n"
            f"startTS = \"{self.start_ts}\"\n"
            f"dbConfig = {self.dbConfig}"
        )
