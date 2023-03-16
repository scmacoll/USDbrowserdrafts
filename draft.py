# noinspection PyUnresolvedReferences
def update_scene_list(self):
    self.scene_list.clear()
    self.current_node.subdirs_present = False

    self.current_node.path = self.current_node.path + '/'
    if self.current_node.path[-2:] == '//':
        self.current_node.path = self.current_node.path[:-1]

    print("current node:    " + str(self.current_node))
    print("node path:    " + self.current_node.path)
    print("node children []:    " + str(self.current_node.children))

    items = os.listdir(self.current_node.path)
    items.sort()

    for file in items:
        path = os.path.join(self.current_node.path, file)
        if os.path.isdir(path):
            usda_file_count = 0
            for root, dirs, files in os.walk(path):
                for filename in files:
                    if filename.endswith('.usda'):
                        usda_file_count += 1

            item_text = f"({usda_file_count})"

            # Create a QHBoxLayout to manage the layout of file and item
            hbox_layout = QtWidgets.QHBoxLayout()

            # Create the file item and align it to the left
            file_item = QtWidgets.QLabel(file)
            file_item.setAlignment(QtCore.Qt.AlignLeft)
            hbox_layout.addWidget(file_item)

            # Create the item and align it to the right
            item = QtWidgets.QLabel(item_text)
            item.setAlignment(QtCore.Qt.AlignRight)
            hbox_layout.addWidget(item)

            # Create a QWidget to hold the QHBoxLayout
            widget = QtWidgets.QWidget()
            widget.setLayout(hbox_layout)

            # Create a QListWidgetItem and set its size hint based on the
            # size of the widget
            list_item = QtWidgets.QListWidgetItem()
            list_item.setSizeHint(widget.sizeHint())

            # Add the widget to the QListWidget
            self.scene_list.addItem(list_item)
            self.scene_list.setItemWidget(list_item, widget)



            item_text = f"({usda_file_count})"
            item = QtWidgets.QListWidgetItem(item_text)
            item.setTextAlignment(QtCore.Qt.AlignRight)
            file = QtWidgets.QListWidgetItem(file)
            file.setTextAlignment(QtCore.Qt.AlignLeft)
            # self.scene_list.addItem(item_text)
            self.scene_list.addItem(file.text() + item.text())
            self.tree.add_path(path + '/')  # sequential paths added
            self.tree.node = self.current_node
            self.current_node.subdirs_present = True
        elif file.endswith('.usda') or file.endswith('.usdc'):
            self.scene_list.addItem(file)




    for file in items:
        path = os.path.join(self.current_node.path, file)
        if os.path.isdir(path):
            self.scene_list.addItem(file)
            self.tree.add_path(path + '/')  # sequential paths added
            self.tree.node = self.current_node
            self.current_node.subdirs_present = True
        elif file.endswith('.usda') or file.endswith('.usdc'):
            self.scene_list.addItem(file)

    return self.scene_list
