# sample.py
# copy this file and edit the tool name and function for each buttons, dont change the name of the function 
# it must be tool_function() to work

TOOL_NAME = "Create refs"


def tool_function():
    import hou
    nodes = hou.selectedNodes()
    for node in nodes:
         
        libnode = node.parm("obj_subnet").eval()
        merge = node.createNode("merge")
        out = node.node("output0")
        refs = []
        for item in hou.node(libnode).children():
            usdpath = item.parm("output_usd").eval()
            refnode = node.createNode("reference::2.0")
            refnode.parm("filepath1").set(usdpath)
            #refnode.setInput(0,hou.item(node.path()+"/1"))
            refs.append(refnode)
        for ref in refs:
            merge.setNextInput(ref)
        out.setInput(0,merge)
        node.layoutChildren()