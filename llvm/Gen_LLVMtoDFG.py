import utils.InstrTypeChecker
import llvm.utils.ProgFile
import utils.ProgConstructor
import utils.GraphUtils
import utils.IRPaser


def DataFlowExploreOriginal( operand="src2", r=None, g=None ):
    """
    Common Processing task for Source-1 and -2
    """
    # Fetch Present Instr
    instr = r.ReadInstr(r.ReadPtr())
    instr_dst = instr.dst
    instr_src = FetchSrc(src=operand, instr=instr)

    # Find instruction having source operand as destination operand
    match = r.SearchSrc(src=instr_src)
    num_operands = len(instr.operands)


    # Draw Edge when destination addressed by current pointer is matched
    if match:
        # Push current pointer when forwarding source-2 path
        if "src2" == operand and not (is_None(instr.operands[0]) or is_Val(instr.operands[0])):
            r.PushPtr()

        # Marking when source-1 (means source-2 path is already discovered), or
        #   source-1 is terminal
        if "src1" == operand or ("src2" == operand and (is_None(instr.operands[0]) or is_Val(instr.operands[0]))):
            r.CheckInstr()
            g.Count()

        # Fetch hit-instruction
        next_instr = r.ReadInstr(r.ReadHitPtr())

        # Update current pointer to hit instruction position
        if len(next_instr.operands) > 0:
            r.SetPtr(r.ReadHitPtr())

        # Drawing the edge
        attrib = "[color=blue dir=back]"
        g.edge(instr.nemonic, next_instr.nemonic, extra=attrib)

        # Forward source-2 Path
        if len(next_instr.operands) == 2 and not is_Val(next_instr.operands[1]):
            # Discovering souce-2 path when source-2 is not value (terminal)
            return "next_seq_src2"
        elif len(next_instr.operands) == 2 and is_Val(next_instr.operands[1]):
            # Skip source-2 discovering when source-2 is value (terminal)
            return "next_seq_src1"
        elif len(next_instr.operands) == 1 and not is_Val(next_instr.operands[0]):
            # Discovering source-1 path
            return "next_seq_src1"
        elif r.DepthStack() > 0:
            # Reaches here if #of operands is less than two and
            #   source-1 is value (teminal)
            r.PopPtr(SrcNo="Src2")
            return "next_seq_src1"
        else:
            # Otherwise dicovering next instruction
            #   (all sources are a terminal)
            r.CheckInstr()
            return "next_reg_dst"
    else:
        # Mis-Match Cases
        # 2.  operand == "src1"
        #   2.1.  source-1 is value (True == is_Val())
        #       Next_State = next_reg_dst
        if 0 == num_operands:
            src1_is_Val = False
        else:
            src1_is_Val = is_Val(instr.operands[0])

        #   2.2.  source-1 is None (True == is_Nan())
        #       Next_State = next_reg_dst
        if 0 == num_operands:
            src1_is_None = True
        else:
            src1_is_None = is_None(instr.operands[0])

        #   2.3.  source-1 is a terminal node
        #       Pop stack and update current pointer
        #       Next_State = next_seq_src1
        src1_is_Term = src1_is_Val or src1_is_None

        # 3.  operand == "src2"
        #   3.1.  source-2 is value (True == is_Val())
        #       Next_State = next_seq_src1
        if 2 == num_operands:
            src2_is_Val = is_Val(instr.operands[1])
        else:
            src2_is_Val = False

        #   3.2.  source-2 is None (True == is_Nan())
        #       Next_State = next_seq_src1
        if 2 == num_operands:
            src2_is_None = is_None(instr.operands[1])
        else:
            src2_is_None = False

        #   3.3.  source-2 is a terminal node
        #       Next_State = next_seq_src1
        src2_is_Term = src2_is_Val or src2_is_None


        # 1.  instr is a sink node
        # No Source Operand
        if 0 == num_operands:
            src_is_Val = False
            if is_None(instr_dst):
                dst_is_Sink = True
                src_is_None = True
            elif "ret" == instr.opcode:
                dst_is_Sink = True
                src_is_None = True
            elif "call" == instr.opcode:
                dst_is_Sink = False
                src_is_None = True
            elif "br" == instr.opcode:
                r.CheckInstr()
                dst_is_Sink = True
                src_is_None = True
            elif "jmp" == instr.opcode:
                r.CheckInstr()
                dst_is_Sink = True
                src_is_None = True
            elif "alloca" == instr.opcode:
                dst_is_Sink = False
                src_is_None = True
            else:
                dst_is_Sink = False
                src_is_None = False

        # Single Source Operand
        elif 1 == num_operands:
            dst_is_Sink = not is_None(instr_dst)
            src_is_None = src1_is_None
            src_is_Val = src1_is_Val
            if dst_is_Sink and not src_is_None:
                r.CheckInstr()

        # Multiple Source Operands
        else:
            dst_is_Sink = is_None(instr_dst)
            src_is_None = src1_is_None and src2_is_None
            src_is_Val = src1_is_Val and src2_is_Val

        # Token on Dst Part is Sink
        is_Sink = dst_is_Sink

        if src_is_Val:
            # Source is Immediate Value
            r.SetPrevInstr(instr=instr)
            return "next_reg_dst"
        elif src2_is_Term:
            # Source-2 is Terminal,
            #   so dicovers source-1 path
            return "next_seq_src1"
        elif src1_is_Term:
            # Source-1 is terminal,
            #   so pop-stack and discovers source-2 after
            #   checking a termination
            r.CheckInstr()
            r.PopPtr(SrcNo="Src1")
            return "next_check_term"
        elif is_Sink and (src_is_None or src_is_Val):
            # Forwarding to next instruction
            #   when instruction is sink node without sources
            r.SetPrevInstr(instr=instr)
            r.CheckInstr()
            return "next_reg_dst"
        elif "src2" == operand:
            # Second Source Exploration is done
            return "next_seq_src1"
        elif "src1" == operand:
            # Reaches here after source-2 path discovering,
            #   AND there is no node for source-1 ID.
            r.PopPtr(SrcNo="Src1")
            r.SearchDst()
            return "next_seq_src2"
        else:
            r.CheckInstr()
            r.SetPrevInstr(instr=instr)
            return "next_reg_dst"


def DataFlowExplore( operand="src2", r=None, g=None ):
    """
    Common Processing task for Source-1 and -2
    """
    # Fetch Present Instr
    instr = r.ReadInstr(r.ReadPtr())
    instr_dst = instr.dst
    instr_src = FetchSrc(src=operand, instr=instr)

    # Find instruction having source operand as destination operand
    match = r.SearchSrc(src=instr_src)
    num_operands = len(instr.operands)

    # Draw Edge when destination addressed by current pointer is matched
    if match:
        # Push current pointer when forwarding source-2 path
        if "src2" == operand and not (is_None(instr.operands[0]) or is_Val(instr.operands[0])):
            r.PushPtr()

        # Marking when source-1 (means source-2 path is already discovered), or
        #   source-1 is terminal
        if "src1" == operand or ("src2" == operand and (is_None(instr.operands[0]) or is_Val(instr.operands[0]))):
            r.CheckInstr()
            g.Count()

        # Fetch hit-instruction
        next_instr = r.ReadInstr(r.ReadHitPtr())

        # Update current pointer to hit instruction position
        if len(next_instr.operands) > 0:
            r.SetPtr(r.ReadHitPtr())

        # Drawing the edge
        attrib = "[color=blue dir=back]"
        g.edge(instr.nemonic, next_instr.nemonic, extra=attrib)

        # Forward source-2 Path
        if len(next_instr.operands) == 2 and not is_Val(next_instr.operands[1]):
            # Discovering souce-2 path when source-2 is not value (terminal)
            if DEBUG:
                print("    Go to Src-2")
            return "next_seq_src2"

        elif len(next_instr.operands) == 2 and is_Val(next_instr.operands[1]):
            # Skip source-2 discovering when source-2 is value (terminal)
            if DEBUG:
                print("    Go to Src-1")
            return "next_seq_src1"

        elif len(next_instr.operands) == 1 and not is_Val(next_instr.operands[0]):
            # Discovering source-1 path
            if DEBUG:
                print("    Go to Src-1")
            return "next_seq_src1"

        elif r.DepthStack() > 0:
            # Reaches here if #of operands is less than two and
            #   source-1 is value (teminal)
            r.PopPtr(SrcNo="Src2")
            if DEBUG:
                print("    Go to Src-1")
            return "next_seq_src1"

        else:
            # Otherwise dicovering next instruction
            #   (all sources are a terminal)
            r.CheckInstr()
            return "next_reg_dst"
    else:
        # Mis-Match Cases
        return "next_reg_dst"


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