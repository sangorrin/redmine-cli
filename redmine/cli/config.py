import configparser
import os

import click


class Config:
    def __init__(self, account=None):
        HOME = os.getenv("HOME")
        self.paths = [
            os.path.join(HOME, ".redmine.conf"),
            os.path.join(HOME, ".redmine/redmine.conf"),
            os.path.join(HOME, ".config/redmine/redmine.conf"),
        ]
        self.url = None
        self.api_key = None
        self.user_id = None
        self.password = None
        self.ssl_verify = True
        self.aliases = {}
        self.account = account

        URL = os.getenv("REDMINE_URL")
        API_KEY = os.getenv("REDMINE_API_KEY")
        if URL and API_KEY:
            self.url = URL
            self.api_key = API_KEY
        else:
            self.read_from_file()

    def read_from_file(self):
        config = configparser.ConfigParser()
        config.read(self.paths)

        if "accounts" not in config:
            raise FileNotFoundError(
                "Config file not found in {}".format(" or ".join(self.paths))
            )

        if self.account is None:
            self.account = config["accounts"]["default"]

        self.url = config[self.account]["url"]
        if "key" in config[self.account]:
            self.api_key = config[self.account]["key"]
        elif "user_id" in config[self.account]:
            self.user_id = config[self.account]["user_id"]
            if "password" in config[self.account]:
                self.password = config[self.account]["password"]
            else:
                raise KeyError("provide password for user %s", self.user_id)
        else:
            raise KeyError("key and user_id:password not found")
        self.ssl_verify = config[self.account].getboolean("ssl_verify")

        try:
            self.aliases.update(config.items("aliases"))
        except configparser.NoSectionError:
            pass

        return config


pass_config = click.make_pass_decorator(Config, ensure=True)
