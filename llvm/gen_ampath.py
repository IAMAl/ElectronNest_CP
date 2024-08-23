import utils.FileUtils as fileutils
import Gen_AMtoPath
import argparse

open('utils/__init__.py', 'a').close()

parser = argparse.ArgumentParser(description="args")

parser.add_argument('--src_path',   help='source file path',    default='.')
parser.add_argument('--w_path',     help='gened file path',     default='.')
parser.add_argument('--src_name',   help='source file name',    required=True)
parser.add_argument('--format',     help='parsing IR: yes/no',  default='no')

args = parser.parse_args()

r_file_path = args.src_path
r_file_name = args.src_name
w_file_path = args.w_path


PATH_FORMAT = False
if 'yes'== args.format:
    PATH_FORMAT = True


prog = fileutils.ReadProgram( r_file_path=r_file_path, r_file_name=r_file_name )


for func in prog.funcs:
    name_func = func.name.replace('\n', '')

    for bblock in func.bblocks:
        name_bblock = bblock.name.replace('\n', '')
        r_file_name = name_func+"_bblock_"+name_bblock
        w_file_name = name_func+"_bblock_"+name_bblock

        Gen_AMtoPath.BackPath(PATH_FORMAT=PATH_FORMAT, r_file_path=r_file_path, r_file_name=r_file_name, w_file_path=w_file_path, w_file_name=w_file_name)


for func in prog.funcs:
    name_func = func.name.replace('\n', '')

    for bblock in func.bblocks:
        name_bblock = bblock.name.replace('\n', '')
        r_file_name = name_func+"_bblock_"+name_bblock
        w_file_name = name_func+"_bblock_"+name_bblock

        Gen_AMtoPath.StLdMarker(r_file_path=r_file_path, r_file_name=r_file_name, w_file_path=w_file_path, w_file_name=w_file_name)