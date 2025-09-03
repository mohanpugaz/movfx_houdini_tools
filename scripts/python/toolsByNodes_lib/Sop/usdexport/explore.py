# sample.py
# copy this file and edit the tool name and function for each buttons, dont change the name of the function 
# it must be tool_function() to work

TOOL_NAME = "Explore Output Path"


def tool_function():
    import hou
    import os
    import subprocess
    import platform
    node = hou.selectedNodes()[0]
    usdfile = node.parm("lopoutput").eval()
    filepath = os.path.dirname(usdfile)

    system = platform.system()
    if system == "Windows":
        os.startfile(filepath)  # uses default program
    elif system == "Darwin":  # macOS
        subprocess.run(["open", filepath])
    else:  # Linux, BSD etc
        subprocess.run(["xdg-open", filepath])