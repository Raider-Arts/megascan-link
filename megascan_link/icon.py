"""Module containing classes for using and retriving icons files
"""
import os

import sd
from sd.api.sdtexture import SDTexture


def getIcon(name: str) -> str:
    """Return the path to the specified icon

    :param name: icon filename
    :type name: str
    :return: absolute path to the icon
    :rtype: str
    """     
    return os.path.join(os.path.abspath(os.path.split(__file__)[0]), name)

class MegascanIcon(object):
    """Simple class for storing and retriving the Megascan Logo as a path to file or as a SDTexture instance
    """
    #: Path to the Megascan Logo
    #:
    #: :type: str
    path = getIcon('megascan_logo.png')
    #: SDTexture instance created form the Megascan Logo path
    #:
    #: :type: SDTexture
    sdtexture = SDTexture.sFromFile(getIcon('megascan_logo.png'))
