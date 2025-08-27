# sample.py
# copy this file and edit the tool name and function for each buttons, dont change the name of the function 
# it must be tool_function() to work

TOOL_NAME = "Anim To Null"


def tool_function():
    import hou
    nodes = hou.selectedNodes()
    for node in nodes:
        null = node.parent().createNode("null")
        null.parm("tx").setFromParm(node.parm("tx"))
        null.parm("ty").setFromParm(node.parm("ty"))
        null.parm("tz").setFromParm(node.parm("tz"))
        null.parm("rx").setFromParm(node.parm("rx"))
        null.parm("ry").setFromParm(node.parm("ry"))
        null.parm("rz").setFromParm(node.parm("rz"))
        null.parm("sx").setFromParm(node.parm("sx"))
        null.parm("sy").setFromParm(node.parm("sy"))
        null.parm("sz").setFromParm(node.parm("sz"))
        null.setPosition(node.position())
        node.setInput(0,null)
        node.parm("tx").revertToDefaults()
        node.parm("ty").revertToDefaults()
        node.parm("tz").revertToDefaults()
        node.parm("rx").revertToDefaults()
        node.parm("ry").revertToDefaults()
        node.parm("rz").revertToDefaults()
        node.parm("sx").revertToDefaults()
        node.parm("sy").revertToDefaults()
        node.parm("sz").revertToDefaults()
        node.parm("tx").deleteAllKeyframes()
        node.parm("ty").deleteAllKeyframes()
        node.parm("tz").deleteAllKeyframes()
        node.parm("rx").deleteAllKeyframes()
        node.parm("ry").deleteAllKeyframes()
        node.parm("rz").deleteAllKeyframes()
        node.parm("sx").deleteAllKeyframes()
        node.parm("sy").deleteAllKeyframes()
        node.parm("sz").deleteAllKeyframes()
