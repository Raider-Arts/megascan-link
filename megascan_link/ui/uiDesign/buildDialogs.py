"""Build the QtDesigner ui files
Simple script to automate the build of QtDesigner ui files to python code
"""
import os
import subprocess
from pathlib import Path

def buildUiDesigns():
    dialogsDesigns = Path().glob('**/*.ui')
    for dialog in dialogsDesigns:
        command = ["pyside2-uic", str(dialog), ">", str(dialog.absolute().parents[1] / (dialog.stem + ".py"))]
        print("processing: ", dialog.stem)
        os.system(" ".join(command))
    print("Done")

if __name__ == "__main__":
    buildUiDesigns()