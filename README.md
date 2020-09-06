# Introduction 
EZBuild is a python build system meant to help Unity developers generate multi-platform builds and upload those builds to 
storefronts, like Itch.io and Steam.

# Getting Started
TODO: Guide users through getting your code up and running on their own system. In this section you can talk about:
1.	Installation process
- Install `butler` if you want to make Itch.io builds
- Install `steamcmd` if you want to make Steam builds
2.	Software dependencies
3.	Latest releases
4.	API references

# Build and Test
``source venv/bin/activate
python ezbuild
`` 

## Build for PyPi

``python3 setup.py sdist bdist_wheel``

## Upload to PyPi (only auth'd users):

``python3 -m twine upload dist/*``