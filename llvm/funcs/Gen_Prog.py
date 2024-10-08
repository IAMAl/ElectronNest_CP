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
import utils.FileUtils as fileutils


def ReadIndex( DFG_Paths, DFG_Path, DFG_Node_List, Operands ):
    """
    Read Indeces of Store and Load IR Instructions
    - Begining Element in Data-Flow Path is Store Node of Data-Flow Path
    - End Element in Data-Flow Path is Load Node of Data-Flow Path
    """
    # Read Indeces' ID to Access Node List
    if isinstance(DFG_Path, list) and len(DFG_Path) > 0:
        #print("    DFG-Path: {}".format(DFG_Path))

        cnt_st = 0
        st_index = []
        for st_node in DFG_Path:
            st_node_id = int(st_node)
            St_Node = DFG_Node_List[st_node_id][0]
            #print("  Store Node-{} ({})".format(st_node_id, St_Node))

            if "store" in St_Node:
                St_Node = St_Node.split(" ")
                st_index1 = St_Node[2]
                if not "%" in st_index1:
                    st_index1 = -1
                    st_index.append(st_index1)
                else:
                    st_index.append(int(st_index1[1:]))

                if len(St_Node) > 3:
                    st_index2 = St_Node[3]
                    if not "%" in st_index2:
                        st_index2 = -1
                        st_index.append(st_index2)
                    else:
                        st_index.append(int(st_index2[1:]))

                cnt_st += 1

        if cnt_st == 0:
            Header_ID = DFG_Path[0]
            chk_opcode = DFG_Node_List[ Header_ID ]
            for Operand in Operands:
                opcode = Operand[0]
                dst = Operand[1]
                if opcode in chk_opcode:
                    break

            while len(dst) > 1:
                for dfg_path in DFG_Paths:
                    if Header_ID in dfg_path:
                        header_index = dfg_path.index( Header_ID ) - 1
                        src_indeces = DFG_Node_List[ header_index ][2:]

                        for src_index in src_indeces:
                            if src_index in dst:
                                dst_index = dst.index( src_index )
                                dst.pop( dst_index )

            if (dst) == 1:
                st_index = [dst[0][1:]]
            else:
                st_index = [-1]


        cnt_ld = 0
        ld_index = []
        for no in range(len(DFG_Path)-1, -1, -1):
            ld_node_id = int(DFG_Path[no])

            Ld_Node = DFG_Node_List[ld_node_id][0]
            #print("  Load Node-{} ({})".format(ld_node_id, Ld_Node))

            if "load" in Ld_Node:
                Ld_Node = Ld_Node.split(" ")
                ld_index1 = Ld_Node[2]
                if not "%" in ld_index1:
                    ld_index1 = -1
                    ld_index.append(ld_index1)
                else:
                    ld_index.append(int(ld_index1[1:]))

                if len(Ld_Node) > 3:
                    ld_index2 = Ld_Node[3]
                    if not "%" in ld_index2:
                        ld_index2 = -1
                        ld_index.append(ld_index2)
                    else:
                        ld_index.append(int(ld_index2[1:]))

                cnt_ld += 1

        if cnt_ld == 0:
            ld_index = [-1]


        # Find DFG-Node
        return st_index, ld_index
    else:
        return [-1], [-1]


def Preprocess( r_file_path, r_file_name, CyclicPaths ):
    """
    Preprocessor

    Role:
        Construct Control-Flow Graph
    """
    print("START PREPROCESS")

    CFGNodes = []
    for cycle_path in CyclicPaths:

        label_A = False
        #print("Work in CFG Cyclic-Loop Path: {}".format(cycle_path))
        Nodes = graphutils.Create_CFGNodes()

        ptr = 0
        for _ in range(len(cycle_path)):

            if label_A == False:
                # Get ID
                node_A_id = cycle_path[ptr]

                index = int(node_A_id)

                label_A = True

            if label_A == True:

                # Create Node
                node_A = graphutils.Create_CFGNode()

                # Set This Node's ID
                node_A.SetNodeID(node_A_id)

                # Set Explored Flag
                node_A.SetExplored()

                # Set Forward Linked Node
                if ptr < (len(cycle_path)-1):
                    node_A.SetNeighborNode(cycle_path[ptr+1])
                else:
                    node_A.SetNeighborNode(cycle_path[0])

                # Set Backward Linked Node
                if ptr > 0 and ptr < len(cycle_path):
                    node_A.SetNeighborNode(cycle_path[ptr-1])
                else:
                    node_A.SetNeighborNode(cycle_path[-1])

                # Register Node
                #print("  CFG Node-{} is created".format(node_A_id))
                Nodes.SetNode(node_A)

                ptr += 1


            # Read This Block's DFG Paths
            #print("  Read DFG for CFG Node-{}".format(node_A_id))
            DFG_paths, node_list = fileutils.ReadDFG(r_file_path=r_file_path, r_file_name=r_file_name, dfg_node_id=node_A_id)
            Operands = fileutils.ReadOperands( r_file_path=r_file_path, r_file_name=r_file_name, dfg_node_id=node_A_id )

            # Set Store-Load Path if available
            if isinstance(DFG_paths, list) and len(DFG_paths) > 0:
                for no, DFG_path in enumerate(DFG_paths):
                    #print("    Path-{}".format(no))
                    #print("      Set Path: {}".format(DFG_path))
                    Nodes.SetStLdPaths(node_A_id, DFG_path)

                    St_Index, Ld_Index = ReadIndex( DFG_paths=DFG_paths, DFG_Path=DFG_path, DFG_Node_List=node_list, Operands=Operands )

                    #print("      Set Indeces: Store{} Load{} for path{}".format(St_Index, Ld_Index, DFG_path))
                    Nodes.SetStLdIndex(node_id=node_A_id, st=1, index=St_Index)
                    Nodes.SetStLdIndex(node_id=node_A_id, st=0, index=Ld_Index)
            else:
                label_A = False


            # Check Neighbor Node Availabiliyty
            if node_A.ReadNumNodes() != 0 and label_A == True:

                # Get Neighbor Node's ID
                if ptr == len(cycle_path):
                    CFGNodes.append(Nodes)
                    break

                node_C_id = cycle_path[ptr]

                # Check Node-C is already Explored
                if Nodes.ReadExplored(node_C_id):

                    #Back to Previous CFG-Node
                    ptr -= 1
                    node_id = cycle_path[ptr]

                    # Check node_ is the "node-A"
                    if node_id == node_A.ReadNodeID():

                        # Read Remained Neighbor Node
                        remained_node = Nodes.ReadNeighborNode(node_id)

                        if isinstance(remained_node, int):
                            # remained_node == -1 then Exit
                            return Nodes
                        else:
                            node_A_id = remained_node.ReadNodeID()
                            #print("  Set Node-{} to Node-A".format(node_A_id))
                            label_A = True

                else:
                    #print("  Set New Node-{} to Node-A".format(node_C_id))
                    node_A_id = node_C_id
                    label_A = True

    return CFGNodes


def BranchNodeTracker(CFG_Nodes):
    """
    Finding Branch CFG-Node
    """
    BranchList = []
    for CycleNo, CFGNodes in enumerate(CFG_Nodes):

        for CFG_No in range(CFGNodes.ReadNumNodes()):

            CFGNode = CFGNodes.ReadCFGNode(CFG_No)
            CFGNode_ID = CFGNode.ReadNodeID()

            CFGNodeBranchList = []

            for Path_No in range(CFGNode.ReadNumPaths()):

                Path = CFGNode.ReadStLdPath(Path_No)

                for Chk_CycleNo in range(CycleNo+1, len(CFG_Nodes), 1):

                    Chk_CFGNode = CFG_Nodes.ReadCFGNode(Chk_CycleNo)
                    Chk_CFGNode_ID = Chk_CFGNode.ReadNodeID()

                    for Chk_Path_No in range(Chk_CFGNode.ReadNumPaths()):

                        Chk_Path = Chk_CFGNode.ReadStLdPath(Chk_Path_No)

                        for DFG_Node_ID in Path:
                            for Chk_DFG_Node_ID in Chk_Path:
                                if Chk_DFG_Node_ID == DFG_Node_ID:
                                    CFGNodeBranchList.append([CFGNode_ID, Path_No, DFG_Node_ID], [Chk_CFGNode_ID, Chk_Path_No, Chk_CFGNode_ID])

        BranchList.append([CycleNo, CFGNodeBranchList])

    return BranchList


def PathPicker(CycleNo, Node_Ptr, CFGNode_A, CFG_Nodes, Path, Ld, St):

    # Check Node Availability
    if isinstance(CFGNode_A, int):
        if Node_Ptr == 0:
            # There is NO Available Node
            return Path
        else:
            Node_Ptr -= 1

    for Path_No in range(CFGNode_A.ReadNumPaths()):

        Path_ = []

        Path_A = CFGNode_A.ReadStLdPath(Path_No)
        print(f"Path_A:{Path_A}  Ld:{Ld}  St:{St}")
        Indeces_A = Path_A[2]

        Ld_Indeces = Indeces_A[Ld][0]
        for Ld_Index in Ld_Indeces:
            print(f"Ld_Index={Ld_Index}")
            Tmp_Node_Ptr = Node_Ptr + 1

            if Ld_Index != -1:
                Cont = True
                while Cont:
                    print("Enter while")

                    CFGNode_B = CFG_Nodes[CycleNo].ReadNode(Tmp_Node_Ptr)
                    print(f"Tmp_Node_Ptr:{Tmp_Node_Ptr}, {CFGNode_B.ReadNumPaths()}")

                    for Path_B_No in range(CFGNode_B.ReadNumPaths()):

                        Path_B = CFGNode_B.ReadStLdPath(Path_B_No)
                        Indeces_B = Path_B[2]
                        print(f"Path_B:{Path_B}")

                        St_Indeces = Indeces_B[St][0]
                        for St_Index in St_Indeces:
                            if St_Index != -1 and St_Index == Ld_Index:
                                print(f"Check St_Index={St_Index} with Ld_Index={Ld_Index}, Path_B:{Path_B}")
                                Path_B = PathPicker(CycleNo, Tmp_Node_Ptr, CFGNode_B, CFG_Nodes, Path, Ld^1, St^1)
                                if Path_B != None:
                                    Path_A[0] = Path_A[0]+Path_B
                                Path_ = Path_A
                                print(f"Path_:{Path_}")

                    Tmp_Node_Ptr += 1
                    Cont = Tmp_Node_Ptr <= CFGNode_B.ReadNumNodes()

            if len(Path_) > 0:
                Path.append(Path_)

    return Path


def BackTrack(CFG_Nodes):

    CycleNo = 0
    Node_Ptr = 0
    CFGNodes = CFG_Nodes[0]
    Path = []

    Cont = True
    while Cont:
        Cont, CFGNode_A = CFGNodes.ReadInitNode()
        if CFGNode_A == -1:
            Cont = True
            CycleNo += 1
            Node_Ptr = 0
        else:
            print("Read Remained Node: {}".format(CFGNode_A.ReadNodeID()))
            Cont = False

        #if Cont:
        print(f">>>> PathPicker")
        path = PathPicker(CycleNo, Node_Ptr, CFGNode_A, CFG_Nodes, Path, 1, 0)
        Node_Ptr += 1
        Path.append(path)
        #print(f">>>> {Path}")

    return Path