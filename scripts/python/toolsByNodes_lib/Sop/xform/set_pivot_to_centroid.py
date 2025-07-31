# sample.py
# copy this file and edit the tool name and function for each buttons, dont change the name of the function 
# it must be tool_function() to work

TOOL_NAME = "Set Pivot To Centroid"


def tool_function():
    import hou
    node = hou.selectedNodes()[0]
    node.parm("px").setExpression("$CEX")
    node.parm("py").setExpression("$CEY")
    node.parm("pz").setExpression("$CEZ")
    