# sample.py
# copy this file and edit the tool name and function for each buttons, dont change the name of the function 
# it must be tool_function() to work

TOOL_NAME = "Create Combine Node"


def tool_function():
    import hou
    sel = hou.selectedNodes()
    for node in sel:
        m = node.parent().createNode("mtlxcombine3")
        for input in m.inputNames():
            m.setInput(m.inputIndex(input),node)
            m.moveToGoodPosition()
            
            
