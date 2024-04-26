import configparser
import os

DEFAULT_CONFIG = '../config/config.ini'  # requires absolute path


class ConfigParser:
    def __init__(self, path=None):
        if path is None:
            self.path = DEFAULT_CONFIG
        else:
            self.path = path
        if not os.path.exists(self.path):
            print(f"config file not found {self.path}")
            exit(1)

        self.cfg = configparser.ConfigParser()
        self.refresh()

    def refresh(self):
        self.cfg.read(self.path)

    def get_val(self, section, option, default=None):
        if not self.cfg.has_option(section=section, option=option):
            return default
        return self.cfg.get(section=section, option=option)

    def get_val_as_array(self, section, option, default=None):
        if not self.cfg.has_option(section=section, option=option):
            return default
        tmp_str = self.cfg.get(section=section, option=option)
        return tmp_str.split(';')

    def get_val_as_int(self, section, option, default=None):
        if not self.cfg.has_option(section=section, option=option):
            return default
        return int(self.cfg.get(section=section, option=option))

    def get_val_as_bool(self, section, option, default=None):
        res = False
        val = self.get_val(section=section, option=option, default=default)
        if str(val).lower() == 'true':
            res = True
        return res
