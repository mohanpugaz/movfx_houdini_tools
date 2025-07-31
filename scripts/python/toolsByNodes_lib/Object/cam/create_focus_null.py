# sample.py
# copy this file and edit the tool name and function for each buttons, dont change the name of the function 
# it must be tool_function() to work

TOOL_NAME = "Create Focus Null"


def tool_function():
    import hou
    node = hou.selectedNodes()[0]
    pos = node.position()
    null = node.parent().createNode("null")
    null.setName("Focus")
    null.setPosition(pos)
    null.moveToGoodPosition()

    expr = r"""
import hou
cam = hou.node(".")
focus = hou.node("../Focus")

if cam and focus:
    cam_pos = cam.worldTransform().extractTranslates()
    focus_pos = focus.worldTransform().extractTranslates()
    return (focus_pos - cam_pos).length()
else:
    return 0
    """
    
    node.parm("focus").setExpression(expr,hou.exprLanguage.Python)

    
    
