import os
import hou
from PySide2 import QtWidgets, QtUiTools


class ProjectManager(QtWidgets.QWidget):
    def __init__(self):  # constructor
        super(ProjectManager, self).__init__()

        self.proj = hou.getenv('JOB') + '/'

        # Load UI file
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load('/Users/stu/Library/Preferences/houdini/19.5'
                              '/scripts/python/projectview/projectview.ui')

        # Create widgets
        self.btn = QtWidgets.QPushButton('Click me')
        self.lbl_title = QtWidgets.QLabel("PROJECT MANAGER")  # label Title
        self.label = QtWidgets.QLabel(self.proj)  # label files
        self.list_widget = QtWidgets.QListWidget()  # create list widget

        self.create_interface()  # run function to create interface

        # Create layout (how widgets will be organised)
        main_layout = QtWidgets.QVBoxLayout()  # vertical layout

        main_layout.addWidget(self.ui)

        # # Add widgets (manual) to layout
        # main_layout.addWidget(self.lbl_title)  # label (title) outside list
        # main_layout.addWidget(self.label)  # label outside list
        # main_layout.addWidget(self.list_widget)  # visible list
        # main_layout.addWidget(self.btn)

        self.setLayout(main_layout)


    def open_scene(self, item):  # double click to open hip file
        print('open hip file')
        hip_file = self.proj + item.data()
        # print hip_file
        # open hip_file
        hou.hipFile.load(hip_file)

    def create_interface(self):  # create list interface
        print("creating interface")

        for file in os.listdir(self.proj):
            self.list_widget.addItem(file)

        # connect list items to function
        self.list_widget.doubleClicked.connect(self.open_scene)

        return self.list_widget
