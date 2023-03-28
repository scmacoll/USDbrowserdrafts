import os
import hou


def import_usd(selected_item):
    # usd_dir = hou.ui.selectFile(title='Select USD File',
    #                             file_type=hou.fileType.Any, pattern='*.usda *.usdc *.usdz')

    loader = hou.node('/obj').createNode('geo', 'usd_loader')
    usd_import = loader.createNode('usdimport')
    usd_import.parm('filepath1').set(selected_item)
    usd_import.parm('importtraversal').set('std:boundables')

    class MyPanel(hou.Panel):
        def __init__(self):
            hou.Panel.__init__(self)
            self.setWindowTitle("My Panel")
            self.setLayout(QtWidgets.QVBoxLayout())
            self.layout().addWidget(self.ui)

        def createOutput(self):
            return self

    my_panel = MyPanel()
    hou.ui.addPaneTab(my_panel, "My Panel", True)


"""
In the code above, the `ProjectManager` class inherits from `hou.Panel`, which provides the necessary functionality for adding the panel to Houdini as a standalone pane tab. The `__init__` method creates the UI using the same code as before, and then creates a pane tab for the panel using the `hou.ui.addPaneTab()` method. The `hou.ui.setPaneTabType()` method sets the pane tab type to `hou.ui.paneTabType.Pinned`, which allows the user to tear off the pane tab. The `hou.ui.setPaneTabIcon()` method sets the icon for the pane tab.

The `onPaneTabClosed` method is called when the pane tab is closed, and removes the pane tab using the `hou.ui.removePaneTab()` method.

Note that the `ProjectManager` class should be saved in a Python module file (.py) and loaded in Houdini using the `hou.session` module. You can do this by creating a new Python module file in your Houdini scripts directory, and adding the following code:

```python
import hou

# Import the ProjectManager class from your module file
from my_module_file import ProjectManager

# Create an instance of the ProjectManager class
project_manager = ProjectManager()

# Add the instance to the Houdini session
hou.session.project_manager = project_manager
"""