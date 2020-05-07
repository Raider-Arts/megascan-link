import sd
import os

def getAbsCurrentPath(append):
	return os.path.join(os.path.abspath(os.path.split(__file__)[0]), append)


def getApp():
	"""Helper function to retrive the SDApplication
	
	Returns:
		SDApplication -- Substance Designer sdapplication instance
	"""	
	context = sd.getContext()
	return context.getSDApplication()

def getUiManager(): 
	"""Helper function to retrive the QtPythonUIManager
	
	Returns:
		QtForPythonUIMgr -- class instance
	"""	
	return getApp().getQtForPythonUIMgr()