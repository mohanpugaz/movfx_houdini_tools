# sample.py
# copy this file and edit the tool name and function for each buttons, dont change the name of the function 
# it must be tool_function() to work

TOOL_NAME = "Create Reference"


def tool_function():
    import hou
    nodes = hou.selectedNodes()
    for node in nodes:
        filevalue = node.parm("lopoutput").eval()
        ref = node.parent().createNode("reference::2.0")
        ref.moveToGoodPosition()
        ref.parm("filepath1").set(filevalue)



