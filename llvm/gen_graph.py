##################################################################
##
##	ElectronNest_CP
##	Copyright (C) 2024  Shigeyuki TAKANO
##
##  GNU AFFERO GENERAL PUBLIC LICENSE
##	version 3.0
##
##################################################################

import utils.IRPaser as irparser
import utils.FileUtils as progfile
import Gen_LLVMtoDFG
import Gen_LLVMtoCFG
import argparse

open('utils/__init__.py', 'a').close()

parser = argparse.ArgumentParser(description="args")

parser.add_argument('--src_path',   help='source file path',        default='.')
parser.add_argument('--w_path',     help='gened file path',         default='.')
parser.add_argument('--src_name',   help='source file name',        required=True)
parser.add_argument('--w_name',     help='gened file name',         default=None)
parser.add_argument('--gen_type',   help='gen type: cdfg/dfg/cfg',  required=True)
parser.add_argument('--block',      help='block: yes/no',           default='no')
parser.add_argument('--nm_mode',    help='mnemonic mode: yes/no',   default='yes')
parser.add_argument('--unique_id',  help='unique id: yes/no',       default='yes')
parser.add_argument('--parse',      help='parsing IR: yes/no',      default='yes')

args = parser.parse_args()


if 'no' == args.nm_mode:
    MNEMONIC_MODE   = False
else:
    MNEMONIC_MODE   = True

if 'no' == args.unique_id:
    UNIQUE_ID       = False
else:
    UNIQUE_ID       = True


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


prog = irparser.IR_Parser( r_file_path, r_file_name )
if 'yes' == args.parse:
    progfile.ProgWriter( prog, w_file_path, w_file_name )

if Gen_DFG and 'no' == args.block:
    Gen_LLVMtoDFG.Main_Gen_LLVMtoDFG( prog, w_file_path )

if Gen_DFG and 'yes' == args.block:
    Gen_LLVMtoDFG.BlockDataFlowExtractor( prog, MNEMONIC_MODE, UNIQUE_ID )

if Gen_CFG:
    Gen_LLVMtoCFG.Main_Gen_LLVMtoCFG( prog, w_file_path )