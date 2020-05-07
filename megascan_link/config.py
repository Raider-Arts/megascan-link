import configparser
import os
import megascan_link
from megascan_link import utilities as util
from pathlib import Path

class ConfigSettings(object):
    path = Path(util.getAbsCurrentPath('megascanlink.ini'))
    config = configparser.ConfigParser()
    opened = False

    @classmethod
    def updateConfigSetting(cls, cat: str, prop: str, value, flush=True):
        """Helper function used to update a config propriety.

        Arguments:

            cat {str} -- Category name string
            prop {str} -- Propriety of the category to update
            value {Any} -- Value to associate to the propriety

        Keyword Arguments:

            flush {bool} -- If true it will immediatly update the file on disk (default: {True})
        """
        cls.checkConfigState()
        cls.config[cat][prop] = value
        if flush:
            with open(cls.path, 'w') as configFile:
                cls.config.write(configFile)

    @classmethod
    def getConfigSetting(cls, cat: str, prop: str) -> str:
        """Helper function to retrive a config propriety value.

        Arguments:

            cat {str} -- Category name string
            prop {str} -- Propriety of the category to retrive

        Returns:

            str -- the propriety value
        """
        cls.checkConfigState()
        return cls.config[cat][prop]
    
    @classmethod
    def checkConfigState(cls):
        if not cls.opened and cls.path.exists():
            cls.config.read(cls.path)
            cls.opened = True


    @classmethod
    def setUpInitialConfig(cls, config: configparser.ConfigParser):
        if not cls.path.exists():
            with open(cls.path, 'w') as configFile:
                config.write(configFile)

    @classmethod
    def flush(cls):
        """Helper function used to write the content to file
        """	
        with open(cls.path, 'w') as configFile:
            cls.config.write(configFile)
        cls.config.read(cls.path)
        cls.opened = True