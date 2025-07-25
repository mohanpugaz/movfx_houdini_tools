# test_tool.py

TOOL_NAME = "Enable Velocity Blur"


def tool_function():
    import hou
    node = hou.selectedNodes()[0]
    node.parm("geo_velocityblur").set(1)
