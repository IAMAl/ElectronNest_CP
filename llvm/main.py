import Gen_LLVMtoCDFG

Gen_DFG     = False
Gen_CFG     = False

if Gen_DFG:
    Main_Gen_LLVMtoDFG( r_file_path, r_file_name, dir_dot )

if Gen_CFG:
    Main_Gen_LLVMtoCFG( r_file_path, r_file_name, dir_dot )
