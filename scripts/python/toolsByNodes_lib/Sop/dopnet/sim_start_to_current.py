# sample.py
# copy this file and edit the tool name and function for each buttons, dont change the name of the function 
# it must be tool_function() to work

TOOL_NAME = "Sim Start To Current Frame"


def tool_function():
    import hou
    node = hou.selectedNodes()[0]
    node.parm("startframe").set(hou.frame())

