from PySide2 import QtWidgets, QtCore
import hou
import os
import importlib.util
import webbrowser as wb
import subprocess as sp
import shutil

class SimpleToolsUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(SimpleToolsUI, self).__init__(parent)
        self.setWindowTitle("Simple Tools UI")
        self.setGeometry(300, 300, 400, 500)

        # Main layout
        layout = QtWidgets.QVBoxLayout(self)

        #Tool Info
        self.tool_label = QtWidgets.QLabel("Tools By Nodes________________MOVFX")
        self.tool_label.setStyleSheet("""
            background-color: #9b59b6;
            color: white;
            padding: 10px;
            border-radius: 15px;
        """)
        self.tool_label.setAlignment(QtCore.Qt.AlignCenter)


        layout.addWidget(self.tool_label)
        
        # Node info label
        self.node_label = QtWidgets.QLabel("Select a node to see tools")
        layout.addWidget(self.node_label)
 
        # Scrollable area for tools
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        # Widget to contain the tools
        tools_widget = QtWidgets.QWidget()
        scroll_area.setWidget(tools_widget)
        
        # General Tools
        self.btn_open_folder = QtWidgets.QPushButton("Open Tools Dir")
        self.btn_create_folder = QtWidgets.QPushButton("Create Tool Folder For Current Node")
        
        
        self.btn_open_folder.setStyleSheet("QPushButton { background-color: rgba(0,0,0,0.1); }")
        self.btn_create_folder.setStyleSheet("QPushButton { background-color: rgba(0,0,0,0.1); }")
        
        layout.addWidget(self.btn_open_folder)
        layout.addWidget(self.btn_create_folder)
        
        self.btn_open_folder.clicked.connect(self.open_folder)
        self.btn_create_folder.clicked.connect(self.create_folder_for_current_node)
       



        # Tools layout (aligned to top)
        self.tools_layout = QtWidgets.QVBoxLayout(tools_widget)
        self.tools_layout.setAlignment(QtCore.Qt.AlignTop)

        # Your tools folder path
        self.tools_folder = os.getenv("MOVFX") + "/scripts/python/toolsByNodes_lib"

        # Track current selection to avoid unnecessary updates
        self.current_node_type = None

        # Start monitoring selection
        hou.ui.addEventLoopCallback(self.on_selection_changed)

        # Initial load
        self.on_selection_changed()

    def on_selection_changed(self):
        selected = hou.selectedNodes()

        # --- No node selected ---
        if len(selected) == 0:
            if self.current_node_type is not None:
                self.current_node_type = None
                self.node_label.setText("No node selected")
                self.clear_tools()

        # --- Single node selected ---
        elif len(selected) == 1:
            node = selected[0]
            node_type = node.type().nameWithCategory()
            node_type = node_type.replace(":", "_")

            # Only update if node type changed
            if node_type != self.current_node_type:
                self.current_node_type = node_type
                self.node_label.setText(f"Node: {node.name()} ({node_type})")
                self.load_tools_for_node_type(node_type)

        # --- Multiple nodes selected ---
        else:
            # Collect all node types
            node_types = {node.type().nameWithCategory().replace(":", "_") for node in selected}

            if len(node_types) == 1:
                # All nodes are same type
                node_type = node_types.pop()
                if node_type != self.current_node_type:
                    self.current_node_type = node_type
                    self.node_label.setText(f"{len(selected)} nodes ({node_type}) selected")
                    self.load_tools_for_node_type(node_type)
            else:
                # Different node types
                if self.current_node_type is not None:
                    self.current_node_type = None
                    self.node_label.setText(f"{len(selected)} nodes of different types selected")
                    self.clear_tools()
                    
    def open_folder(self):
        tool_path = self.tools_folder
        print(tool_path)
        wb.open(tool_path)
        #sp.Popen(tool_path)
        
    def create_folder_for_current_node(self):
        selected = hou.selectedNodes()
        if len(selected) == 1:
            node = selected[0]
            node_type = node.type().nameWithCategory()
            node_type = node_type.replace(":", "_")
            print(node_type)
            path = self.tools_folder + "/" + node_type
            
            self.create_folders_safe(path)
            source = self.tools_folder + "/__sample__/sample.py"
            destination = path + "/sample.py"
            print(source)
            print(destination)
            shutil.copy2(source, destination)

    def create_folders_safe(self, path):
        """Safely create folders with error handling."""
        try:
            os.makedirs(path, exist_ok=True)
            print(f"✓ Created/verified folder: {path}")
            return True
        except PermissionError:
            print(f"✗ Permission denied: {path}")
            return False
        except Exception as e:
            print(f"✗ Error creating folder {path}: {e}")
            return False

            
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