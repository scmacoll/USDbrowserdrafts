import os
import hou
from PySide2 import QtWidgets, QtUiTools, QtGui


class Node:
    def __init__(self, path):
        self.path = path
        self.children = []

    def add_child(self, node):
        print("Adding child:", node.path)
        self.children.append(node)

    #  !TO DO
    # def parent(self, parent):
    #     self.parent = os.normpath.isdir(self.parent)


class Tree:
    def __init__(self, root=""):
        self.root = Node(root)

    def add_path(self, path):
        print("Adding path:", path)
        current = self.root
        for part in path.split(os.sep):
            print("part:    " + part)
            if not part:
                continue
            found = None
            for child in current.children:
                if child.path == part:
                    found = child
                    break
            if found is None:
                found = Node(part)
                current.add_child(found)
            current = found


    def get_current_path(self, current):
        path = []
        while current is not self.root:
            path.append(current.path)
            current = current.parent
        path.reverse()
        return os.sep.join(path)


class ProjectManager(QtWidgets.QWidget):
    def __init__(self):
        super(ProjectManager, self).__init__()

        self.tree = Tree()
        self.current_node = self.tree.root
        print("    REFRESH    ")

        # Load UI file
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load('/Users/stu/Library/Preferences/houdini/19.5'
                              '/scripts/python/projectview/projectview.ui')

        # get UI elements (designer)
        self.set_proj = self.ui.findChild(QtWidgets.QPushButton, 'setproj')
        self.back_btn = self.ui.findChild(QtWidgets.QPushButton, 'backbtn')
        self.fwd_btn = self.ui.findChild(QtWidgets.QPushButton, 'fwdbtn')
        self.proj_path = self.ui.findChild(QtWidgets.QLabel, 'projpath')
        self.job_path = self.ui.findChild(QtWidgets.QLabel, 'jobpath')
        self.proj_name = self.ui.findChild(QtWidgets.QLabel, 'projname')
        self.scene_list = self.ui.findChild(QtWidgets.QListWidget, 'scenelist')

        back_icon_path = '/Users/stu/Documents/3D/QtDesigner/icons/BUTTONS' \
                         '/back.svg'
        back_icon = QtGui.QIcon(back_icon_path)
        self.back_btn.setIcon(back_icon)
        fwd_icon_path = '/Users/stu/Documents/3D/QtDesigner/icons/BUTTONS' \
                        '/forward.svg'
        fwd_icon = QtGui.QIcon(fwd_icon_path)
        self.fwd_btn.setIcon(fwd_icon)

        # create connections (/button functionality)
        self.set_proj.clicked.connect(self.set_project)
        self.back_btn.clicked.connect(self.back_button)
        self.fwd_btn.clicked.connect(self.forward_button)

        # Create layout (how widgets will be organised)
        main_layout = QtWidgets.QVBoxLayout()  # vertical layout

        main_layout.addWidget(self.ui)

        self.setLayout(main_layout)

    def set_project(self):
        set_job = hou.ui.selectFile(title='Select Project Folder',
                                    file_type=hou.fileType.Directory)
        hou.hscript('setenv JOB=' + set_job)
        # set_job = os.path.expanduser(set_job)
        self.proj = hou.getenv('JOB')

        self.tree = Tree(self.proj)  # create a new tree
        self.current_node = self.tree.root  # create a new node
        self.tree.add_path(self.proj)  # add path to tree node

        proj_name = 'Project:  ' + set_job.split('/')[-2]
        set_job = 'JOB:  ' + os.path.dirname(set_job)
        proj_path = 'Path:  ' + set_job
        self.proj_name.setText(proj_name)
        self.job_path.setText(set_job)
        self.proj_path.setText(proj_path)

        #  Create a Node Instance
        self.current_node = self.tree.root
        self.update_scene_list()

    def update_scene_list(self):
        self.scene_list.clear()

        self.tree.root.path = self.tree.root.path + '/'
        if self.tree.root.path[-2:] == '//':
            self.tree.root.path = self.tree.root.path[:-1]

        print("current node:    " + str(self.tree.root))
        print("node path:    " + self.tree.root.path)
        print("node children []:    " + str(self.tree.root.children))

        items = os.listdir(self.tree.root.path)
        items.sort()

        for file in items:
            path = os.path.join(self.tree.root.path, file)
            if os.path.isdir(path):
                self.scene_list.addItem(file)
                self.tree.add_path(path + '/')  # sequential paths added
                self.tree.node = self.tree.root
            elif file.endswith('.usda'):
                self.scene_list.addItem(file)

        return self.scene_list

    def back_button(self):


        self.update_scene_list()

    def forward_button(self):
        selected_item = self.scene_list.currentItem()

        if selected_item is not None and os.path.isdir(os.path.join(
                self.tree.root.path, selected_item.text())):
            selected_path = os.path.join(self.current_node.path,
                                         selected_item.text())
            for child in self.current_node.children:
                if child.path == selected_path:
                    self.current_node = child
                    self.update_scene_list()
                    break
        else:
            print("you have selected a .USD file")
            return

        self.tree.root.path = os.path.join(
            self.tree.root.path + selected_item.text())

        print("<<<    forward button pressed! :D    >>>")
        self.update_scene_list()

    def get_current_node(self):
        return self.current_node
