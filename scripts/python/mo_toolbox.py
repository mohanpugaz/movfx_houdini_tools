import movfxTools
from hutil.Qt import QtWidgets


class M_Toolbox(QtWidgets.QWidget):
    
    def __init__(self):
        super(M_Toolbox,self).__init__()
        self.btn = QtWidgets.QPushButton("Test")
        self.createInterface()
        
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.btn)
        self.setLayout(main_layout)
        
    def createInterface(self):   

        return 