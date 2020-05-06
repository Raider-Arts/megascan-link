import sd

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