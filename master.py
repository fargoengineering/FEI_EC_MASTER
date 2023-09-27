import pysoem
import RPi.GPIO as GPIO
import collections
import struct
from time import sleep

class FEImaster:

    slave_list = []
    FEI_PRODUCT_CODE = 0x0101
    FEI_VENDOR_ID = 0x00000EEA

    def __init__(self):
        self.master = pysoem.Master()
        self.master.open('eth0')
        
        SlaveSet = collections.namedtuple(
            "SlaveSet", "slave_name product_code config_func"
        )
        self._expected_slave_mapping = {
            0: SlaveSet("FEI_SLAVE_v7", self.FEI_PRODUCT_CODE, self.slave_setup)
        }
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(20, GPIO.OUT)

    def slave_setup(self, slave_pos):  
        slave = self._master.slaves[slave_pos]

        slave.sdo_write(0x1c12, 0, struct.pack('B', 0))

        map_1c13_bytes = struct.pack('BxHH', 2, 0x1A00)
        slave.sdo_write(0x1c13, 0, map_1c13_bytes, True)

    def scan(self):
        # Find slave devices
        if self.master.config_init() > 0:
            for slave in self.master.slaves:
                print(f"Device Located: {slave.name}")
        else: 
            print('no slaves found')
            self.master.close()

    def connect_to_slaves(self):
        # Add Slaves to a list
        if self.master.config_init() > 0:
            for slave in self.master.slaves:
                print(f"Connected to: {slave.name}")
                print(f"Slave ID: {slave.id}")
                print(f"Slave revision: {slave.rev}")
                print(f"Slave manufacturer: {slave.man}")
                self.slave_list.append(slave)
                
    def set_state(self, state):
        # config_init returns the number of slaves found
        if self.master.config_init() > 0:

            print("{} slaves found and configured".format(len(self.master.slaves)))

            # for i, slave in enumerate(self.master.slaves):
            #     assert(slave.man == self.FEI_VENDOR_ID)
            #     assert(slave.id == self._expected_slave_mapping[i].product_code)
            #     slave.config_func = self._expected_slave_mapping[i].config_func

            # PREOP_STATE to SAFEOP_STATE request - each slave's config_func is called
            self.master.config_map()

            # wait 50 ms for all slaves to reach SAFE_OP state
            if self.master.state_check(pysoem.SAFEOP_STATE, 50000) != pysoem.SAFEOP_STATE:
                self.master.read_state()
                for slave in self.master.slaves:
                    if not slave.state == pysoem.SAFEOP_STATE:
                        print('{} did not reach SAFEOP state'.format(slave.name))
                        print('al status code {} ({})'.format(hex(slave.al_status),pysoem.al_status_code_to_string(slave.al_status)))
                raise Exception('not all slaves reached SAFEOP state')

            self.master.state = pysoem.OP_STATE
            self.master.write_state()

            self.master.state_check(pysoem.OP_STATE, 50000)
            if self.master.state != pysoem.OP_STATE:
                self.master.read_state()
                for slave in self.master.slaves:
                    if not slave.state == pysoem.OP_STATE:
                        print('{} did not reach OP state'.format(slave.name))
                        print('al status code {} ({})'.format(hex(slave.al_status),pysoem.al_status_code_to_string(slave.al_status)))
                raise Exception('not all slaves reached OP state')
                
    def process_PDO(self):
        # Sync PDO 
        for i in range(100):
            self.master.send_processdata()        
            self.master.receive_processdata(2000)
            sleep(0.1)
            
        for slave in self.master.slaves:
            print(f"Input: {self.master.read(0x1A00,0x2)}")
            
                
    def disconnect(self):
        self.master.state = pysoem.INIT_STATE
        self.master.write_state()
        self.master.close()
        GPIO.cleanup()
        print("DISCONNECTED")
                      
if __name__ == '__main__':
    m = FEImaster()
    # try:
    m.scan()
    m.connect_to_slaves()    
    m.set_state(3)
    m.process_PDO()
    sleep(10)        
    m.disconnect()
    # except Exception:
    #     m.disconnect()