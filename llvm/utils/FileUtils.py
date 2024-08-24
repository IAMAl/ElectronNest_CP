##################################################################
##
##	ElectronNest_CP
##	Copyright (C) 2024  Shigeyuki TAKANO
##
##  GNU AFFERO GENERAL PUBLIC LICENSE
##	version 3.0
##
##################################################################

import utils.ProgConstructor as progconst


def ReadFile( file_path=".", file_name="" ):
    """
    File-Open used for CFG (cyclic loops) file

    Arguments
        file_path:    path (directory) for source file
        file_name:    name of file for source file
    """
    with open(file_path +"/"+ file_name, "r") as file:
        lines = []
        for line in file:
            #print("reading line: {}".format(line))
            line = line.replace("\n", '')
            lines.append(line)

        return lines


def ProgWriter( prog, w_file_path=".", w_file_name="" ):
    """
    Program File Read and Composition

    Arguments:
        w_file_path:        Writinging File Path
        w_file_name:        File Name

    Function:
        - Write parsed program to file
    """
    openfile = w_file_path +"/"+ w_file_name
    with open(openfile, "w") as program:
        program.write("program {}\n".format(prog.name))
        for func in prog.funcs:
            program.write("\nbegin function {}\n".format(func.name))
            for bblock in func.bblocks:
                program.write("\nbegin bblock {}\n".format(bblock.name))
                for instr in bblock.instrs:
                    #print(instr.operands)
                    instruction = []
                    instruction.append(instr.opcode)     #Opcode Name                String
                    instruction.append(instr.dst)        #Destination Name           String
                    instruction.append(instr.d_type)     #Destination Data-Type      String
                    instruction.append(instr.operands)   #Source Name                String
                    instruction.append(instr.func)       #Function Name              String
                    instruction.append(instr.br_t)       #Lavel for Branch Taken     Bool
                    instruction.append(instr.br_f)       #Lavel for Branch Not Taken Bool
                    instruction.append(instr.imm)        #Immediate Value            String
                    instruction.append(instr.nemonic)    #Nemonic (Assembly Code)    String
                    program.writelines(str(instruction)+"\n")
                program.write("end bblock {}\n".format(bblock.name))
            program.write("\nend function {}\n".format(func.name))


def ProgReader( r_file_path=".", r_file_name="" ):
    """
    Program File Read and Composition

    Arguments:
        r_file_path:        Reading File Path
        r_file_name:        File Name

    Function:
        - Read File of parsed program
        - Compose program() class
    """
    openfile = r_file_path +"/"+ r_file_name.split('.')[0]+'.txt'
    with open(openfile, "r") as prog_file:
        in_prog = False
        in_func = False
        in_bblock = False
        for line in prog_file:
            if "program" in line:
                prog = progconst.program()
                prog.name = line.split(" ")[1].replace('"\n', '').replace('"', '')
                in_prog = True
            elif "begin function" in line:
                func = progconst.function()
                func.name = line.split(" ")[2].replace('"\n', '').replace('"', '')
                in_func  = True
            elif "begin bblock" in line:
                bblock = progconst.basicblock()
                bblock.name = line.split(" ")[2].replace('"\n', '').replace('"', '')
                in_bblock  = True
            elif "end bblock" in line:
                func.bblocks.append(bblock)
                in_bblock  = False
            elif "end function" in line:
                prog.funcs.append(func)
                in_func  = False
            elif in_prog and in_func and in_bblock:
                instr = progconst.instruction()
                line = line.split("\"")
                for index, item in enumerate(line):
                    item = item.replace('"\n', '')
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


def ReadAM( file_path=".", file_name="" ):
    """
    File-Open used for AM file

    Arguments
        file_path:    path (directory) for source file
        file_name:    name of file for source file
    """

    f = open( file_path +'/'+ file_name )
    return f