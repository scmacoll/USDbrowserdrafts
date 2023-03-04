import os
import hou
from PySide2 import QtWidgets


class ProjectManager(QtWidgets.QWidget):
    def __init__(self):  # constructor
        super(ProjectManager, self).__init__()

        self.proj = hou.getenv('JOB') + '/'

        # Create widgets
        self.widget = QtWidgets.QLabel(self.proj)  # label files
        self.list_widget = QtWidgets.QListWidget()  # create list widget

        self.create_interface()

        # Create layout (how widgets will be organised)
        main_layout = QtWidgets.QVBoxLayout()  # vertical layout

        # Add widgets to layout
        main_layout.addWidget(self.widget)


    def open_scene(self, item):
        print('open hip file')
        hip_file = self.proj + item.data()
        # print hip_file
        # open hip_file
        hou.hipFile.load(hip_file)

    def create_interface(self):
        print("creating interface")

        for file in os.listdir(self.proj):
            self.list_widget.addItem(file)

        # connect list items to function
        self.list_widget.doubleClicked.connect(self.open_scene)

        return self.list_widget
