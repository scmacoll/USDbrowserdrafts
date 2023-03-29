import os
import hou


def import_usd(selected_item):
    # usd_dir = hou.ui.selectFile(title='Select USD File',
    #                             file_type=hou.fileType.Any, pattern='*.usda *.usdc *.usdz')

    loader = hou.node('/obj').createNode('geo', 'usd_loader')
    usd_import = loader.createNode('usdimport')
    usd_import.parm('filepath1').set(selected_item)
    usd_import.parm('importtraversal').set('std:boundables')
