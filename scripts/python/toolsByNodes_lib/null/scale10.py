# test_tool.py

TOOL_NAME = "Scale to 10"


def tool_function():
    import hou
    node = hou.selectedNodes()[0]
    node.parm("scale").set(10)
