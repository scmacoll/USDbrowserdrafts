# noinspection PyUnresolvedReferences
# def update_scene_list(self):
#     self.scene_list.clear()
#     self.current_node.subdirs_present = False
#
#     self.current_node.path = self.current_node.path + '/'
#     if self.current_node.path[-2:] == '//':
#         self.current_node.path = self.current_node.path[:-1]
#
#     # print("current node:    " + str(self.current_node))
#     # print("node path:    " + self.current_node.path)
#     # print("node children []:    " + str(self.current_node.children))
#
#     items = os.listdir(self.current_node.path)
#     items.sort()
#
#     max_usdc_width = 0
#     usd_items = []
#     non_usd_items = []
#     for file in items:
#         path = os.path.join(self.current_node.path, file)
#         if os.path.isdir(path):
#             usdc_file_count = 0
#             for root, dirs, files in os.walk(path):
#                 for filename in files:
#                     if filename.endswith('.usdc'):
#                         usdc_file_count += 1
#             max_usdc_width = max(max_usdc_width, len(str(usdc_file_count)))
#
#             usda_file_count = 0
#             usdc_file_count = 0
#             for root, dirs, files in os.walk(path):
#                 for filename in files:
#                     if filename.endswith('.usda'):
#                         usda_file_count += 1
#                     elif filename.endswith('.usdc'):
#                         usdc_file_count += 1
#
#             str_length = len(str(usdc_file_count))
#             usdc_padding = ' ' * (max_usdc_width - str_length)
#
#             if usda_file_count == 0:
#                 usda_file_count = '   '
#                 item_text = f"{usda_file_count}{usdc_padding}    (" \
#                             f"{usdc_file_count}) "
#             elif usdc_file_count == 0:
#                 usdc_file_count = '   '
#                 item_text = f"({usda_file_count}){usdc_padding}    " \
#                             f"{usdc_file_count} "
#             else:
#                 item_text = f"({usda_file_count}){usdc_padding}    (" \
#                             f"{usdc_file_count}) "
#
#             item = QtWidgets.QListWidgetItem(f"{file}")
#
#             item_widget = QtWidgets.QWidget()
#             item_layout = QtWidgets.QHBoxLayout(item_widget)
#             item_layout.setContentsMargins(0, 0, 0, 0)
#
#             item_label = QtWidgets.QLabel(item_text)
#             item.setTextAlignment(QtCore.Qt.AlignLeft)
#             font = QtGui.QFont("Consolas", 12)
#             item_label.setFont(font)
#             item_label.setAlignment(QtCore.Qt.AlignRight)
#             item_layout.addWidget(item_label)
#
#             usd_items.append((item, item_widget))
#
#             self.tree.add_path(path + '/')  # sequential paths added
#             self.tree.node = self.current_node
#             self.current_node.subdirs_present = True
#
#         elif file.endswith('.usda') or file.endswith('.usdc'):
#             non_usd_items.append(file)
#
#     # Add the non-usd items first
#     for item in non_usd_items:
#         self.scene_list.addItem(item)
#
#     # Add a separator item
#     if non_usd_items and usd_items:
#         separator = QtWidgets.QListWidgetItem()
#         separator.setFlags(QtCore.Qt.NoItemFlags)
#         separator.setSizeHint(QtCore.QSize(0, 2))
#         separator.setBackground(
#             QtGui.QColor(128, 128, 128))  # Set the background color to gray
#         self.scene_list.addItem(separator)
#
#     # Add the usd items
#     for item, item_widget in usd_items:
#         self.scene_list.addItem(item)
#         self.scene_list.setItemWidget(item, item_widget)
#
#     return self.scene_list
#
#
# # noinspection PyUnresolvedReferences
# def update_scene_list(self):
#     self.scene_list.clear()
#     self.current_node.subdirs_present = False
#
#     self.current_node.path = self.current_node.path + '/'
#     if self.current_node.path[-2:] == '//':
#         self.current_node.path = self.current_node.path[:-1]
#
#     # print("current node:    " + str(self.current_node))
#     # print("node path:    " + self.current_node.path)
#     # print("node children []:    " + str(self.current_node.children))
#
#     items = os.listdir(self.current_node.path)
#     items.sort()
#
#     max_usdc_width = 0
#     usd_items = []
#     non_usd_items = []
#     for file in items:
#         path = os.path.join(self.current_node.path, file)
#         if os.path.isdir(path):
#             usdc_file_count = 0
#             for root, dirs, files in os.walk(path):
#                 for filename in files:
#                     if filename.endswith('.usdc'):
#                         usdc_file_count += 1
#             max_usdc_width = max(max_usdc_width, len(str(usdc_file_count)))
#
#     for file in items:
#         path = os.path.join(self.current_node.path, file)
#         if os.path.isdir(path):
#             usda_file_count = 0
#             usdc_file_count = 0
#             for root, dirs, files in os.walk(path):
#                 for filename in files:
#                     if filename.endswith('.usda'):
#                         usda_file_count += 1
#                     elif filename.endswith('.usdc'):
#                         usdc_file_count += 1
#
#             str_length = len(str(usdc_file_count))
#             usdc_padding = ' ' * (max_usdc_width - str_length)
#
#             if usda_file_count == 0:
#                 usda_file_count = '   '
#                 item_text = f"{usda_file_count}{usdc_padding}    (" \
#                             f"{usdc_file_count}) "
#             elif usdc_file_count == 0:
#                 usdc_file_count = '   '
#                 item_text = f"({usda_file_count}){usdc_padding}    " \
#                             f"{usdc_file_count} "
#             else:
#                 item_text = f"({usda_file_count}){usdc_padding}    (" \
#                             f"{usdc_file_count}) "
#
#             item = QtWidgets.QListWidgetItem(f"{file}")
#
#             item_widget = QtWidgets.QWidget()
#             item_layout = QtWidgets.QHBoxLayout(item_widget)
#             item_layout.setContentsMargins(0, 0, 0, 0)
#
#             item_label = QtWidgets.QLabel(item_text)
#             item.setTextAlignment(QtCore.Qt.AlignLeft)
#             font = QtGui.QFont("Consolas", 12)
#             item_label.setFont(font)
#             item_label.setAlignment(QtCore.Qt.AlignRight)
#             item_layout.addWidget(item_label)
#
#             usd_items.append((item, item_widget))
#
#             self.tree.add_path(path + '/')  # sequential paths added
#             self.tree.node = self.current_node
#             self.current_node.subdirs_present = True
#
#         elif file.endswith('.usda') or file.endswith('.usdc'):
#             non_usd_items.append(file)
#
#     # Add the non-usd items first
#     for item in non_usd_items:
#         self.scene_list.addItem(item)
#
#     # Add a separator item
#     if non_usd_items and usd_items:
#         separator = QtWidgets.QListWidgetItem()
#         separator.setFlags(QtCore.Qt.NoItemFlags)
#         separator.setSizeHint(QtCore.QSize(0, 2))
#         separator.setBackground(
#             QtGui.QColor(128, 128, 128))  # Set the background color to gray
#         self.scene_list.addItem(separator)
#
#     # Add the usd items
#     for item, item_widget in usd_items:
#         self.scene_list.addItem(item)
#         self.scene_list.setItemWidget(item, item_widget)
#
#     return self.scene_list

#########################################3

"""The error you're encountering is because my_item_list is a Python list object, and sortItems() is not a valid method for lists.

The sortItems() method is a method of QListWidget objects, which can be used to sort the items in a list widget based on some criterion.

To fix this error, you need to make sure that the sortItems() method is called on a QListWidget object, rather than a Python list.

If you want to sort the items in the scene_list object (which is a QListWidget object), you can replace self.my_item_list.sortItems(Qt.DescendingOrder) with self.scene_list.sortItems(Qt.DescendingOrder).

Alternatively, if you want to sort the items in my_item_list, you could convert it to a QListWidget object first and then call sortItems() on it. Here's an example:"""


    def alpha_sort_button(self):
        # Convert my_item_list to a QListWidget object
        my_list_widget = QtWidgets.QListWidget()
        for item in self.my_item_list:
            my_list_widget.addItem(item.text())

        # Sort the items in the list widget
        my_list_widget.sortItems(Qt.DescendingOrder)

        # Replace the items in my_item_list with the sorted items
        self.my_item_list = []
        for i in range(my_list_widget.count()):
            self.my_item_list.append(my_list_widget.item(i))

        # Add the sorted items to the scene_list widget
        for item in self.my_item_list:
            self.scene_list.addItem(item)

        # rest of the method code


"""This code creates a new QListWidget object called my_list_widget, adds the items from my_item_list to it, sorts the items using sortItems(), and then replaces the items in my_item_list with the sorted items. Finally, the sorted items are added to the scene_list widget."""