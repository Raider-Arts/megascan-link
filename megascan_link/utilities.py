"""Module containing utilities function for general usage
"""
import os

import sd
from sd.api.sdapplication import SDApplication


def getAbsCurrentPath(append: str) -> str:
	"""Simple function to get the current script path

	:param append: path or filename to add
	:type append: str
	:return: the full path plus the append param
	:rtype: str
	"""	
	return os.path.join(os.path.abspath(os.path.split(__file__)[0]), append)


def getApp() -> SDApplication:
	"""Helper function to retrive the SDApplication

	:return: the substance designer application instance
	:rtype: SDApplication
	"""
	context = sd.getContext()
	return context.getSDApplication()

def getUiManager():
	"""Helper function to retrive the QtPythonUIManager

	:return: return the current QtForPythonUIMgr instance 
	:rtype: UIMngr
	"""
	return getApp().getQtForPythonUIMgr()
