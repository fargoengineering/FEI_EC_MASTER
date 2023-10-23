import os
import threading
import time
from global_vars import *
from UserInterface.generate_ui import *
from UserInterface.update_ui import *
from fei_ethercat import *
from UserInterface.parse_excel_ngio import *


gv = global_vars()
ec = etherCAT()
pe = parse_excel(gv)
gu = generate_ui(gv,ec)
ui = update_ui(gv)

# Normal GUI Operation
pe.parse_excel() # parse excel config file
ec.run_ec() # start etherCAT 
gu.generate_ui() # generate UI
gu.read_pdo_thread()
gu.mainloop()
# END Normal GUI Operation

# Benchmark Testing, Loop through number of boards
# num_boards = 32

# # 
# type = 3
# ec.run_ec()
# while(1):
        
#     start = time.time()
#     # for board in range(1,num_boards+1):
#         #ec.update_pdo(5,board,1,1,1,1,1,type)
#         # print(f"board: {board} type: {type}")
    
#     ec.update_pdo(5,2,1,1,1,1,1,type)
#     time.sleep(1)
        
#     if(type<9):
#         type=type+1
#     else:
#         type = 1
#     end = time.time()    
#     elapsed = end - start

#     print(f"took {elapsed} seconds to write to {num_boards} slots")
#     # time.sleep(5)
#     pass
# ec.close_ec()
#END benchmark testing

#hybrid test
# pe.parse_excel() # parse excel config file
# ec.run_ec() # start etherCAT 

# #set all to type 1:
# for board in range(1,33):
#     ec.update_pdo(5,board,1,1,1,1,1,1)

# gu.generate_ui() # generate UI
# gu.read_pdo_thread()
# gu.mainloop()
# END hybrid testing