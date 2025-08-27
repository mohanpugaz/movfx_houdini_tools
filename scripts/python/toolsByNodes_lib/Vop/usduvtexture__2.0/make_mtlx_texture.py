# sample.py
# copy this file and edit the tool name and function for each buttons, dont change the name of the function 
# it must be tool_function() to work

TOOL_NAME = "Make Mtlx Texture"


def tool_function():
    import hou
    nodes = hou.selectedNodes()
    for node in nodes:
        t = node.parent().createNode("mtlxUsdUVTexture23")
        fileparm = node.parm("file")
        t.parm("file").setFromParm(fileparm)
        pos = node.position()
        t.setPosition(pos + hou.Vector2(1.5,0))