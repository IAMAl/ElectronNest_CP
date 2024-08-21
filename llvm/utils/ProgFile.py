import ProgConstructor

def ProgWriter( prog, w_file_path="./", w_file_name="" ):
    """
    Program File Read and Composition

    Arguments:
        w_file_path:        Writinging File Path
        w_file_name:        File Name

    Function:
        - Write parsed program to file
    """
    openfile = w_file_path + w_file_name+".txt"
    with open(openfile, "w") as prog_file:
        header = "program \""+prog.name+"\""
        prog_file.write(header)

        for func in prog.funcs:
            func_header = "begin function \""+func.name+"\""
            prog_file.write(func_header)

            for block in func.blocks:
                block_header = "begin bblock \""+block.name+"\""
                prog_file.write(block_header)

                for instr in block.instrs:
                    instruction = instr.opcode+" "+instr.dsta+" "+instr.d_type+" "+instr.operand+" "+instr.func.name+" "+instr.br_t+" "+instr.br_f+" "+instr.imm+" "+instr.nemonic
                    prog_file.write(instruction)

                prog_file.write("end bblock")

            prog_file.write("end function")


def ProgReader( r_file_path="./", r_file_name="" ):
    """
    Program File Read and Composition

    Arguments:
        r_file_path:        Reading File Path
        r_file_name:        File Name

    Function:
        - Read File of parsed program
        - Compose program() class
    """
    openfile = r_file_path + r_file_name+".txt"
    with open(openfile, "r") as prog_file:
        in_prog = False
        in_func = False
        in_bblock = False
        for line in prog_file:
            if "program" in line:
                prog = program()
                prog.name = line.split(" ")[1].replace('"', '')
                in_prog = True
            elif "begin function" in line:
                func = function()
                func.name = line.split(" ")[2].replace('"', '')
                in_func  = True
            elif "begin bblock" in line:
                bblock = basicblock()
                bblock.name = line.split(" ")[2].replace('"', '')
                in_bblock  = True
            elif "end bblock" in line:
                func.bblocks.append(bblock)
                in_bblock  = False
            elif "end function" in line:
                prog.funcs.append(func)
                in_func  = False
            elif in_prog and in_func and in_bblock:
                instr = instruction()
                line = line.split(" ")
                for index, item in enumerate(line):
                    item = item.replace(',', '')
                    item = item.replace('[', '')
                    item = item.replace(']', '')
                    item = item.replace('\'', '')
                    if index == 0:
                        instr.opcode = item         #Opcode Name                String
                    elif index == 1:
                        instr.dst = item            #Destination Name           String
                    elif index == 2:
                        instr.d_type = item         #Destination Data-Type      String
                    elif index == 3:
                        instr.operands.append(item) #Source Name                String
                    elif index == 4:
                        instr.operands.append(item) #Source Name
                    elif index == 5:
                        instr.func = item           #Function Name              String
                    elif index == 6:
                        instr.br_t = item           #Lavel for Branch Taken     Bool
                    elif index == 7:
                        instr.br_f = item           #Lavel for Branch Not Taken Bool
                    elif index == 8:
                        instr.imm = item            #Immediate Value            String
                    elif index == 9:
                        instr.nemonic = item        #Nemonic (Assembly Code)    String
                        bblock.append(instr)
    return prog
