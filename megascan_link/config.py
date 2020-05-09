import configparser
import os
import megascan_link
from megascan_link import utilities as util
from pathlib import Path

class ConfigSettings(object):
    """Class that manages a config file
    """    
    #: Contains the path to the megascanlink config file (root dir of module)
    path = Path(util.getAbsCurrentPath('megascanlink.ini'))
    #: Config parser class instance
    config = configparser.ConfigParser()
    #: Current state of the config file
    opened = False

    @classmethod
    def updateConfigSetting(cls, cat: str, prop: str, value: str, flush=True):
        """Helper function used to update a config propriety.

        :param cat: Category name string
        :type cat: str
        :param prop: Propriety of the category to update
        :type prop: str
        :param value: Value to associate to the propriety
        :type value: str
        :param flush: If true it will immediatly update the file on disk, defaults to True
        :type flush: bool, optional
        """
        cls.checkConfigState()
        if not cls.config.has_section(cat):
            cls.config.add_section(cat)
        cls.config[cat][prop] = str(value)
        if flush:
            with open(cls.path, 'w') as configFile:
                cls.config.write(configFile)

    @classmethod
    def getConfigSetting(cls, cat: str, prop: str) -> str:
        """Helper function to retrive a config propriety value.

        :param cat: Category name string
        :type cat: str
        :param prop: Propriety of the category to retrive
        :type prop: str
        :return: the propriety value
        :rtype: str
        """
        cls.checkConfigState()
        # return cls.config[cat][prop]
        return cls.config.get(cat,prop,fallback="")
    
    @classmethod
    def checkConfigState(cls):
        """Check if the current config file is opened if not and the file exist
        reads and load the content of it to the config parser
        """        
        if not cls.opened and cls.path.exists():
            cls.config.read(cls.path)
            cls.opened = True


    @classmethod
    def setUpInitialConfig(cls, config: configparser.ConfigParser):
        """Function to use a config parser instance to initialize the config file
        This will initialize the config file only if it does not exist

        :param config: The config instance to use for populating the initial value of the config
        :type config: configparser.ConfigParser
        """        
        if not cls.path.exists():
            with open(cls.path, 'w') as configFile:
                config.write(configFile)

    @classmethod
    def checkIfOptionIsSet(cls, cat: str, prop: str) -> bool:
        """Helper function that will check if a propriety of a section is set or not by confronting
        it with the following values ["true", "yes", "y", "ok"]

        :param cat: Category name string
        :type cat: str
        :param prop: Propriety of the category to check agains
        :type prop: str
        :return: if the propriety is set returns True, False otherwise
        :rtype: bool
        """        
        if cls.getConfigSetting(cat, prop).lower() in ["true", "yes", "y", "ok"]:
            return True
        return False

    @classmethod
    def flush(cls):
        """Helper function used to write the content to file
        """	
        with open(cls.path, 'w') as configFile:
            cls.config.write(configFile)
        cls.config.read(cls.path)
        cls.opened = True