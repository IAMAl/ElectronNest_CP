def BackTrack(am, row_no, paths, stack_a, stack_b):
    """
    Back Tracker

    Arguments:
        am:             Inverse-Adjacency Matrix
        row_no:         Tracking Node-ID
        paths:          Set of Tracked Paths
        stack_a:        Stack for Branch-Dest
        stack_b:        Stack for Branch-Root

    Function
        - Generate set of paths from root
    """

    #print("enter to row-{}".format(row_no))
    #print(stack_a)
    stack_a_ = []
    for clm_no in range(row_no+1, len(am)-1, +1):
        if am[row_no][clm_no] == 1:
            stack_a_.append(clm_no)

    #print("find:{}".format(stack_a_))
    #print("stack:{}".format(stack_a))

    if len(stack_a_) > 1:
        stack_b.append(row_no)
        stack_a.append(stack_a_[1])
        node_id = stack_a_[0]
        paths[-1].append(node_id)
        BackTrack(am, node_id, paths, stack_a, stack_b)

    elif len(stack_a_) == 1:
        node_id = stack_a_[0]
        paths[-1].append(node_id)
        #print("pres branch")
        BackTrack(am, node_id, paths, stack_a, stack_b)

    elif len(stack_a) > 0:
        paths.append([])

        root_id = stack_b.pop(-1)
        paths[-1].append(root_id)

        node_id = stack_a.pop(-1)
        paths[-1].append(node_id)
        #print("next branch")
        BackTrack(am, node_id, paths, stack_a, stack_b)

    elif len(stack_a_) == 0:
        #print("exit from row-{}".format(row_no))
        return paths

    #print("exit from row-{}".format(row_no))
    return paths


def TrackFormatter(paths):
    paths_ = []

    for index, path in enumerate(paths):
        for chk_index in range(index+1, len(paths), +1):
            if paths[chk_index][0] in path:
                path_id = path.index(paths[chk_index][0])
                paths_ = path[0:path_id]+paths_

    return paths_


def BackPath(PATH_FORMAT=False, r_file_path="./", r_file_name="@main()_bblock_15", w_file_path="./", w_file_name="@main()_bblock_15"):
    """
    Back Path Generator

    Arguments:
        r_file_path:  path for input flle
        r_file_name:  input file name
        w_file_path:  path for output flle
        w_file_name:  output file name

    Function
        - Generate set of paths from root
    """

    #Setting Up Node List
    bb_node_list = []
    with open(r_file_path+r_file_name+"_node_list_inv.txt", "r") as bb_dfg_nl:
        for node in bb_dfg_nl:
            node = node.replace('\n', '')
            node = node.split(' ')
            bb_node_list.append([node[0], node[1]])

    #Setting Up Inverse-AM
    bb_inv_am = []
    bb_inv_am.append([])
    with open(r_file_path+r_file_name+"_am_inv.txt", "r") as bb_dfg_am:
        for no, row in enumerate(bb_dfg_am):
            row = row.replace('\n', '')
            row = row.replace('[', '')
            row = row.replace(']', '')
            row = row.split(' ')
            for elm in row:
                if len(elm) != 0:
                    if elm == "1":
                        bb_inv_am[no].append(1)
                    else:
                        bb_inv_am[no].append(0)

            bb_inv_am.append([])

    find = False
    with open(w_file_path+w_file_name+"_bpath.txt", "w") as bpath:
        #Find Store Instr
        no_stores = 0

        for node_id, node in enumerate(bb_node_list):
            node_no = node[0]
            node_opcode = node[1]

            paths = []

            if "store" in node_opcode or "br" in node_opcode or "ret" in node_opcode:
                #print(node_opcode)
                #Find Root Instruction
                find = True
                no_stores += 1

                paths.append([])
                paths[0].append(node_id)

                stack_a = []
                stack_b = []

                paths = BackTrack(bb_inv_am, node_id, paths, stack_a, stack_b)

                if PATH_FORMAT:
                    paths = TrackFormatter(paths)

                if no_stores > 0:
                    bpath.writelines(map(str, paths))

        if no_stores == 0:
            bpath.write("there is no path")


def RootFinder(paths, path, node_id):

    for index, chk_path in enumerate(paths):
        if node_id in chk_path:
            #print("check node-id = {} in path: {}".format(node_id, chk_path))
            index_ = chk_path.index(node_id)

            if index_ > 0:
                #print("find at {}".format(index_))
                popped_path = paths.pop(-1)
                node_id = popped_path[0]
                part_path = popped_path[0:index_]
                #print("next  node-id = {} in paths:{}".format(node_id, paths))
                if len(paths) > 0:
                    path_, pos = RootFinder(paths, path, node_id)
                    path = path_+part_path
                elif index_ > 0:
                    path = part_path
                else:
                    path = [node_id]

    #print("exit:{}".format(path))   
    return path, index_


def StLdMarker(r_file_path="./", r_file_name="@main()_bblock_12", w_file_path="./", w_file_name="@main()_bblock_12"):
    """
    Store&Load Maker

    Arguments:
        r_file_path:  path for input flle
        r_file_name:  input file name
        w_file_path:  path for output flle
        w_file_name:  output file name

    Function
        - Generate set of paths from store-root
        - Generate set of paths to load-leaf
        - Generate set of paths from store-root to load-leaf
    """

    #Setting Up Node List
    bb_node_list = []
    with open(r_file_path+r_file_name+"_node_list_inv.txt", "r") as bb_dfg_nl:
        for node in bb_dfg_nl:
            node = node.replace('\n', '')
            node = node.split(' ')
            bb_node_list.append([node[0], node[1]])

    #Setting Up Path List
    backpaths = []
    paths_ = []
    with open(w_file_path+w_file_name+"_bpath.txt", "r") as bpath:
        for paths in bpath:
            paths = paths.split("][")
            paths[0] = paths[0][1:]
            paths[-1] = paths[-1][0:len(paths[-1])-1]

        for path_ in paths:
            path_ = path_.split(", ")
            list_path = []
            for node_id in path_:
                if node_id != '' and not 'here is no pa' in node_id:
                    list_path.append(int(node_id))

            if len(list_path) > 0:
                paths_.append(list_path)

        backpaths = paths_


    num_stores = 0
    num_root_loads = 0
    num_leaf_loads = 0
    st_root_paths = []
    ld_root_paths = []
    ld_leaf_paths = []
    stld_paths = []
    st_root_index = 0
    ld_root_index = 0
    ld_leaf_index = 0
    for index, path in enumerate(backpaths):
        first_node_id = path[0]
        last1_node_id = path[-1]
        last2_node_id = path[len(path)-2]

        #Find Store&Load Instr
        find_st = False
        for node in bb_node_list:
            node_id = int(node[0])
            node_opcode = node[1]

            if first_node_id == node_id:
                if "store" in node_opcode:
                    find_st = True
                    #print(node_opcode)
                    st_root_index = index
                    num_stores += 1

            if first_node_id == node_id:
                if "load" in node_opcode:
                    #print(node_opcode)
                    ld_root_index = index
                    num_root_loads += 1

            if last1_node_id == node_id or last2_node_id == node_id:
                if "load" in node_opcode:
                    #print(node_opcode)
                    ld_leaf_index = index
                    num_leaf_loads += 1

            if num_stores > 0 and st_root_index == index:
                if not path in st_root_paths:
                    st_root_paths.append(path)

            if num_root_loads > 0 and ld_root_index == index:
                if not path in ld_root_paths:
                    ld_root_paths.append(path)

            if num_leaf_loads > 0 and ld_leaf_index == index:
                if not path in ld_leaf_paths:
                    ld_leaf_paths.append(path)

                    ld_leaf_path = ld_leaf_paths.copy()

                    find_root = False
                    if find_st:
                        stld_paths.append(path)
                    else:
                        #print("enter into {} from {} for Node-{}".format(ld_leaf_path, path, node_id))
                        path_, index_  = RootFinder(ld_leaf_path, path, node_id)
                        
                        if len(path_) > 0:
                            tmp_path = path_
                            #print("found:{}".format(tmp_path))
                            path_ = tmp_path+path[index_:]
                            find_root = True
                            #print(path_)

                    #print(path_)
                    if find_root:
                        stld_paths.append(path_)

    with open(w_file_path+w_file_name+"_bpath_st_root.txt", "w") as st_bpath:
        st_bpath.writelines(map(str, st_root_paths))

    with open(w_file_path+w_file_name+"_bpath_st_ld.txt", "w") as st_ld_bpath:
        st_ld_bpath.writelines(map(str, stld_paths))

    with open(w_file_path+w_file_name+"_bpath_ld_leaf.txt", "w") as ld_bpath:
        ld_bpath.writelines(map(str, ld_leaf_paths))