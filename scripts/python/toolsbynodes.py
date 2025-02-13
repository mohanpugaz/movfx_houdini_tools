from PySide2 import QtWidgets
import hou

class SimplePythonPanel(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(SimplePythonPanel, self).__init__(parent)

        self.setWindowTitle("Simple Houdini Panel")
        self.setLayout(QtWidgets.QVBoxLayout())

        # Button Row
        button_layout = QtWidgets.QHBoxLayout()
        self.btn_createNew = QtWidgets.QPushButton("Create New Tool")
        self.btn_edit = QtWidgets.QPushButton("Edit Tools")
        self.btn_remove = QtWidgets.QPushButton("Remove Tools")

        button_layout.addWidget(self.btn_createNew)
        button_layout.addWidget(self.btn_edit)
        button_layout.addWidget(self.btn_remove)
        self.layout().addLayout(button_layout)

        # Node Label
        self.node_label = QtWidgets.QLabel("Selected Node: None")
        self.layout().addWidget(self.node_label)

        # Install event callback for selection changes
        hou.ui.addEventLoopCallback(self.update_node_name)

        # Assign default functions to buttons
        self.btn_createNew.clicked.connect(self.on_btn_createNew_click)
        self.btn_edit.clicked.connect(self.on_btn_edit_click)
        self.btn_remove.clicked.connect(self.on_btn_remove_click)

    def update_node_name(self):
        selected_nodes = hou.selectedNodes()

        if not selected_nodes:
            self.node_label.setText("Node Type: None\nNode Name: None")
            return

        if len(selected_nodes) > 1:
            self.node_label.setText("Node Type: Multiple Selected\nNode Name: Multiple Selected")
        else:
            node = selected_nodes[0]
            self.node_label.setText(f"Node Type: {node.type().name()}\nNode Name: {node.name()}")

    def on_btn_createNew_click(self):
        hou.ui.displayMessage("Create New Clicked")  # Replace with custom function

    def on_btn_edit_click(self):
        print("Button 2 clicked")  # Replace with custom function

    def on_btn_remove_click(self):
        print("Button 3 clicked")  # Replace with custom function

    def closeEvent(self, event):
        hou.ui.removeEventLoopCallback(self.update_node_name)
        event.accept()

def createInterface():
    return SimplePythonPanel()
