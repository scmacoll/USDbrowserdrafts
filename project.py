import os
import hou
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QLineEdit, QListWidgetItem, QHBoxLayout
from PySide2.QtGui import QKeySequence, QBrush, QColor
from PySide2 import QtWidgets, QtUiTools, QtGui, QtCore


class Node:
    def __init__(self, path):
        self.path = path
        self.children = []

    def add_child(self, node):
        # print("Adding child:", node.path)
        self.children.append(node)


class Tree:
    def __init__(self, root=""):
        self.root = Node(root)

    def add_path(self, path):
        # print("Adding path:", path)
        current = self.root
        for part in path.split(os.sep):
            # print("part:    " + part)
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

        self.back_stack = []

        # Load UI file
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load('/Users/stu/Library/Preferences/houdini/19.5'
                              '/scripts/python/projectview/projectview.ui')

        # get UI elements (designer)
        self.set_proj = self.ui.findChild(QtWidgets.QPushButton, 'setproj')
        self.back_btn = self.ui.findChild(QtWidgets.QPushButton, 'backbtn')
        self.fwd_btn = self.ui.findChild(QtWidgets.QPushButton, 'fwdbtn')
        self.ref_btn = self.ui.findChild(QtWidgets.QPushButton, 'refbtn')
        self.alpha_sort = self.ui.findChild(QtWidgets.QPushButton, 'alphasort')
        self.home_btn = self.ui.findChild(QtWidgets.QPushButton, 'homebtn')
        self.reset_btn = self.ui.findChild(QtWidgets.QPushButton, 'resetbtn')
        self.proj_path = self.ui.findChild(QtWidgets.QLabel, 'projpath')
        self.job_path = self.ui.findChild(QtWidgets.QLabel, 'jobpath')
        self.proj_name = self.ui.findChild(QtWidgets.QLabel, 'projname')
        self.usd_label = self.ui.findChild(QtWidgets.QLabel, 'usdlabel')
        self.scene_list = self.ui.findChild(QtWidgets.QListWidget, 'scenelist')
        self.search_bar = self.ui.findChild(QtWidgets.QLineEdit, 'searchbar')
        self.usda_label = self.ui.findChild(QtWidgets.QLabel, 'usdalbl')
        self.usdc_label = self.ui.findChild(QtWidgets.QLabel, 'usdclbl')

        self.default_proj_name = self.proj_name.text()
        self.default_proj_path = self.proj_path.text()
        self.default_job_path = self.job_path.text()

        self.current_order = Qt.AscendingOrder

        back_icon_path = '/Users/stu/Documents/3D/QtDesigner/icons/BUTTONS' \
                         '/back.svg'
        back_icon = QtGui.QIcon(back_icon_path)
        self.back_btn.setIcon(back_icon)

        fwd_icon_path = '/Users/stu/Documents/3D/QtDesigner/icons/BUTTONS' \
                        '/forward.svg'
        fwd_icon = QtGui.QIcon(fwd_icon_path)
        self.fwd_btn.setIcon(fwd_icon)

        ref_icon_path = '/Users/stu/Documents/3D/QtDesigner/icons/BUTTONS' \
                        '/reload.svg'
        ref_icon = QtGui.QIcon(ref_icon_path)
        self.ref_btn.setIcon(ref_icon)

        home_icon_path = '/Users/stu/Documents/3D/QtDesigner/icons/IMAGE' \
                         '/home.svg'
        home_icon = QtGui.QIcon(home_icon_path)
        self.home_btn.setIcon(home_icon)

        alpha_icon_path = '/Users/stu/Documents/3D/QtDesigner/icons/IMAGE' \
                          '/adaptpixelrange.svg'
        alpha_icon = QtGui.QIcon(alpha_icon_path)
        self.alpha_sort.setIcon(alpha_icon)

        set_proj_icon_path = '/Users/stu/Documents/3D/QtDesigner/icons/BUTTONS/chooser_folder.svg'
        set_proj_icon = QtGui.QIcon(set_proj_icon_path)
        self.set_proj.setIcon(set_proj_icon)

        usd_label_icon_path = '/Users/stu/Downloads/image2vector(4).svg'
        usd_label_icon = QtGui.QPixmap(usd_label_icon_path)
        self.usd_label.setPixmap(usd_label_icon)

        # create connections (/button functionality)
        self.set_proj.clicked.connect(self.set_project)
        self.back_btn.clicked.connect(self.back_button)
        self.fwd_btn.clicked.connect(self.forward_button)
        self.alpha_sort.clicked.connect(self.alpha_sort_button)
        self.fwd_btn.clicked.connect(self.redo_click_forward)
        self.ref_btn.clicked.connect(self.refresh_current_scene_list)
        self.home_btn.clicked.connect(self.go_to_job_dir)
        self.reset_btn.clicked.connect(self.reset_button)
        self.scene_list.doubleClicked.connect(self.double_click_forward)
        self.search_bar.textChanged.connect(self.search_directories)

        # Create layout (how widgets will be organised)
        main_layout = QtWidgets.QVBoxLayout()  # vertical layout

        main_layout.addWidget(self.ui)

        self.setLayout(main_layout)

        self.search_bar.setEnabled(False)
        self.back_btn.setEnabled(False)
        self.fwd_btn.setEnabled(False)
        self.alpha_sort.setEnabled(False)
        self.ref_btn.setEnabled(False)
        self.home_btn.setEnabled(False)

        self.usda_label.setVisible(False)
        self.usdc_label.setVisible(False)

        self.enter_pressed_on_search_bar = False
        self.scene_list.mousePressEvent = self.mousePressEvent
        self.scene_list.keyPressEvent = self.keyPressEvent

        # reload current python panel interface

    def reset_button(self):
        self.tree = Tree()
        self.current_node = self.tree.root
        self.back_stack.clear()
        self.proj = None

        self.proj_name.setText(self.default_proj_name)
        self.proj_path.setText(self.default_proj_path)
        self.job_path.setText(self.default_job_path)
        self.search_bar.installEventFilter(self)

        self.scene_list.clear()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            item = self.scene_list.itemAt(event.pos())
            if item:
                if item.isSelected():
                    self.scene_list.clearSelection()
            else:
                self.scene_list.clearSelection()
        self.enter_pressed_on_search_bar = False
        super(ProjectManager, self).mousePressEvent(event)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            if self.search_bar.hasFocus():
                self.search_bar.clearFocus()
            elif self.enter_pressed_on_search_bar:
                self.scene_list.clearSelection()
                self.search_bar.setFocus()
            else:
                # self.scene_list.clearFocus()  # ? need to fix
                self.scene_list.clearSelection()

            super(ProjectManager, self).keyPressEvent(event)

        elif event.key() == QtCore.Qt.Key_Backspace:
            self.scene_list.clearSelection()
            super(ProjectManager, self).keyPressEvent(event)

        elif event.key() == QtCore.Qt.Key_Delete:
            self.scene_list.clearSelection()
            super(ProjectManager, self).keyPressEvent(event)

        elif event.key() == QtCore.Qt.Key_Return:
            if self.search_bar.hasFocus():
                self.search_bar.clearFocus()
                self.scene_list.setCurrentRow(0)
                self.scene_list.setFocus()
                self.enter_pressed_on_search_bar = True
            else:
                self.double_click_forward()
                self.enter_pressed_on_search_bar = False
            print(self.enter_pressed_on_search_bar)
            super(ProjectManager, self).keyPressEvent(event)

        elif event.key() == QtCore.Qt.Key_Left:
            if self.scene_list.hasFocus():
                self.back_button()

        elif event.key() == QtCore.Qt.Key_Right:
            if self.scene_list.hasFocus():
                self.double_click_forward()

        elif event.matches(QKeySequence("Ctrl+Backspace")) and \
                self.search_bar.hasFocus():
            self.search_bar.clear()
            super(ProjectManager, self).keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() not in (QtCore.Qt.Key_Up, QtCore.Qt.Key_Down,
                               QtCore.Qt.Key_Return):
            self.enter_pressed_on_search_bar = False
        super(ProjectManager, self).keyReleaseEvent(event)

    def set_project(self):
        set_job = hou.ui.selectFile(title='Select Project Folder',
                                    file_type=hou.fileType.Directory)
        hou.hscript('setenv JOB=' + set_job)
        self.proj = hou.getenv('JOB')

        self.tree = Tree(self.proj)
        self.current_node = self.tree.root  # create a new node
        self.tree.add_path(self.proj)  # add path to tree node

        proj_name = '  USD Project:  ' + set_job.split('/')[-2]
        set_job = 'JOB:  ' + os.path.dirname(set_job)
        proj_path = 'Path:  ' + set_job
        self.proj_name.setText(proj_name)
        self.job_path.setText(set_job)
        self.proj_path.setText(proj_path)

        #  Create a Node Instance
        self.current_node = self.tree.root
        self.update_scene_list()

    def go_to_job_dir(self):
        self.current_node.path = self.proj
        self.update_scene_list()

    def update_scene_list(self):
        self.scene_list.clear()
        self.current_node.subdirs_present = False
        if self.proj:
            self.search_bar.setEnabled(True)
            self.back_btn.setEnabled(True)
            self.fwd_btn.setEnabled(True)
            self.alpha_sort.setEnabled(True)
            self.ref_btn.setEnabled(True)
            self.home_btn.setEnabled(True)

        self.current_node.path = self.current_node.path + '/'
        if self.current_node.path[-2:] == '//':
            self.current_node.path = self.current_node.path[:-1]

        # print("current node:    " + str(self.current_node))
        # print("node path:    " + self.current_node.path)
        # print("node children []:    " + str(self.current_node.children))

        sorted_items = []
        items = os.listdir(self.current_node.path)

        font = QtGui.QFont("Consolas", 12)
        self.usd_items = []
        self.non_usd_items = []
        max_usdc_width = 0
        usda_file_count = 0
        usdc_file_count = 0
        usda_file_present = False
        usdc_file_present = False

        # grab total values of current node
        for file in items:
            path = os.path.join(self.current_node.path, file)
            if os.path.isdir(path):
                sorted_items.append(file)
                sorted_items.sort()
            for root, dirs, files in os.walk(path):
                for filename in files:
                    if filename.endswith('.usda'):
                        usda_file_count += 1
                    if filename.endswith('.usdc'):
                        usdc_file_count += 1
            max_usdc_width = max(max_usdc_width, len(str(usdc_file_count)))

        # Set visibility & width of usda/usdc labels
        if usda_file_count > 0 or usdc_file_count > 0:
            usda_file_present = usda_file_count > 0
            usdc_file_present = usdc_file_count > 0

        if usda_file_present and usdc_file_present:
            self.usda_label.setVisible(True)
            self.usdc_label.setVisible(True)
            self.usda_label.setText("usda")
            self.usda_label.setMinimumWidth(40)
        elif not usda_file_present and not usdc_file_present:
            self.usda_label.setVisible(False)
            self.usdc_label.setVisible(False)
            self.usda_label.setText("usda")
            self.usda_label.setMinimumWidth(40)
        elif usda_file_present and not usdc_file_present:
            self.usda_label.setVisible(True)
            self.usda_label.setText("      usda")
            self.usda_label.setMinimumWidth(45)
            # Adjust layout of usda label
            layout = QHBoxLayout()
            layout.addWidget(self.usda_label)
            layout.addStretch(1)  # Set stretch factor of usda label to 1
            layout.addWidget(self.usdc_label)
            self.setLayout(layout)
            self.usdc_label.setVisible(False)
        elif not usda_file_present and usdc_file_present:
            self.usda_label.setVisible(False)
            self.usdc_label.setVisible(True)
            self.usda_label.setText("usda")
            self.usda_label.setMinimumWidth(40)

        # print("items before sorting:    ", items)
        #
        # # Create a list of selected items that don't end with .usda or .usdc
        # sorted_items = [item for item in items if not item.endswith('.usda') and not item.endswith('.usdc')]
        #
        # # Sort the selected items
        # sorted_items.sort()
        #
        # # Replace duplicates in the original list with items from the sorted list
        # sorted_items_index = 0
        # for i in range(len(items)):
        #     if items[i] in sorted_items:
        #         items[i] = sorted_items[sorted_items_index]
        #         sorted_items_index += 1
        #

        sorted_items.sort()
        sorted_items_index = 0
        for i in range(len(items)):
            if items[i] in sorted_items:
                items[i] = sorted_items[sorted_items_index]
                sorted_items_index += 1
        # ! Sort function will go around here
        print("items after sorting:    ", items)


        # get all usd files in current node & subdirs
        for file in items:
            path = os.path.join(self.current_node.path, file)
            if os.path.isdir(path):  # if item is a directory
                usda_file_count = 0
                usdc_file_count = 0
                for root, dirs, files in os.walk(path):
                    for filename in files:
                        if filename.endswith('.usda'):
                            usda_file_count += 1
                        elif filename.endswith('.usdc'):
                            usdc_file_count += 1

                str_length = len(str(usdc_file_count))
                usdc_padding = '&nbsp;' * (max_usdc_width - str_length)

                if usda_file_count == 0 and usdc_file_count == 0:
                    usda_file_count = '&nbsp;' * 3
                    usdc_file_count = '&nbsp;' * 3
                    item_text = f"<font color='#1F8ECD'>" \
                                f"{usda_file_count}</font>{usdc_padding}  " \
                                f"<font color='#5DAADA'>" \
                                f"{usdc_file_count}</font> "
                elif usda_file_count == 0:
                    usda_file_count = '&nbsp;' * 3
                    item_text = f"<font color='#1F8ECD'>" \
                                f"{usda_file_count}</font>{usdc_padding}  " \
                                f"<font color='#5DAADA'>" \
                                f"({usdc_file_count})</font> "
                elif usdc_file_count == 0:
                    usdc_file_count = '&nbsp;' * 3
                    item_text = f"<font color='#1F8ECD'>(" \
                                f"{usda_file_count})</font>{usdc_padding}  " \
                                f"<font color='#5DAADA'>" \
                                f"{usdc_file_count}</font> "
                else:
                    item_text = f"<font color='#1F8ECD'>(" \
                                f"{usda_file_count})</font>{usdc_padding}  " \
                                f"<font color='#5DAADA'>" \
                                f"({usdc_file_count})</font> "

                item = QtWidgets.QListWidgetItem(f"{file}")
                item.setTextAlignment(QtCore.Qt.AlignLeft)
                item.order = QtCore.Qt.DescendingOrder

                item_widget = QtWidgets.QWidget()

                item_label = QtWidgets.QLabel(item_text)
                item_label.setAlignment(QtCore.Qt.AlignRight)
                item_label.setFont(font)

                item_layout = QtWidgets.QHBoxLayout(item_widget)
                item_layout.setContentsMargins(0, 0, 0, 0)
                item_layout.addWidget(item_label)

                self.non_usd_items.append((item, item_widget))

                self.tree.add_path(path + '/')  # sequential paths added
                self.tree.node = self.current_node
                self.current_node.subdirs_present = True

            elif file.endswith('.usda'):
                list_widget = QtWidgets.QListWidget()
                file = QtWidgets.QListWidgetItem(file)
                file.setForeground(QtGui.QColor('#1F8ECD'))

                list_widget.addItem(file.text())
                self.usd_items.append(file)

            elif file.endswith('.usdc'):
                list_widget = QtWidgets.QListWidget()
                file = QtWidgets.QListWidgetItem(file)
                file.setForeground(QtGui.QColor('#5DAADA'))

                list_widget.addItem(file.text())
                self.usd_items.append(file)

        # Add the non-usd items first
        for item, item_widget in self.non_usd_items:
            self.scene_list.addItem(item)
            self.scene_list.setItemWidget(item, item_widget)

        # Add a separator item
        if self.usd_items and self.non_usd_items:
            separator = QtWidgets.QListWidgetItem()
            separator.setFlags(QtCore.Qt.NoItemFlags)
            separator.setSizeHint(QtCore.QSize(0, 20))
            separator.setBackground(
                QtGui.QColor(128, 128, 128))

            line = QtWidgets.QFrame()
            line.setFrameShape(QtWidgets.QFrame.HLine)
            # line.setFrameShadow(QtWidgets.QFrame.Sunken)
            line.setLineWidth(1)
            line.setContentsMargins(7, 0, 7, 0)

            # Set the background color of the separator
            palette = line.palette()
            palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(
                128, 128, 128))
            line.setPalette(palette)

            # Add the line widget to the separator list widget item
            self.scene_list.addItem(separator)
            self.scene_list.setItemWidget(separator, line)

        # Add usd items
        for item in self.usd_items:
            self.scene_list.addItem(item)

        return self.scene_list

    def back_button(self):
        print(len(self.back_stack))
        print("<<<    back button pressed! :D    >>>")
        home_dir = os.path.expanduser("~")
        job_path = self.job_path.text().split('JOB:  ')[1].replace('$HOME',
                                                                   home_dir)

        if os.path.abspath(self.current_node.path) == job_path:
            print("Can't go back any further on the $JOB PATH")
            return
        else:
            self.back_stack.append(self.current_node.path)
            self.current_node.path = os.path.dirname(
                os.path.dirname(self.current_node.path))
            print("going back to:    " + self.current_node.path)
            self.update_scene_list()

    def forward_button(self):
        selected_item = self.scene_list.currentItem()

        if selected_item is not None and os.path.isdir(os.path.join(
                self.current_node.path, selected_item.text())):
            selected_path = os.path.join(self.current_node.path,
                                         selected_item.text())
            self.back_stack.clear()
            for child in self.current_node.children:
                if child.path == selected_path:
                    self.current_node = child
                    self.update_scene_list()
                    break
        elif selected_item is not None and selected_item.text(
        ).endswith(('.usda', '.usdc')):
            print("you have selected a .USD file")
            return
        else:
            return

        self.current_node.path = os.path.join(
            self.current_node.path + selected_item.text())

        print("<<<    forward button pressed! :D    >>>")
        self.update_scene_list()

    def double_click_forward(self):
        self.back_stack.clear()
        self.forward_button()

    def redo_click_forward(self):
        selected_item = self.scene_list.currentItem()
        print("<<<    redo click forward button pressed! :D    >>>")
        print("stack length:    " + str(len(self.back_stack)))

        if selected_item is None:
            if len(self.back_stack) >= 1 and self.current_node.subdirs_present:
                node = self.back_stack.pop()
                self.current_node.path = node
                self.update_scene_list()
                print("stack length:    " + str(len(self.back_stack)))
            elif len(self.back_stack) <= 0 and \
                    self.current_node.subdirs_present:
                print("    No more redos!    ")
                return
            else:
                print("    Can't go back any further!    ")
                return

    def refresh_current_scene_list(self):
        self.update_scene_list()

    def alpha_sort_button(self, items):
        print("alpha_sort_button called!")
        # print("alpha_sort_button called with alpha_sort =",
        #       self.alpha_sort_button)
        # print("alpha_sort checkbox state before sorting:", self.alpha_sort.isChecked())
        # if not items:
        #     return items
        # if not any(file.endswith(('.usda', '.usdc')) for file in items):
        #     if self.alpha_sort.isChecked():
        #         items.sort()
        #     else:
        #         items.sort(reverse=True)
        # else:
        #     usd_items = [file for file in items if file.endswith(('.usda', '.usdc'))]
        #     non_usd_items = [file for file in items if not file.endswith(('.usda', '.usdc'))]
        #     if self.alpha_sort.isChecked():
        #         usd_items.sort()
        #         non_usd_items.sort()
        #     else:
        #         usd_items.sort(reverse=True)
        #         non_usd_items.sort(reverse=True)
        #     items = non_usd_items + usd_items
        # print("alpha_sort checkbox state after sorting:", self.alpha_sort.isChecked())
        # return items

    # if self.current_order == Qt.AscendingOrder:
        #     self.scene_list.sortItems(Qt.DescendingOrder)
        #     self.current_order = Qt.DescendingOrder
        # else:
        #     self.scene_list.sortItems(Qt.AscendingOrder)
        #     self.current_order = Qt.AscendingOrder

    def search_directories(self):
        query = self.search_bar.text()
        if query:
            self.scene_list.clear()
            self.current_node.subdirs_present = False
            items = os.listdir(self.current_node.path)
            items.sort()
            for file in items:
                path = os.path.join(self.current_node.path, file)
                if os.path.isdir(path) and query.lower() in file.lower():
                    self.scene_list.addItem(file)
                    self.tree.add_path(path + '/')
                    self.tree.node = self.current_node
                    self.current_node.subdirs_present = True
                elif file.endswith('.usda') and query.lower() in file.lower():
                    self.scene_list.addItem(file)
        else:
            self.update_scene_list()
