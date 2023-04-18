def merge_nodes(prim_nodes, geo_node):
    merge_node = geo_node.createNode('merge', 'merge')

    for node in prim_nodes:
        merge_node.setNextInput(node)

    geo_node.layoutChildren()
    merge_node.setDisplayFlag(True)
    merge_node.setRenderFlag(True)


def blast_name(kwargs):

    import hou

    # Get the current Python node and find its parent (the Geometry node)
    current_node = kwargs["node"]
    geo_node = current_node.parent()
    # Find the first USD import node connected to the Geometry node
    usd_import_node = current_node.input(0)

    # Get the output of the USD import node
    usd_import_output = usd_import_node.geometry()

    # Get all primitives from the USD import node
    prims = usd_import_output.prims()

    # Initialize a set to store unique @name attributes
    unique_paths = set()
    unique_names = set()
    prim_nodes = []

    attrib_value = current_node.parm("attrib").eval()
    blast_select = current_node.parm("blastselect").eval()
    path_level = current_node.parm("pathlvl").eval()
    group_param = current_node.parm("group").eval()
    # group_param = hou.evalParm('group')

    # Blast selection: All Primitives
    if blast_select is 0:
        for prim in prims:
            prim_name = prim.attribValue("name")
            prim_path = prim.attribValue("path")

            integers = [int(s) for s in prim_name.split() if s.isdigit()]
            for integer in integers:
                unique_names.add(str(integer))

            unique_paths.add(prim_path)
            unique_names.add(prim_name)

        num_prims = len(prims)

        if len(unique_paths) is num_prims:
            group_attrib = "path"
            unique_values = unique_paths
        elif len(unique_names) is num_prims:
            group_attrib = "name"
            unique_values = unique_names
        else:
            group_attrib = "integer"
            unique_values = set(str(integer) for integer in range(num_prims))

        for value in unique_values:
            prim_value = "prim_" + str(value)
            blast_node = geo_node.createNode("blast", prim_value)
            blast_node.setInput(0, current_node)

            if group_attrib is "path":
                blast_node.parm("group").set("@path=" + value)
            elif group_attrib is "name":
                blast_node.parm("group").set("@name=" + value)
            else:
                blast_node.parm("group").set(value)

            blast_node.parm("negate").set(True)
            blast_node.parm("grouptype").set(4)

            prim_nodes.append(blast_node)

        merge_nodes(prim_nodes, geo_node)

    # Blast selection: Group
    elif blast_select is 2 and group_param is not "":
        group_list = group_param.split(',')

        for group in group_list:
            group = group.strip()
            if not group:
                continue

            group_name = "group_" + str(group)
            blast_node = geo_node.createNode("blast", group_name)
            blast_node.setInput(0, current_node)
            blast_node.parm("group").set(group)
            blast_node.parm("negate").set(True)
            blast_node.parm("grouptype").set(4)

            prim_nodes.append(blast_node)
        merge_nodes(prim_nodes, geo_node)

    # Blast selection: Attribute, Attribute: @Name
    elif blast_select is 1 and attrib_value is 0:

        for prim in prims:
            prim_name = prim.attribValue("name")
            unique_names.add(prim_name)

        for name in unique_names:
            # Create a blast node
            blast_node = geo_node.createNode("blast", name)

            # Set the node's input to be the output of the current node
            blast_node.setInput(0, current_node)

            # Set the group name in the blast node using the @name attribute
            blast_node.parm("group").set("@name=" + name)
            blast_node.parm("negate").set(True)
            blast_node.parm("grouptype").set(4)

            prim_nodes.append(blast_node)

        merge_nodes(prim_nodes, geo_node)
    # Blast selection = Attribute, Attribute = @Path
    elif blast_select is 1 and attrib_value is 1:

        # Path level values
        for prim in prims:
            prim_path = prim.attribValue("path")
            path_parts = prim_path.split("/")
            if len(path_parts) > path_level:
                root_path = path_parts[1]
                if path_level is 0:
                    blast_path = '/' + root_path + '/*'
                else:
                    blast_path = "/" + "/".join(
                        path_parts[1:path_level+2]) + "/*"
                unique_names.add((root_path, blast_path))

        for path, blast_path in unique_names:
            split_path = blast_path.split("/")
            current_path = split_path[-2]

            blast_node = geo_node.createNode("blast", current_path)
            blast_node.setInput(0, current_node)
            blast_node.parm("group").set("@path=" + blast_path)
            blast_node.parm("negate").set(True)
            blast_node.parm("grouptype").set(4)

            prim_nodes.append(blast_node)

        merge_nodes(prim_nodes, geo_node)

    else:
        return


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

#  ######################################################

"""
def blast_name(kwargs):

    import hou

    # Get the current Python node and find its parent (the Geometry node)
    current_node = kwargs["node"]
    geo_node = current_node.parent()
    # Find the first USD import node connected to the Geometry node
    usd_import_node = current_node.input(0)

    # Get the output of the USD import node
    usd_import_output = usd_import_node.geometry()

    # Get all primitives from the USD import node
    prims = usd_import_output.prims()

    # Initialize a set to store unique @name attributes
    unique_name = set()
    prim_nodes = []

    attrib_value = current_node.parm("attrib").eval()
    blast_select = current_node.parm("blastselect").eval()

    if blast_select == 1 and attrib_value == 0:

        for prim in prims:
            prim_name = prim.attribValue("name")
            unique_name.add(prim_name)

        for name in unique_name:
            # Create a blast node
            blast_node = geo_node.createNode("blast")

            # Set the node's input to be the output of the current node
            blast_node.setInput(0, current_node)

            # Set the group name in the blast node using the @name attribute
            blast_node.parm("group").set("@name=" + name)
            blast_node.parm("negate").set(True)
            blast_node.parm("grouptype").set(4)

            prim_nodes.append(blast_node)

    elif blast_select == 1 and attrib_value == 1:

        for prim in prims:
            prim_name = prim.attribValue("path")
            unique_name.add(prim_name)

        for path in unique_name:
            # Create a blast node
            blast_node = geo_node.createNode("blast")

            # Set the node's input to be the output of the current node
            blast_node.setInput(0, current_node)

            # Set the group path in the blast node using the @path attribute
            blast_node.parm("group").set("@path=" + path)
            blast_node.parm("negate").set(True)
            blast_node.parm("grouptype").set(4)

            prim_nodes.append(blast_node)

    merge_node = geo_node.createNode('merge', 'merge')

    for node in prim_nodes:
        merge_node.setNextInput(node)

    geo_node.layoutChildren()
    merge_node.setDisplayFlag(True)
    merge_node.setRenderFlag(True)
"""