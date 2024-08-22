import utils.IRPaser
import utils.ProgFile
import llvm.Gen_LLVMtoDFG
import llvm.Gen_LLVMtoCFG
import argparse


parser = argparse.ArgumentParser(description="引数の例")

parser.add_argument('r_file_path_src',  help='source file path',        default='.')
parser.add_argument('w_file_path'       help='gened file path',         default='.')
parser.add_argument('r_file_name',      help='source ll file name')
parser.add_argument('w_file_name',      help='gen type: CFG/DFG/DCFG',  default=None)

parser.add_argument('gen_type',         help='gen type: cdfg/dfg/cfg',  default=None)
parser.add_argument('parse',            help='pasing IR: yes/no',       default='no')


args = parser.parse_args()


Gen_DFG     = False
Gen_CFG     = False
if 'cdfg' == parser.gen_type:
    Gen_DFG     = True
    Gen_CFG     = True
elif 'dfg' == parser.gen_type:
    Gen_DFG     = True
elif 'cfg' == parser.gen_type:
    Gen_CFG     = True


r_file_path = parser.r_file_path_src
r_file_name = parser.r_file_name


w_file_path = parser.w_file_path
if None != w_file_name:
    w_file_name = parse.w_file_name
else:
    w_file_name = r_file_name


if 'yes' == parser.parse:
    prog = IR_Parser( r_file_path_src, r_file_name_src )
    ProgWriter( prog, w_file_path, w_file_name )

if Gen_DFG:
    Main_Gen_LLVMtoDFG( r_file_path, r_file_name, w_file_path )

if Gen_CFG:
    Main_Gen_LLVMtoCFG( r_file_path, r_file_name, w_file_path )