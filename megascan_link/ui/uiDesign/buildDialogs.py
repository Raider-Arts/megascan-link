'''
 # @ Author: Luca Faggion
 # @ Create Time: 2020-05-08 09:38:52
 # @ Modified by: Luca Faggion
 # @ Modified time: 2020-05-08 10:02:09
 # @ Description: Simple script used to build all the ui design coming from Qt Designer
 '''

import os
import subprocess
from pathlib import Path

dialogsDesigns = Path().glob('**/*.ui')
for dialog in dialogsDesigns:
    command = ["pyside2-uic", str(dialog), ">", str(dialog.absolute().parents[1] / (dialog.stem + ".py"))]
    print("processing: ", dialog.stem)
    os.system(" ".join(command))
print("Done")
