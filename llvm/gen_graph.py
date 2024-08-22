import utils.IRPaser as irparser
import utils.ProgFile as progfile
import Gen_LLVMtoDFG
import Gen_LLVMtoCFG
import argparse

open('utils/__init__.py', 'a').close()

import argparse

parser = argparse.ArgumentParser(description="args")

# 必須ではないオプション引数として定義
parser.add_argument('--src_path',   help='source file path',        default='.')
parser.add_argument('--w_path',     help='gened file path',         default='.')
parser.add_argument('--src_name',   help='source ll file name',     required=True)
parser.add_argument('--w_name',     help='gened file name',         default=None)
parser.add_argument('--gen_type',   help='gen type: cdfg/dfg/cfg',  required=True)
parser.add_argument('--parse',      help='parsing IR: yes/no',      default='no')

args = parser.parse_args()


Gen_DFG     = False
Gen_CFG     = False
if 'cdfg' == args.gen_type:
    Gen_DFG     = True
    Gen_CFG     = True
elif 'dfg' == args.gen_type:
    Gen_DFG     = True
elif 'cfg' == args.gen_type:
    Gen_CFG     = True


r_file_path = args.src_path
r_file_name = args.src_name


w_file_path = args.w_path
if None != args.w_name:
    w_file_name = args.w_name
else:
    w_file_name = r_file_name.split('.')[0]+'.txt'


#if 'yes' == args.parse:
#    prog = irparser.IR_Parser( r_file_path, r_file_name )
#    progfile.ProgWriter( prog, w_file_path, w_file_name )

prog = irparser.IR_Parser( r_file_path, r_file_name )

if Gen_DFG:
    Gen_LLVMtoDFG.Main_Gen_LLVMtoDFG( prog, r_file_path, r_file_name, w_file_path )

if Gen_CFG:
    Gen_LLVMtoCFG.Main_Gen_LLVMtoCFG( prog, r_file_path, r_file_name, w_file_path )