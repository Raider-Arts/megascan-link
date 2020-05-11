# Development Prerequisites

There are no prerequisites for the plugin all the requisites are already build-in in the default Python installation of Substance Designer

The only requisite necessary is [PySide2](https://pypi.org/project/PySide2/) for using the `buildDialogs.py` script.

But if you want to debug the plugin with a step-through debugger refere to the official Substance Designer documentation. [Debugging Plugins using Visual Studio Code](https://docs.substance3d.com/sddoc/debugging-plugins-using-visual-studio-code-172825679.html)


### Building the Documentation

The prerequisite to build the documentation using **sphinx** are the following:

- [sphinx](https://www.sphinx-doc.org/en/master/)
- [recommonmark](https://recommonmark.readthedocs.io/en/latest/)
- [sphinx-rtd-theme](https://pypi.org/project/sphinx-rtd-theme/)
- [sphinx-markdown-tables](https://pypi.org/project/sphinx-markdown-tables/)

when all the prerequisites are installed these are the steps needed to build the documentation:

- Navigate to the doc folder

        cd doc

- Build using make

        make html


### Building the sdplugin package

To build the sdplugin package navigate to the root folder of the repository and simply execute the `makepackage.py` script:

        python makepackage.py

the resulting builded file is placed in the `build` directory