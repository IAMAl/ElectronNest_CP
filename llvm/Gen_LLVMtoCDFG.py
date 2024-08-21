import utils.InstrTypeChecker
import llvm.utils.ProgFile
import utils.ProgConstructor
import utils.GraphUtils
import utils.IRPaser


def remove_duplicate_edges( num_dup, start_no, lines ):
    """
    Remove Dupplicate (Same) Edges
    """
    if lines is not None:
        for index_no in range(start_no, len(lines)-num_dup, 1):
            lines[index_no] = lines[index_no+1]

        for index_no in range(len(lines)-num_dup, len(lines), 1):
            lines[index_no] = ""

    return lines


def dupl_remover_dfg( w_file_path, prog ):
    """
    Remove Duplicate
    """
    # Duplicate Remover
    # Directory path maintains LLVM-IR file
    openfile = w_file_path +"/"+ prog.name+"_dfg_o.dot"
    dot_file_name = prog.name

    present_lines = []
    lines = []
    num_dup = 0

    with open(openfile, "r") as dot_file:
        for present_line in dot_file:
            present_lines.append(present_line)

    # Seek Same Line with Scan-Line Method
    for present_no in range(len(present_lines)):
        present_line = present_lines[present_no]
        for compare_no, compare_line in enumerate(present_lines[present_no:len(present_lines)-num_dup]):
            if compare_no == 0:
                lines.append(present_line)

            elif compare_line == present_line and compare_no > 0:
                num_dup += 1
                start_no = present_no+compare_no
                present_lines = remove_duplicate_edges(num_dup, start_no, present_lines)

    print("Total {} lines removed.".format(num_dup))

    #Write after removing
    #post-fix:  "_dfg_r"
    dot_file_r_name = w_file_path+"/"+dot_file_name+"_dfg_r.dot"
    with open(dot_file_r_name, "w") as dot_file:
        dot_file.writelines(lines)


def line_reorder( prog, w_file_path, dot_file_name ):
    openfile = w_file_path+"/"+ prog.name+"_dfg_r.dot"
    lines = []
    with open(openfile, "r") as dot_file:
        for present_line in dot_file:
            lines.append(present_line)
            
    #remove_duplicate_edges(num_dup, start_no, lines)

    dot_file_r_name = w_file_path+"/"+dot_file_name+"_dfg.dot"
    with open(dot_file_r_name, "w") as dot_file:
        dot_file.write(lines[0])
        dot_file.write(lines[1])
        dot_file.write(lines[2])

        for line_no in range(len(lines)-2, 3, -1):
            dot_file.write(lines[line_no-1])

        dot_file.write("}")


def Main_Gen_LLVMtoDFG( r_file_path, r_file_name, w_file_path ):
    prog = ProgReader( r_file_path, r_file_name )

    # Create Objects constructing
    #   hierarchical instructin structure
    # Setting Initial State
    ptr, \
    total_num_funcs, \
    total_num_blocks, \
    total_num_instrs, \
    instr = InitInstr(prog)

    Next_State = "next_seq_src2"

    with open(w_file_path+"/"+prog.name + "_dfg_o.dot", "w") as out:
        # Graph Utilities
        g = GraphUtils(out, total_num_instrs)

        # Graph Header Description
        g.start_df_graph()

        # Utilities
        r = RegInstr(prog=prog, ptr=ptr)

        # Processing Body
        while "term" != Next_State:

            # Sequence for Source-2 (Right)
            if "next_seq_src2" == Next_State:
                Next_State = DataFlowExploreOriginal(operand="src2", r=r, g=g)

            # Sequence for Source-1 (Left)
            if "next_seq_src1" == Next_State:
                Next_State = DataFlowExploreOriginal(operand="src1", r=r, g=g)

            # Check Termination
            if "next_check_term" == Next_State:
                Next_State = r.CheckTerm()

            # Move Next Instruction
            if "next_reg_dst" == Next_State:
                Next_State = r.NextInstr(r=r)

        # Write Edges
        for edge in g.edges:
            g.write(edge)

        g.write("}")

    # Reform Graph
    dot_file_name = prog.name + "_dfg.dot"

    dupl_remover_dfg(w_file_path)
    line_reorder( prog, w_file_path, dot_file_name )


def cfg_extractor( prog=prog, out=None, r_file_path, r_file_name ):
    """
    Control Graph Extractor
    """
    openfile = r_file_path + "/" + r_file_name+".ll"
    with open(openfile, "r") as llvm_ir:
        """
        LLVM-IR file-open, and parsing the IR file
        """
        print("File: {} parsed.".format(r_file_name))

        # Fetch Basic Block Label
        for bb_f_indx in range(prog.num_funcs):
            #print(prog.funcs[bb_f_indx].num_bblocks)
            # Fetch Target BBlock
            for bb_b_indx in range(prog.funcs[bb_f_indx].num_bblocks):
                bb_i_indx = prog.funcs[bb_f_indx].bblocks[bb_b_indx].num_instrs - 1
                target_nemonic = prog.funcs[bb_f_indx].bblocks[bb_b_indx].name
                br_t = prog.funcs[bb_f_indx].bblocks[bb_b_indx].instrs[bb_i_indx].br_t
                br_f = prog.funcs[bb_f_indx].bblocks[bb_b_indx].instrs[bb_i_indx].br_f

                # Fetch Destination Node of BBlock
                for f_indx in range(prog.num_funcs):
                    for b_indx in range(prog.funcs[f_indx].num_bblocks):
                        if b_indx != bb_b_indx:
                            if DEBUG:
                                print(prog.funcs[f_indx].bblocks[b_indx].name)

                            # Assign Node label
                            if prog.funcs[f_indx].bblocks[b_indx].name is not None:
                                if "entry" in prog.funcs[f_indx].bblocks[b_indx].name:
                                    b_label = "entry"
                                else:
                                    b_label = "label:<"+prog.funcs[f_indx].bblocks[b_indx].name+">"
                            else:
                                break

                            # Fetch BBlock Name
                            b_nemonic = prog.funcs[f_indx].bblocks[b_indx].name

                            # Fetch Number of Instrs in the BBlock
                            num_instrs = prog.funcs[f_indx].bblocks[b_indx].num_instrs
                            instr = prog.funcs[f_indx].bblocks[b_indx].instrs[num_instrs - 1]
                            fro = target_nemonic
                            to = b_nemonic
                            if DEBUG:
                                print("L: {}  T[{}]  F[{}]".format(b_label, br_t, br_f))

                            if br_t is not None and b_label == br_t:
                                if DEBUG:
                                    print("T-Matched:{}".format(br_t))
                                if fro == "entry":
                                    attrib = "[color=black dir=black]"
                                elif br_t == br_f:
                                    attrib = "[color=red dir=black]"
                                else:
                                    attrib = "[color=blue dir=black]"
                                out.write("\"%s\" -> \"%s\"%s\n" % (fro, to, attrib))

                            if br_f is not None and b_label == br_f and br_t != br_f:
                                if DEBUG:
                                    print("F-Matched:{}".format(br_f))
                                attrib = "[color=green dir=black]"
                                out.write("\"%s\" -> \"%s\"%s\n" % (fro, to, attrib))

                num_instrs = prog.funcs[bb_f_indx].bblocks[bb_b_indx].num_instrs
                instr = prog.funcs[bb_f_indx].bblocks[bb_b_indx].instrs[num_instrs - 1]
                b_nemonic = prog.funcs[bb_f_indx].bblocks[bb_b_indx].name
                to = b_nemonic
                if instr.opcode == "ret" and bb_f_indx == (prog.num_funcs-1) and bb_b_indx == (prog.funcs[bb_f_indx].num_bblocks-1):
                    attrib = "[color=black dir=black]"
                    out.write("\"%s\" -> \"%s\"%s\n" % (to, "ret", attrib))

        out.write("}")


def dupl_remover_cfg( w_file_path, prog ):
    dot_file_name = prog.name+"_cfg.dot"
    openfile = w_file_path + dot_file_name

    present_lines = []
    lines = []
    num_dup = 0

    with open(openfile, "r") as dot_file:
        for present_line in dot_file:
            present_lines.append(present_line)

    # Seek Same Line with Scan-Line Method
    for present_no, present_line in enumerate(present_lines):
        for compare_no, compare_line in enumerate(present_lines):
            if compare_no == 0:
                lines.append(present_line)
            elif compare_line == present_line and compare_no != present_no:
                #print("duplicated.")
                num_dup += 1
                start_no = present_no+compare_no
                for index_no in range(start_no, len(present_lines)-1, 1):
                    present_lines[index_no] = present_lines[index_no+1]

                present_lines[len(present_lines)-1] = ""

    print("Total {} lines removed.".format(num_dup))

    dot_file_name =w_file_path+ "/"+prog.name+"_cfg_r.dot"
    with open(dot_file_name, "w") as dot_file:
        for line_no in range(len(present_lines)):
            dot_file.write(present_lines[line_no])


def Main_Gen_LLVMtoCFG( r_file_path, r_file_name, w_file_path ):

    prog = ProgReader(r_file_path, r_file_name)
    ptr, \
    total_num_funcs, \
    total_num_blocks, \
    total_num_instrs, \
    instr = InitInstr(prog)

    with open(w_file_path+"/"+prog.name + "_cfg.dot", "w") as out:
        # Graph Utilities
        g_cfg = GraphUtils(out, total_num_instrs)

        # Graph Header Description
        g_cfg.start_cf_graph()
        cfg_extractor(prog=prog, out=out, r_file_path=r_file_path, r_file_name=r_file_name)
    
    # Reform Graph
    dupl_remover_cfg(w_file_path, prog)
