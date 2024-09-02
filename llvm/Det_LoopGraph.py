##################################################################
##
##	ElectronNest_CP
##	Copyright (C) 2024  Shigeyuki TAKANO
##
##  GNU AFFERO GENERAL PUBLIC LICENSE
##	version 3.0
##
##################################################################

import utils.GraphUtils as graphutils


def RemoveCycles(CyclicEdges):
    CyclicEdges_ = []
    index = 0
    offset = 0
    length = len(CyclicEdges)
    prev_cycle = []
    if length > 1:
        while True:

            index += 1
            if (offset+index) == length:
                break

            cycle = CyclicEdges.pop(0)
            for idx in range(length-offset-index-1):
                check_cycle = CyclicEdges[idx-offset]

                if len(check_cycle) == len(cycle):
                    for count in range(len(cycle)):
                        print("Check {} and {}".format(check_cycle, cycle))
                        if check_cycle == cycle and prev_cycle != cycle:
                            prev_cycle = cycle
                            CyclicEdges_.append(cycle)
                            CyclicEdges.pop(idx-offset)
                            offset += 1
                            print("idx:{} offset:{} for {}".format(idx, offset, cycle))
                        else:
                            check_cycle = check_cycle[1:]+check_cycle[:1]

    return CyclicEdges_


def ReadNodeList(r_file_name):

    r_node_list_file_name = r_file_name+"_node_list.txt"
    node_list = []
    with open(r_node_list_file_name, "r") as list:
        for line in list:
            line_ = []
            line = line.split(" ")
            for item in line:
                item = item.replace('\n', '')
                line_.append(item)

            node_list.append(line_)

    return  node_list


def TranslateNode(r_file_name, CyclicEdges):

    node_list = ReadNodeList(r_file_name)

    CyclicEdges_ = []
    for cycle_path in CyclicEdges:
        path = []
        for node_no in cycle_path:
            for node in node_list:
                if node[0] in str(node_no):
                    print("Checked: {}({}) == {}".format(node[0], node[1], node_no))
                    node_id = node[1]
                    path.append(node_id)
                    break

            #print(path)

        CyclicEdges_.append(path)

    return CyclicEdges_


def Get_Neighbors( my_no, am_size, am, ng_id ):
    if my_no != ng_id or my_no == 0:
        row = am[my_no]
        nnodes = []
        for index in range(am_size):
            if row[index] == 1 and index != ng_id:
                nnodes.append(index)

        return nnodes
    else:
        return []

def is_Loop( ptr, addr, Paths ):
    Find = False
    NNodes = Paths[ptr][2][addr:]
    for check_node_id in NNodes:
        for index in range(len(Paths)-1):
            nnode_id = Paths[index][0]

            #print(f">>>> Check Node-{nnode_id}, index={index}")

            #print(f">>>>>> Check node-{check_node_id} with node-{nnode_id}")
            if check_node_id == nnode_id:
                return True, index

    return Find, 0


def RollBack(target_id, ptr, Paths):

    for check_ptr in range(ptr, -1,-1):
        check_id = Paths[check_ptr][0]
        check_addr = Paths[check_ptr][1]
        check_srcs = Paths[check_ptr][2]
        check_len = len(check_srcs)

        if target_id in check_srcs:
            print(f"    Found target node {target_id}: compare {len(check_srcs)} and {check_addr+1}")
            if len(check_srcs) <= (check_addr+1):
                print(f"    Already exlpored, go back more")
                target_id = check_id
                back_ptr = RollBack(target_id, check_ptr, Paths)
                back_node_id = Paths[back_ptr][0]
                print(f"    This node {back_node_id} is roll back node")
                return back_ptr
            else:
                back_node_id = Paths[check_ptr][0]
                print(f"    This node {back_node_id} is roll back node")
                return check_ptr

        # roll back more

    return ptr

def CycleDetector( am_size=0, am=[], nodes=[], edgetab=[] ):

    count = 0

    Loops = []
    Paths = []
    ptr = 0
    addr = 0
    nnode_id = 0
    Find = False
    index = 0
    stack = []

    # Get Neighbor Node's ID
    NNodes = Get_Neighbors( ptr, am_size, am, ptr )
    Paths.append([ptr, 0, NNodes])
    stack.append(ptr)

    while not is_Empty(Paths) and count < 50:

        print(f"Paths = {Paths}")
        print(f"  ptr = {ptr}, addr = {addr}, index = {index}")

        nnode_id = Paths[ptr][2][addr]
        print(f"  Check Neighbor Node-{nnode_id} for Node-{Paths[ptr][0]}")
        Find, index = is_Loop( ptr, addr, Paths )
        neighbor_id = Paths[index][0]

        if Find:
            print(f"  Cycle Detected from Node-{Paths[ptr][0]} to Neighbor Node-{neighbor_id}")

            Paths[ptr][1] += 1

            # Collecting Path Nodes
            reg_id = Paths[ptr][0]
            loop = []
            loop.append(nnode_id)
            loop.append(reg_id)
            print(f"  loop = {loop}, index = {index}")
            Loops.append(loop)

            # Update address
            tmp_addr = addr
            addr = 1 + Paths[index][1]
            Paths[index][1] = addr
            print(f"  addr: before[{tmp_addr}] after[{addr}]")

            tmp_ptr = ptr
            if (1 + Paths[index][1]) >= len(Paths[index][2]):
                index += 1
                addr = Paths[index][1]
                print(f"  go next from index={index-1} to index={index}, addr={addr}")
                if len(Paths[index][2]) <= addr:
                    target_id = Paths[index][2][len(Paths[index][2])-1]
                    check_ptr = RollBack(target_id, index, Paths)
                    print(f"    tmp_ptr={tmp_ptr} : check_ptr={check_ptr} and addr={Paths[check_ptr][1]}")
                    tmp_ptr = check_ptr

            prev_ptr = ptr
            ptr = tmp_ptr
            index = tmp_ptr
            addr = Paths[ptr][1]


        else:
            prev_ptr = ptr
            addr = 0
            # Get Neighbor Node's ID
            NNodes = Get_Neighbors( nnode_id, am_size, am, prev_ptr )
            if (len(NNodes) > 0 and [nnode_id, 0, NNodes] not in Paths) or len(Paths) == 1:
                Paths.append([nnode_id, 0, NNodes])
                ptr = len(Paths) - 1
                stack.append(ptr)
                #print(stack)


        count += 1

    print(Loops)
    return Loops