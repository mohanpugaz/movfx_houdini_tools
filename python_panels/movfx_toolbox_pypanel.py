from PySide2 import QtWidgets
import qlibutils

"""
w=hou.ui.findPaneTab('FloatingPanel').activeInterfaceRootWidget()
w.findChild(QtWidgets.QPlainTextEdit).appendPlainText("this is\n\njust a")
"""

def onCreateInterface():
    #title = QtWidgets.QLabel("Network Info [qL]")
    logfield = QtWidgets.QPlainTextEdit()
    logfield.setReadOnly(True)
    logfield.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
    logfield.setObjectName("logfield")
    
    # Create a widget with a vertical box layout.
    # Add the label and calendar to the layout.
    root_widget = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout()
    #layout.addWidget(title)
    layout.addWidget(logfield)
    
    buttons = QtWidgets.QHBoxLayout()
    refresh = QtWidgets.QPushButton("Refresh")
    refresh.clicked.connect(lambda: refresh_ui())
    buttons.addWidget(refresh)
    layout.addLayout(buttons)
    
    root_widget.setLayout(layout)
    
    # Return the top-level widget.
    #refresh_ui()
    return root_widget


def refresh_ui():
    #print("refresh()")
    #print(kwargs)
    pane = kwargs["paneTab"]
    path = pane.pwd().path()

    if selection_is_similar():
        node = "You selected : " + str(hou.selectedNodes()[0].type().name())
        nodeclass = hou.selectedNodes()[0].type()
        add_buttons(nodeclass)
    else:
        node = "Please select same node types"
        
    stats = node
    try:
        root = pane.activeInterfaceRootWidget()
        root.findChild(QtWidgets.QPlainTextEdit).setPlainText(stats)
 
    except:
        pass
    #print("hoyyy")

def onNodePathChanged(node):

    pane = kwargs["paneTab"]
    path = pane.pwd()
    refresh_ui()

def selection_is_similar():
    nodes = hou.selectedNodes()
    nodeclasses = []
    for n in nodes:
        nodeclasses.append(n.type())
    result = all_elements_same(nodeclasses)
    #print(result)
    return result

def all_elements_same(lst):
    return all(element == lst[0] for element in lst)

def add_buttons(node):
    root = pane.activeInterfaceRootWidget()
    root.QtWidgets.QPushButton("test")