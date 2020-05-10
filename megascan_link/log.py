"""This Module contains the logger facilities class 
"""

import megascan_link
from megascan_link import utilities as util
from megascan_link import config

import logging
import sys

import sd
from sd.api.sdapplication import SDApplication
from sd.logger import *

class LoggerLink(object):
	"""Class used to log messages to the log file

	see: :meth:`~megascan_link.log.LoggerLink.Log` for know how to use it to print also to the Python editor output
	"""	

	#: Internal reference to the logger
	_logger = logging.getLogger('megascanlink')

	#: Internal state of the logger
	_isSetup = False

	@classmethod
	def setUpLogger(cls):
		"""Method used to setup the current logger instance 

		Links the handler to print to the log file (log config path: './megascanlink.log')
		and set up the format to print with
		"""
		cls._isSetup = True
		logFormatter = logging.Formatter("%(asctime)s [%(name)s] [%(levelname)s]  %(message)s")
		for handler in cls._logger.handlers:
			cls._logger.handlers.pop()
		filehandler = logging.FileHandler(util.getAbsCurrentPath('megascanlink.log'), mode='a')
		filehandler.setFormatter(logFormatter)
		cls._logger.addHandler(filehandler)
		cls._logger.setLevel(logging.DEBUG)

	@classmethod
	def Log(cls, msg: str, logLevel=logging.INFO):
		"""Helper function used to log a massage to a file or if specified in the config file
		with the `outputConsole` propriety also to the Python Editor output of Substance Designer

		:param msg: the message to print
		:type msg: str
		:param logLevel: the log level to print with if it  is lower than the current :attr:`~megascan_link.log.LoggerLink._logger` level it would not be printed, defaults to logging.INFO
		:type logLevel: int, optional
		"""		
		conf = config.ConfigSettings()
		lvl = ""
		if not cls._isSetup:
			cls.setUpLogger()
		if logLevel == logging.INFO:
			lvl = "INFO"
			cls._logger.info(msg)
		if logLevel ==  logging.WARNING:
			lvl = "WARNING"
			cls._logger.warning(msg)
		if logLevel == logging.ERROR:
			lvl = "ERROR"
			cls._logger.error(msg)
		if logLevel == logging.DEBUG:
			lvl = "DEBUG"
			cls._logger.debug(msg)
		if conf.checkIfOptionIsSet("General", "outputConsole"):
			if logLevel >= cls._logger.level:
				print("[megascanlink][{}] {}".format(lvl,msg))
