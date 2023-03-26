import os
import hou

usd_dir = hou.ui.selectFile(title='Select USD File',
                            file_type=hou.fileType.Any, pattern='*.usda *.usdc *.usdz')
usd_dir_expanded = hou.expandString(usd_dir)

loader = hou.node('/obj').createNode('geo', 'usd_loader')

usd_import = loader.createNode('usdimport')
parm_file = usd_import.parm('filepath1').set(usd_dir)
parm_trav = usd_import.parm('importtraversal').set('std:boundables')

