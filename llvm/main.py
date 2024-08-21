import utils.ProgFile
import utils.IRPaser
import Gen_LLVMtoCDFG

Gen_DFG     = False
Gen_CFG     = False

r_file_path_src = ""
r_file_name_src = ""

w_file_path = ""
w_file_name = ""

prog = IR_Parser( r_file_path_src, r_file_name_src )
ProgWriter( prog, w_file_path, w_file_name )

r_file_path = w_file_path
r_file_name = w_file_name

if Gen_DFG:
    Main_Gen_LLVMtoDFG( r_file_path, r_file_name, w_file_path )

if Gen_CFG:
    Main_Gen_LLVMtoCFG( r_file_path, r_file_name, w_file_path )
