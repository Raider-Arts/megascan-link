import sd
import os
from sd.api.sdtexture import SDTexture

def getIcon():
    return os.path.join(os.path.abspath(os.path.split(__file__)[0]), 'megascan_logo.png')

class MegascanIcon(object):
    path = getIcon()
    sdtexture = SDTexture.sFromFile(getIcon())