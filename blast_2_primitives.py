import hou

# Get the current Python node and find its parent (the Geometry node)
python_node = hou.pwd()
geo_node = python_node.parent()
# Find the first USD import node connected to the Geometry node
usd_import_node = python_node.input(0)

# Get the output of the USD import node
usd_import_output = usd_import_node.geometry()

# Get all primitives from the USD import node
prims = usd_import_output.prims()

# Initialize a set to store unique @name attributes
unique_name = set()

# ! if attrib == "name":

# ! elif attrib == "path":

# Iterate through each primitive
for prim in prims:
    # Get the @path attribute
    prim_name = prim.attribValue("name")
    unique_name.add(prim_name)

# Create blast nodes for each unique @name attribute
for name in unique_name:
    # Create a blast node
    blast_node = geo_node.createNode("blast")

    # Set the node's input to be the output of the USD import node
    blast_node.setInput(0, usd_import_node)

    # Set the group name in the blast node using the @name attribute
    blast_node.parm("group").set("@name=" + name)
    blast_node.parm("negate").set(True)
    blast_node.parm("grouptype").set(4)

geo_node.layoutChildren()
#
# # Get the current Python node and find its parent (the Geometry node)
# python_node = hou.pwd()
# geo_node = python_node.parent()
# # Find the first USD import node connected to the Geometry node
# usd_import_node = python_node.input(0)
#
# # Get the output of the USD import node
# usd_import_output = usd_import_node.geometry()
#
# # Get all primitives from the USD import node
# prims = usd_import_output.prims()
#
# # Initialize a set to store unique @path attributes
# unique_path = set()
#
# # Iterate through each primitive
# for prim in prims:
#     # Get the @path attribute
#     prim_path = prim.attribValue("path")
#     unique_path.add(prim_path)
#
# # Create blast nodes for each unique @path attribute
# for path in unique_path:
#     # Create a blast node
#     blast_node = geo_node.createNode("blast")
#
#     # Set the node's input to be the output of the USD import node
#     blast_node.setInput(0, usd_import_node)
#
#     # Set the group path in the blast node using the @path attribute
#     blast_node.parm("group").set("@path=" + path)
#     blast_node.parm("negate").set(True)
#     blast_node.parm("grouptype").set(4)
#
# geo_node.layoutChildren()

# import hou
#
# # Get the current Python node and find its parent (the Geometry node)
# python_node = hou.pwd()
# geo_node = python_node.parent()
# # Find the first USD import node connected to the Geometry node
# usd_import_node = python_node.input(0)
#
# # Get the output of the USD import node
# usd_import_output = usd_import_node.geometry()
#
# # Get all primitives from the USD import node
# prims = usd_import_output.prims()
#
# # Iterate through each primitive
# for i, prim in enumerate(prims):
#     # Create a blast node
#     blast_node = geo_node.createNode("blast")
#
#     # Set the node's input to be the output of the USD import node
#     blast_node.setInput(0, usd_import_node)
#
#     # Set the group name in the blast node
#     blast_node.parm("group").set(str(i))
#     blast_node.parm("negate").set(True)
#     blast_node.parm("grouptype").set(4)
#
# geo_node.layoutChildren()

#################
# TOP PARENT PATH
#
# # Function to extract the top parent path from a given path
# def get_top_parent_path(path):
#     parts = path.split('/')
#     if len(parts) > 2:
#         return '/' + parts[1] + '/' + parts[2]
#     else:
#         return ''
#
# # Get the current Python node and find its parent (the Geometry node)
# python_node = hou.pwd()
# geo_node = python_node.parent()
# # Find the first USD import node connected to the Geometry node
# usd_import_node = python_node.input(0)
#
# # Get the output of the USD import node
# usd_import_output = usd_import_node.geometry()
#
# # Get all primitives from the USD import node
# prims = usd_import_output.prims()
#
# # Initialize a set to store unique top parent @path attributes
# unique_top_parent_paths = set()
#
# # Iterate through each primitive
# for prim in prims:
#     # Get the @path attribute
#     prim_path = prim.attribValue("path")
#     top_parent_path = get_top_parent_path(prim_path)
#     unique_top_parent_paths.add(top_parent_path)
#
# # Create blast nodes for each unique top parent @path attribute
# for path in unique_top_parent_paths:
#     # Create a blast node
#     blast_node = geo_node.createNode("blast")
#
#     # Set the node's input to be the output of the USD import node
#     blast_node.setInput(0, usd_import_node)
#
#     # Set the group name in the blast node using the top parent @path attribute
#     blast_node.parm("group").set("@path=" + path + "/*")
#     blast_node.parm("negate").set(True)
#     blast_node.parm("grouptype").set(4)
#
# geo_node.layoutChildren()
