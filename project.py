import os
import hou
from PySide2 import QtWidgets, QtUiTools


class ProjectManager(QtWidgets.QWidget):
    def __init__(self):  # constructor`
        super(ProjectManager, self).__init__()

        self.proj = hou.getenv('JOB') + '/'

        # Load UI file
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load('/Users/stu/Library/Preferences/houdini/19.5'
                              '/scripts/python/projectview/projectview.ui')

        # get UI elements (designer)
        self.set_proj = self.ui.findChild(QtWidgets.QPushButton, 'setproj')
        self.proj_path = self.ui.findChild(QtWidgets.QLineEdit, 'projpath')
        self.proj_name = self.ui.findChild(QtWidgets.QLabel, 'projname')
        self.scene_list = self.ui.findChild(QtWidgets.QListWidget, 'scenelist')

        # # Create widgets
        # self.btn = QtWidgets.QPushButton('Click me')
        # self.lbl_title = QtWidgets.QLabel("PROJECT MANAGER")  # label Title
        # self.label = QtWidgets.QLabel(self.proj)  # label files
        # self.list_widget = QtWidgets.QListWidget()  # create list widget

        # create connections (/button functionality)
        self.set_proj.clicked.connect(self.set_project)

        # Create layout (how widgets will be organised)
        main_layout = QtWidgets.QVBoxLayout()  # vertical layout

        main_layout.addWidget(self.ui)

        # # Add widgets to layout
        # main_layout.addWidget(self.lbl_title)  # label (title) outside list
        # main_layout.addWidget(self.label)  # label outside list
        # main_layout.addWidget(self.list_widget)  # visible list
        # main_layout.addWidget(self.btn)

        self.setLayout(main_layout)

    def set_project(self):
        set_job = hou.ui.selectFile(title='Select Project Folder',
                                    file_type=hou.fileType.Directory)
        hou.hscript('setenv JOB=' + set_job)
        self.proj = hou.getenv('JOB') + '/'

        proj_name = 'Project:  ' + set_job.split('/')[-2]
        set_job = os.path.dirname(set_job)  # remove "/" @ end of name
        proj_path = set_job

        self.proj_name.setText(proj_name)
        self.proj_path.setText(proj_path + '/')

        self.create_interface()

    def navigate_subdir(self):
        selected_item = self.scene_list.currentItem()
        if selected_item is not None and os.path.isdir(os.path.join(
                self.proj, selected_item.text())):
            self.proj = os.path.join(self.proj, selected_item.text())
            self.create_interface()
            self.proj_path.setText(os.path.normpath(self.proj))

    # def create_interface(self):
    #     print("loaded interface")
    #     self.scene_list.clear()
    #
    #     for file in os.listdir(self.proj):
    #         path = os.path.join(self.proj, file)
    #         if os.path.isdir(path):
    #             self.scene_list.addItem(file)
    #             self.scene_list.doubleClicked.connect(self.navigate_subdir)
    #         elif file.endswith('.usda'):
    #             self.scene_list.addItem(file)
    #             self.scene_list.doubleClicked.connect(
    #                 lambda item: print("importing usda"))
    #
    #     return self.scene_list
    def create_interface(self):
        print("loaded interface")
        self.scene_list.clear()

        items = os.listdir(self.proj)
        items.sort()

        for file in items:
            path = os.path.join(self.proj, file)
            if os.path.isdir(path):
                self.scene_list.addItem(file)
                self.scene_list.doubleClicked.connect(self.navigate_subdir)
            elif file.endswith('.usda'):
                self.scene_list.addItem(file)
                self.scene_list.doubleClicked.connect(
                    lambda item: print("importing usda"))

        return self.scene_list

