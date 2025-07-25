from PySide2 import QtWidgets, QtCore
import hou
import os
import importlib.util
import webbrowser as wb
import subprocess as sp


class SimpleToolsUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(SimpleToolsUI, self).__init__(parent)
        self.setWindowTitle("Simple Tools UI")
        self.setGeometry(300, 300, 400, 500)

        # Main layout
        layout = QtWidgets.QVBoxLayout(self)

        # Node info label
        self.node_label = QtWidgets.QLabel("Select a node to see tools")
        layout.addWidget(self.node_label)

        # General Tools
        self.btn_open_folder = QtWidgets.QPushButton("Open")
        layout.addWidget(self.btn_open_folder)
        self.btn_open_folder.clicked.connect(self.open_folder)

        # Scrollable area for tools
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        # Widget to contain the tools
        tools_widget = QtWidgets.QWidget()
        scroll_area.setWidget(tools_widget)

        # Tools layout (aligned to top)
        self.tools_layout = QtWidgets.QVBoxLayout(tools_widget)
        self.tools_layout.setAlignment(QtCore.Qt.AlignTop)

        # Your tools folder path
        self.tools_folder = "/users/mohan/movfx/movfx_houdini_tools/scripts/python/toolsByNodes_lib"

        # Track current selection to avoid unnecessary updates
        self.current_node_type = None

        # Start monitoring selection
        hou.ui.addEventLoopCallback(self.on_selection_changed)

        # Initial load
        self.on_selection_changed()

    def on_selection_changed(self):
        # Get selected nodes
        selected = hou.selectedNodes()

        if len(selected) == 1:
            node = selected[0]
            node_type = node.type().name()

            # Only update if node type changed
            if node_type != self.current_node_type:
                self.current_node_type = node_type
                self.node_label.setText(f"Node: {node.name()} ({node_type})")
                self.load_tools_for_node_type(node_type)
        else:
            # Only update if we had a selection before
            if self.current_node_type is not None:
                self.current_node_type = None
                self.node_label.setText("Select a single node")
                self.clear_tools()


    def open_folder(self,  node_type):
        tool_path = self.tools_folder + "/" + hou.selectedNodes()[0].type().name()
        print(tool_path)
        #wb.open(tool_path)
        sp.Popen(tool_path)

    def load_tools_for_node_type(self, node_type):
        self.clear_tools()

        # Path to node type folder
        node_folder = os.path.join(self.tools_folder, node_type)

        if not os.path.exists(node_folder):
            label = QtWidgets.QLabel(f"No folder found: {node_type}")
            self.tools_layout.addWidget(label)
            return

        # Get Python files in the folder
        py_files = [f for f in os.listdir(node_folder) if f.endswith('.py')]

        if not py_files:
            label = QtWidgets.QLabel(f"No tools found in {node_type} folder")
            self.tools_layout.addWidget(label)
            return

        # Create buttons for each tool
        for py_file in py_files:
            try:
                tool = self.load_tool(node_folder, py_file)
                if tool:
                    button = QtWidgets.QPushButton(tool['name'])
                    button.clicked.connect(self.make_tool_function(tool['function']))
                    self.tools_layout.addWidget(button)
            except Exception as e:
                print(f"Error loading {py_file}: {e}")

    def make_tool_function(self, func):
        """Create a proper function for button connection"""

        def call_tool():
            func()

        return call_tool

    def load_tool(self, folder_path, filename):
        # Load the Python file
        file_path = os.path.join(folder_path, filename)
        spec = importlib.util.spec_from_file_location("tool", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Check if it has required parts
        if hasattr(module, 'TOOL_NAME') and hasattr(module, 'tool_function'):
            return {
                'name': module.TOOL_NAME,
                'function': module.tool_function
            }
        return None

    def clear_tools(self):
        # Remove all tool buttons
        while self.tools_layout.count():
            child = self.tools_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def closeEvent(self, event):
        hou.ui.removeEventLoopCallback(self.on_selection_changed)
        event.accept()


def createInterface():
    return SimpleToolsUI()