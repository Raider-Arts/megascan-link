"""Module containing classes for using and retriving icons files
"""
import os

import sd
from sd.api.sdtexture import SDTexture


def getIcon():
    """Return the path to the Megascan logo icon
    """    
    return os.path.join(os.path.abspath(os.path.split(__file__)[0]), 'megascan_logo.png')

class MegascanIcon(object):
    """Simple class for storing and retriving the Megascan Logo as a path to file or as a SDTexture instance
    """
    #: Path to the Megascan Logo
    #:
    #: :type: str
    path = getIcon()
    #: SDTexture instance created form the Megascan Logo path
    #:
    #: :type: SDTexture
    sdtexture = SDTexture.sFromFile(getIcon())
