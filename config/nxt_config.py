from config.parser import ConfigParser


class NXTConfig:

    def __init__(self, path=None):
        self.parser = ConfigParser(path=path)

        ################################################################################################################
        # DEFAULT
        ################################################################################################################
        self.ip = self.parser.get_val("DEFAULT", "IP", None)
        self.user = self.parser.get_val("DEFAULT", "USER", None)
        self.password = self.parser.get_val("DEFAULT", "PASSWORD", None)

