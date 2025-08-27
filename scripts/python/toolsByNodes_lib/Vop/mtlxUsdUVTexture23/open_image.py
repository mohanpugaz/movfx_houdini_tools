# sample.py
# copy this file and edit the tool name and function for each buttons, dont change the name of the function 
# it must be tool_function() to work

TOOL_NAME = "Open Image"


def tool_function():
    import hou
    nodes = hou.selectedNodes()
    for node in nodes:
        filevalue = node.parm("file").eval()
        open_with_default(filevalue)


def open_with_default(filepath):
    import os
    import subprocess
    import platform
    system = platform.system()
    if system == "Windows":
        os.startfile(filepath)  # uses default program
    elif system == "Darwin":  # macOS
        subprocess.run(["open", filepath])
    else:  # Linux, BSD etc
        subprocess.run(["xdg-open", filepath])


