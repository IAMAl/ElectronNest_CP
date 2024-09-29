##################################################################
##
##	ElectronNest_CP
##	Copyright (C) 2024  Shigeyuki TAKANO
##
##  GNU AFFERO GENERAL PUBLIC LICENSE
##	version 3.0
##
##################################################################

import utils.FileUtils as fileutils
import utils.GraphUtils as graphutils
import funcs.Gen_Prog as genprog
import argparse

open('utils/__init__.py', 'a').close()

parser = argparse.ArgumentParser(description="args")

parser.add_argument('--src_path',   help='source file path',    default='.')
parser.add_argument('--w_path',     help='gened file path',     default='.')
parser.add_argument('--w_name',     help='gened file name',     default='agu_prog.ll')
parser.add_argument('--src_name',   help='source file name',    required=True)
parser.add_argument('--cfg_name',   help='cfg name',            required=True)

args = parser.parse_args()

r_file_path = args.src_path
r_file_name = args.src_name
name        = args.cfg_name
w_file_path = args.w_path

# Read Loop Paths in Control-Flow Graph
r_cfg_file_name = name+"_loop.txt"
cfg_paths = fileutils.ReadFile(file_path=r_file_path, file_name=r_cfg_file_name)
CyclicPaths = graphutils.NodeParser( cfg_paths, 'cfg' )

# Compose CFG_Nodes Object
r_file_name = r_file_name
CFG_Nodes = genprog.Preprocess( r_file_path, r_file_name, CyclicPaths )

CFGNodes_ = []
for index in range(len(CFG_Nodes)-1, -1, -1):
    CFG_Nodes[index].Reorder()
    CFGNodes_.append(CFG_Nodes[index])

# Tracking
print(f"BackTrack")
paths = genprog.BackTrack(CFGNodes_)

openfile = w_file_path +'/'+ name +".txt"
with open(openfile, "w") as agu_prog:
    for path in paths:
        for item in path:
            print(item)
            agu_prog.writelines(map(str, item))
