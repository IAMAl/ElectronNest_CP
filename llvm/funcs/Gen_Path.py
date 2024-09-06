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

        if path_select == 'st_leaf_path':
            self.st_leaf_path.append( path )

        if path_select == 'ld_ld_path':
            self.st_ld_path.append( path )

        if path_select == 'ld_leaf_path':
            self.st_leaf_path.append( path )
    
    def Get( self, path_select ):
        if path_select == 'st_route_path':
            return self.st_route_path

        elif path_select == 'st_ld_path':
            return self.st_ld_path

        if path_select == 'st_leaf_path':
            return self.st_leaf_path

        if path_select == 'ld_ld_path':
            return self.st_ld_path

        if path_select == 'ld_leaf_path':
            return self.st_leaf_path

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
    return 'st' in mnemonic


def is_LdNode( mnemonic ):
    return 'st' in mnemonic


def is_LeafNode( NodeList, index ):
    return 'LEAF' in NodeList[ index ]


def GetNeighborNodea( row ):
    NNodes = []
    for index, elm in enumerate( row ):
        if elm == 1:
            NNodes.append( index )
    return NNodes


def GetMnemonic( NodeList, index )
    return NodeList[ index ]


def Eplore_Path( am, NodeList, path ):

    TotalNumNodes = len( am[0] )
    PtrList = np.zeros( TotalNumNodes )

    index = 0

    CountNodes = 0

    Branch_St = []
    StPath = []
    st_ld_path = []
    st_route_path = []
    st_leaf_path = []

    Branch_Ld = []
    LdPath = []
    ld_ld_path = []
    ld_leaf_path = []

    start_st = False
    start_ld = False

    while CountNodes < TotalNumNodes:

        row = am[ index ]
        NNodes = GetNeighborNodea( row )
        mnemonic = GetMnemonic( NodeList, index )

        if is_StNode( mnemonic ) and not start_st:
            start_st = True
            path.StPush( index )
            Branch_St.append( index )
            st_ld_path.append( index )
            st_route_path.append( index )
            st_leaf_path.append( index )

            CountNodes += 1

            if PtrList[ index ] >= len( NNodes ):
                index = path.Pop()
            else:
                path.Push( index )
                tmp_index = index
                index = NNodes[ PtrList[ index ] ]
                PtrList[ tmp_index ] += 1

        elif is_StNode( mnemonic ) and start_st:
            start_st = False
            print(f"Error on Store path")
            break

        elif is_LdNode( mnemonic ) and not start_ld:
            start_ld = True
            path.LdPush( index )
            Branch_Ld.append( index )

            if start_st:
                run_start_st = True
                start_st = False
                st_ld_path.append( index)
                path.Register( 'st_ld__path', st_ld_path )
                st_ld_path = []

            else:
                ld_ld_path.append( index )
                ld_leaf_path.append( index )

            CountNodes += 1

            if PtrList[ index ] >= len( NNodes ):
                index = path.Pop()
            else:
                path.Push( index )
                tmp_index = index
                index = NNodes[ PtrList[ index ] ]
                PtrList[ tmp_index ] += 1

        elif is_LdNode( mnemonic ) and start_ld:
            start_ld = False
            ld_ld_path.append( index )
            ld_leaf_path.append( index )
            path.Register( 'ld_ls_path', ld_ld_path )
            ld_ld_path = []

            CountNodes += 1

            if PtrList[ index ] >= len( NNodes ):
                index = path.Pop()
            else:
                path.Push( index )
                tmp_index = index
                index = NNodes[ PtrList[ index ] ]
                PtrList[ tmp_index ] += 1

        elif not is_LeafNode( NodeList, index ):

            if start_st:
                StPath.append( index )
                st_ld_path.append( index )
                st_route_path.append( index )
                st_leaf_path.append( index )

            if start_ld:
                LdPath.append( index )
                ld_ld_path.append( index )
                ld_leaf_path.append( index )

            CountNodes += 1

            if PtrList[ index ] >= len( NNodes ):
                index = path.Pop()
            else:
                path.Push( index )
                tmp_index = index
                index = NNodes[ PtrList[ index ] ]
                PtrList[ tmp_index ] += 1

        elif is_LeafNode( NodeList, index ):

            if start_st:
                StPath.append( index )
                st_ld_path.append( index )
                st_route_path.append( index )
                st_leaf_path.append( index )
                path.Register( 'st_ld_path', st_ld_path )
                path.Register( 'st_route_path', st_route_path )
                path.Register( 'st_leaf_path', st_leaf_path )
                st_ld_path = []
                st_route_path = []
                st_leaf_path = []

            if start_ld:
                LdPath.append( index )
                ld_ld_path.append( index )
                ld_leaf_path.append( index )
                path.Register( 'ld_ld_path', ld_ld_path )
                path.Register( 'ld_leaf_path', ld_leaf_path )
                ld_ld_path = []
                ld_leaf_path = []

            CountNodes += 1

            if PtrList[ index ] >= len( NNodes ):
                index = path.Pop()
            else:
                path.Push( index )
                tmp_index = index
                index = NNodes[ PtrList[ index ] ]
                PtrList[ tmp_index ] += 1

    return path


def Gen_Path( am, NodeList, w_path, w_name ):
    path = Path()
    path_ = Eplore_Path( am, NodeList, path )
    
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