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

def CycleDetector( am_size=0, am=[], nodes=[], edgetab=[] ):

    read_no = 1
    write_no = 0
    CyclicEdges = []
    for steps in range(am_size):
        #print("\nStep-{}".format(steps))
        #print("Read from Table-{}".format(read_no))
        for node_id in range(am_size):
            #edgetab.Dump(node_id)
            #print("  Enter Node-{}".format(node_id), end="")
            if not nodes[node_id].Check_Term() or steps == 0:

                edges = edgetab.Read(read_no, node_id)

                cycles, edges, check_index, _, last_level, level = graphutils.CheckCycle([], node_id, edges, True, False, 0)
                if len(cycles) > 0 and not nodes[node_id].Check_Detect():
                    CyclicEdges.append(cycles[0])
                    nodes[node_id].Set_Detect()
                    #print("    CYCLE Detected: {}".format(cycles), end="")

                edges, check_index = graphutils.CheckEcho(node_id, edges)

                edges = graphutils.RemoveList(edges)

                if graphutils.CheckEmpty(node_id, edges) and steps != 0:
                    #print("  Node-{} Terminated: {}".format(node_id, edges))
                    nodes[node_id].Set_Term()

                dest_ids = nodes[node_id].Read_DestIDs()
                #print("  Send from Node-{} to Dest Nedes:{}".format(node_id, dest_ids), end="")
                edgetab.Write(write_no, node_id, dest_ids, edges)

            #print("\n")

        tmp_no = read_no
        read_no = write_no
        write_no = tmp_no

    return CyclicEdges


def RemoveCycles(CyclicEdges):
    CyclicEdges_ = []
    index = 0
    offset = 0
    length = len(CyclicEdges)
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
                        #print("Check {} and {}".format(check_cycle, cycle))
                        if check_cycle == cycle:
                            CyclicEdges_.append(cycle)
                            CyclicEdges.pop(idx-offset)
                            offset += 1
                            #print("idx:{} offset:{} for {}".format(idx, offset, cycle))
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