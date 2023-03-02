import os
from PySide2 import QtWidgets
import hou

proj = hou.getenv('JOB') + '/'


def open_scene(item):
    print('open hip file')
    hip_file = proj + item.data()
    # print hip_file
    # open hip_file
    hou.hipFile.load(hip_file)


def create_interface():
    widget = QtWidgets.QLabel(proj)
    list_widget = QtWidgets.QListWidget()

    for file in os.listdir(proj):
        list_widget.addItem(file)

    # connect list items to function
    list_widget.doubleClicked.connect(open_scene)

    return list_widget
