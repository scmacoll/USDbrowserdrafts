import os
import hou
from PySide2 import QtWidgets, QtUiTools, QtGui


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
        self.proj_path = self.ui.findChild(QtWidgets.QLabel, 'projpath')
        self.job_path = self.ui.findChild(QtWidgets.QLabel, 'jobpath')
        self.proj_name = self.ui.findChild(QtWidgets.QLabel, 'projname')
        self.scene_list = self.ui.findChild(QtWidgets.QListWidget, 'scenelist')
        self.back_btn = self.ui.findChild(QtWidgets.QPushButton, 'backbtn')

        icon_path = '/Users/stu/Documents/3D/QtDesigner/icons/BUTTONS' \
                    '/back.svg'
        icon = QtGui.QIcon(icon_path)
        self.back_btn.setIcon(icon)

        # # Create widgets
        # self.btn = QtWidgets.QPushButton('Click me')
        # self.lbl_title = QtWidgets.QLabel("PROJECT MANAGER")  # label Title
        # self.label = QtWidgets.QLabel(self.proj)  # label files
        # self.list_widget = QtWidgets.QListWidget()  # create list widget

        # create connections (/button functionality)
        self.set_proj.clicked.connect(self.set_project)
        self.back_btn.clicked.connect(self.back_button)

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
        set_job = 'JOB:  ' + os.path.dirname(set_job)
        proj_path = 'Path:  ' + os.path.split(set_job)[1]
        job_path = set_job

        self.proj_name.setText(proj_name)
        self.proj_path.setText(proj_path + '/')
        self.job_path.setText(job_path + '/')

        self.create_interface()

    def back_button(self):
        # get parent directory
        parent_dir = os.path.dirname(self.proj[:-1])  # [:-1] removes the
        # trailing slash

        # set new project path and update UI
        if os.path.isdir(parent_dir):
            self.proj = parent_dir + '/'

            self.create_interface()
            rel_path = os.path.relpath(self.proj, start=hou.getenv('JOB'))
            self.proj_path.setText(os.path.normpath(self.proj_path.text())
                                   + '/' + rel_path + '/')

    def navigate_subdir(self):
        selected_item = self.scene_list.currentItem()
        if selected_item is not None and os.path.isdir(os.path.join(
                self.proj, selected_item.text())):
            self.proj = os.path.join(self.proj, selected_item.text())

            self.create_interface()
            rel_path = os.path.relpath(self.proj, start=hou.getenv('JOB'))
            self.proj_path.setText(os.path.normpath(self.proj_path.text())
                                   + '/' + rel_path + '/')

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

