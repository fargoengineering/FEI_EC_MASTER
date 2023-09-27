import pysoem
import struct
from global_vars import *

class etherCAT:
    
    def __init__(self):  
        self.master = pysoem.Master()
        self.gv = global_vars()
        
        # expected_slave_mapping? Needed?
        
    def run_ec(self):
        
        self.master.open(self.gv.ec_adapter_name)   # make sure matching correct platform
        
        if self.master.config_init() > 0:
            
            for slave in enumerate(self.master.slaves):
                print(f"Slave name: {slave.name}")
                
            self.master.config_map()
            
            # wait 50 ms for slaves to reach SAFE_OP state
            if self.master.state_check(pysoem.SAFEOP_STATE, 50000) != pysoem.SAFEOP_STATE:
                self.master.read_state()
                for slave in self.master.slaves:
                    if not slave.state == pysoem.OP_STATE:
                        print(f"{slave.name} did not reach OP state")
                # raise Exception('not all slaves reached OP state')
                
    def update_pdo(self,command,data,slot_number):
        
        # WRITE OUTPUT PDO
        # need to validate that this is the correct order
        packed_output = struct.pack('lll',command,data,slot_number) 
        self.master.slaves[0].output = packed_output
        self.master.send_processdata()
        
        # READ INPUT PDO
        self.master.receive_processdata(2000)
        # get data returned and print them to output text

        