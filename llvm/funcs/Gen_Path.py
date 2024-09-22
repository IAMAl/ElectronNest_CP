##################################################################
##
##	ElectronNest_CP
##	Copyright (C) 2024  Shigeyuki TAKANO
##
##  GNU AFFERO GENERAL PUBLIC LICENSE
##	version 3.0
##
##################################################################
import numpy as np


class Path:
    def __init__( self ):
        self.st_route_path = []
        self.st_ld_path = []
        self.st_leaf_path = []
        self.ld_ld_path = []
        self.ld_leaf_path = []

        self.Branch_St = []
        self.Branch_Ld = []

        self.StPath = []
        self.LdPath = []

        self.Branch = []

    def Register( self, path_select, path ):
        if path_select == 'st_route_path':
            self.st_route_path.append( path )

        elif path_select == 'st_ld_path':
            self.st_ld_path.append( path )

        elif path_select == 'st_leaf_path':
            self.st_leaf_path.append( path )

        elif path_select == 'ld_ld_path':
            self.ld_ld_path.append( path )

        elif path_select == 'ld_leaf_path':
            self.ld_leaf_path.append( path )

    def Get( self, path_select ):
        if path_select == 'st_route_path':
            return self.st_route_path

        elif path_select == 'st_ld_path':
            return self.st_ld_path

        elif path_select == 'st_leaf_path':
            return self.st_leaf_path

        elif path_select == 'ld_ld_path':
            return self.ld_ld_path

        elif path_select == 'ld_leaf_path':
            return self.ld_leaf_path

    def Set_BranchStNode( self, index ):
        self.Branch_St.append( index )

    def Set_BranchLdNode( self, index ):
        self.Branch_Ld.append( index )

    def Set_StPath( self, index ):
        self.StPath.append( index )

    def Set_LdPath( self, index ):
        self.LdPath.append( index )

    def Push( self, index ):
        self.Branch.append( index )

    def Pop( self ):
        return self.Branch.pop( -1 )

    def StPush( self, index ):
        self.Branch_St.append( index )

    def LdPush( self, index ):
        self.Branch_Ld.append( index )

    def StPop( self ):
        return self.Branch_St.pop( -1 )

    def LdPop( self ):
        return self.Branch_Ld.pop( -1 )


def is_StNode( mnemonic ):
    return 'store' in mnemonic[1]


def is_LdNode( mnemonic ):
    return 'load' in mnemonic[1]


def is_LeafNode( mnemonic, index ):
    return 'LEAF' in mnemonic[2]


def GetNeighborNodea( row ):
    NNodes = []
    for index, elm in enumerate( row ):
        if elm == 1:
            NNodes.append( index )
    return NNodes


def GetMnemonic( NodeList, index ):
    return NodeList[ index ]


def SetExplored( em, src_idx, dst_idx):
    if dst_idx != src_idx:
        em[ src_idx ][ dst_idx ] = 1
        em[ dst_idx ][ src_idx ] = 1
    return em


def GetNonExploredNodes( am, em ):
    cm = am ^ em

    NodeList = []
    for idx, row in enumerate(cm):
        if 1 in row:
            NodeList.append(idx)
    return NodeList


def Explore_Path( am, NodeList, path ):

    TotalNumNodes = len( am[0] )
    PtrList = np.zeros( TotalNumNodes, dtype=int )
    em = np.zeros((TotalNumNodes, TotalNumNodes), dtype=int)

    index = 0

    CountNodes = 0

    StPath = []
    st_ld_path = []
    st_route_path = []
    st_leaf_path = []

    LdPath = []
    ld_ld_path = []
    ld_leaf_path = []

    start_st = False
    start_ld = False

    Branch = []
    BR_Popped = False

    popped = False
    Discon = False

    while CountNodes < TotalNumNodes and not Discon:
        if CountNodes > 0 and len(nlist) == 0:
            Discon = True

        # Fetch one row
        row = am[ index ]

        # Fetch Neighbot Nodes
        NNodes = GetNeighborNodea( row )

        # Fetch Mnemonic
        mnemonic = GetMnemonic( NodeList, index )

        print(f"NNodes:{NNodes}  mnemonic:{mnemonic}")
        
        br = False

        if not is_LeafNode( mnemonic, index ):
            print(f"This is NOT LEAF Node: {Branch}")
            if len(NNodes) > 2:
                print(f"This is Branch Noode:{NNodes[1:]}")
                br = True

            # Register  arriving the branch node
            if len(NNodes) >= 2 and index not in Branch:
                Branch.append( index )
                print(f"Branch: {Branch}")

            if not  popped:
                CountNodes += 1
            
            popped = False
            tmp_index = index
            

            if is_StNode( mnemonic ) and not start_st:
                # Node is first store instruction
                start_st = True
                path.StPush( index )

                # Register Path Node
                st_ld_path.append( index )
                st_route_path.append( index )
                st_leaf_path.append( index )

            elif is_StNode( mnemonic ) and start_st:
                # Node is store instruction
                #   support multiple store instructions in a basic block
                start_st = True
                path.StPush( index )

                # Register Path Node
                st_ld_path.append( index )
                st_route_path.append( index )
                st_leaf_path.append( index )

            elif is_LdNode( mnemonic ) and not start_ld:
                # Node is first load instruction
                start_ld = True
                path.LdPush( index )

                # Register Path Node
                if start_st:
                    st_route_path.append( index )
                    st_leaf_path.append( index )
                    st_ld_path.append( index)
                    print(f"st_route_path: {st_route_path}")
                    print(f"st_leaf_path: {st_leaf_path}")
                    print(f"st_ld_path: {st_ld_path}")
                    path.Register( 'st_ld_path', st_ld_path )
                    st_ld_path = []

                # Register Path Node
                ld_ld_path.append( index )
                ld_leaf_path.append( index )
                print(f"ld_ld_path: {ld_ld_path}")
                print(f"ld_leaf_path: {ld_leaf_path}")

            elif is_LdNode( mnemonic ) and start_ld:
                # Node is second load instruction
                start_ld = False
                path.LdPush( index )

                if start_st:
                    StPath.append( index )
                    st_ld_path.append( index )
                    st_route_path.append( index )
                    st_leaf_path.append( index )
                    print(f"st_ld_path: {st_ld_path}")
                    print(f"st_route_path: {st_route_path}")
                    print(f"st_leaf_path: {st_leaf_path}")
                    st_ld_path = []

                # Register Path Node
                ld_ld_path.append( index )
                ld_leaf_path.append( index )
                path.Register( 'ld_ld_path', ld_ld_path )
                print(f"ld_ld_path: {ld_ld_path}")
                ld_ld_path = []

            else:
                
                if start_st:
                    StPath.append( index )
                    st_ld_path.append( index )
                    st_route_path.append( index )
                    st_leaf_path.append( index )

                if start_ld:
                    LdPath.append( index )
                    ld_ld_path.append( index )
                    ld_leaf_path.append( index )

            past_index = tmp_index
            tmp_index = index
            if PtrList[ index ] > len( NNodes ):
                index = Branch.pop(-1)
                print("Branch Popped")
                popped = True
            elif PtrList[ index ]  >= 2:
                index = nlist.pop(0)
                print(f"next node={index}")
            elif br:
                print(f"NNodes: {NNodes}, PtrList[ index ]+1:{PtrList[ index ]+1}, index:{index}")
                index = NNodes[ PtrList[ index ] + 1 ]
                print(f"index={index}")      
            else:
                print(f"NNodes: {NNodes}, PtrList[ index ]:{PtrList[ index ]}, index:{index}")
                if 'store' in mnemonic[1] or 'load' in mnemonic[1] and len(NNodes) > 2:
                    index = NNodes[ PtrList[ index ] ]
                elif len(NNodes) > 1 and (PtrList[ index ]+1) < len(NNodes):
                    index = NNodes[ PtrList[ index ]  + 1 ]
                else:
                    index = NNodes[ PtrList[ index ] ]
                
                print(f"index={index}")

            PtrList[ tmp_index ] += 1

            # Set explored node
            print(f"tmp_index:{tmp_index}, index:{index}")
            em = SetExplored( em, tmp_index, index)

        elif is_LeafNode( mnemonic, index ):
            
            popped = False

            print("This is LEAF Node")
            PtrList[ index ] += 1
            CountNodes += 0

            tmp_index = index
            if start_st:
                StPath.append( index )
                st_ld_path.append( index )
                st_route_path.append( index )
                st_leaf_path.append( index )
                path.Register( 'st_ld_path', st_ld_path )
                path.Register( 'st_route_path', st_route_path )
                path.Register( 'st_leaf_path', st_leaf_path )
                print(f"st_route_path: {st_route_path}")
                print(f"st_leaf_path: {st_leaf_path}")
                st_ld_path = []
                st_route_path = []
                st_leaf_path = []

            if start_ld:
                LdPath.append( index )
                ld_ld_path.append( index )
                ld_leaf_path.append( index )
                path.Register( 'ld_leaf_path', ld_leaf_path )
                print(f"ld_leaf_path: {ld_leaf_path}")
                ld_ld_path = []
                ld_leaf_path = []
                start_ld = False

            # Set explored node
            path.Push( index )
            index = Branch.pop(-1)
            print("Branch Popped")
            em = SetExplored( em, tmp_index, index)
            popped = True


        # Check Remained Node
        #   exit when there is not remained
        nlist = GetNonExploredNodes( am, em )
        print(f"  nlist:{nlist}")
        if popped:
            popped = False
            
            # go to another graph when popped
            tmp_CountNodes = CountNodes
            #CountNodes -= len(nlist)
            #CountNodes -= 1
            if len(nlist) > 0:
                index = nlist.pop(0)
                print(f"  next root node-{index}")
            else:
                # otherwise continues
                CountNodes = tmp_CountNodes

            # Initialize
            if start_st:
                st_ld_path = []
                st_route_path = []
                st_leaf_path = []
            if start_ld:
                ld_ld_path = []
                ld_leaf_path = []
            start_st = False
            start_ld = False

        print(em)
        print(f"CountNodes = {CountNodes}/{TotalNumNodes}")

    return path


def Gen_Path( am, NodeList, w_path, w_name ):
    path = Path()
    path_ = Explore_Path( am, NodeList, path )

    w_path_name = w_path+'/'+w_name+"_bpath_st_root.txt"
    with open(w_path_name, "w") as st_bpath:
        st_bpath.writelines(map(str, path_.Get( 'st_route_path' )))

    w_path_name = w_path+'/'+w_name+"_bpath_st_leaf.txt"
    with open(w_path_name, "w") as st_bpath:
        st_bpath.writelines(map(str, path_.Get( 'st_leaf_path' )))

    w_path_name = w_path+'/'+w_name+"_bpath_st_ld.txt"
    with open(w_path_name, "w") as st_bpath:
        st_bpath.writelines(map(str, path_.Get( 'st_ld_path' )))

    w_path_name = w_path+'/'+w_name+"_bpath_ld_ld.txt"
    with open(w_path_name, "w") as st_bpath:
        st_bpath.writelines(map(str, path_.Get( 'ld_ld_path' )))

    w_path_name = w_path+'/'+w_name+"_bpath_ld_leaf.txt"
    with open(w_path_name, "w") as st_bpath:
        st_bpath.writelines(map(str, path_.Get( 'ld_leaf_path' )))