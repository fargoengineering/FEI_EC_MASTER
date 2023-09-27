import pysoem
from global_vars import *

class etherCAT:
    
    def __init__(self):  
        self.master = pysoem.Master()
        self.gv = global_vars()
        
        # expected_slave_mapping? Needed?
        
    def run_ec(self):
        
        self.master.open(self.gv.ec_adapter_name)
        
        