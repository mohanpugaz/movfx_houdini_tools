# sample.py
# copy this file and edit the tool name and function for each buttons, dont change the name of the function 
# it must be tool_function() to work

TOOL_NAME = "Explore Source"


def tool_function():
    import hou
    import os
    import webbrowser as wb
    sel = hou.selectedNodes()
    for node in sel:
        source = node.parm("filepath1").eval()
        sourcepath = os.path.dirname(source)
        wb.open(sourcepath)
    