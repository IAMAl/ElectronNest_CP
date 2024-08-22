import copy

class instruction:
    opcode = None       #Opcode Name                String
    dst = None          #Destination Name           String
    d_type = None       #Destination Data-Type      String
    operands = []       #Source Name                String
    func = None         #Function Name              String
    br_t = None         #Lavel for Branch Taken     Bool
    br_f = None         #Lavel for Branch Not Taken Bool
    imm = None          #Immediate Value            String
    nemonic = None      #Nemonic (Assembly Code)    String
    discovered = False  #Tracking Record            Bool


class basicblock():
    """
    Basic Block Extractor
    name = None         Basic Block Name            String
    instrs = []         Set of Instructions         instruction class
    num_instrs = 0      A Number of Instructions    Int
    """
    def __init__(self):
        self.name = None
        self.instrs = []
        self.num_instrs = 0

    def clear(self):
        self.name = None
        self.instrs.clear()
        self.num_instrs = 0

    def append(self, instr=instruction):
        self.instrs.append(copy.deepcopy(instr))
        self.num_instrs += 1

    def set_name(self, b_name):
        self.name = b_name


class function():
    """
    Function Extractor
    name = name         Function Name               String
    bblocks = []        Set of Basic Blocks         basicblock class
    num_bblocks = 0     A Number of Basic Blocks    Int
    """
    def __init__(self):
        self.name = None
        self.bblocks = []
        self.num_bblocks = 0

    def clear(self):
        self.name = None
        self.bblocks.clear()
        self.num_bblocks = 0

    def append(self, bblock):
        self.bblocks.append(copy.deepcopy(bblock))
        self.num_bblocks += 1

    def set_name(self, f_name):
        self.name = f_name


class program():
    """
    Program Extractor
    name = name         Program Name                String
    funcs = []          Set of Functioins           function class
    num_funcs = 0       A Number of Functions       Int
    """
    def __init__(self):
        self.name = None
        self.funcs = []
        self.num_funcs = 0

    def clear(self):
        self.name = None
        self.funcs.clear()
        self.num_funcs = 0

    def append(self, func):
        self.funcs.append(copy.deepcopy(func))
        self.num_funcs += 1

    def set_name(self, p_name):
        self.name = p_name


def InitInstr( prog ):
    """
    Initialize Graph Constructor
    """
    # Pointer Extraction
    f_ptr = prog.num_funcs - 1
    if (f_ptr < 0):
        f_ptr = 0
    b_ptr = prog.funcs[f_ptr].num_bblocks - 1

    if (b_ptr < 0):
        b_ptr = 0
    i_ptr = prog.funcs[f_ptr].bblocks[b_ptr].num_instrs - 1

    if (i_ptr < 0):
        i_ptr = 0
    ptr = {"f_ptr":f_ptr, "b_ptr":b_ptr, "i_ptr":i_ptr}
    instr = prog.funcs[f_ptr].bblocks[b_ptr].instrs[i_ptr]

    # Instruction Adjacency Matrix Size Extraction
    total_num_instrs = 0
    total_num_bblocks = 0
    for func in prog.funcs:
        total_num_bblocks += func.num_bblocks
        for bblock in func.bblocks:
            total_num_instrs += bblock.num_instrs

    return ptr, prog.num_funcs, total_num_bblocks, total_num_instrs, instr