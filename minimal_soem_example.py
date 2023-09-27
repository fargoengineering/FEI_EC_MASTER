"""Prints the analog-to-digital converted voltage of an EL3002.

Usage: python minimal_example.py <adapter>

This example expects a physical slave layout according to
_expected_slave_layout, see below.
"""

import sys
import struct
import time
import collections
import pysoem
# import RPi.GPIO as GPIO


class MinimalExample:

    # BECKHOFF_VENDOR_ID = 0x0002
    BECKHOFF_VENDOR_ID = 0x00000EEA
    # EK1100_PRODUCT_CODE = 0x044c2c52
    EL3002_PRODUCT_CODE = 0xBEEF

    def __init__(self):
        # self._ifname = ifname
        self._master = pysoem.Master()
        SlaveSet = collections.namedtuple(
            'SlaveSet', 'slave_name product_code config_func')
        # self._expected_slave_mapping = {0: SlaveSet('EK1100', self.EK1100_PRODUCT_CODE, None),1: SlaveSet('EL3002', self.EL3002_PRODUCT_CODE, self.el3002_setup)}
        # self._expected_slave_mapping = {0: SlaveSet('EL3002', self.EL3002_PRODUCT_CODE, self.el3002_setup)}
        self._expected_slave_mapping = {0: SlaveSet('EL3002', self.EL3002_PRODUCT_CODE, None)}
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(20,GPIO.OUT)
        # GPIO.output(20,GPIO.LOW)

    def el3002_setup(self, slave_pos):
        slave = self._master.slaves[slave_pos]

        slave.sdo_write(0x1c12, 0, struct.pack('B', 0))

        map_1c13_bytes = struct.pack('BxHH', 2, 0x1A01, 0x1A03)
        slave.sdo_write(0x1c13, 0, map_1c13_bytes, True)

    def run(self):

        # self._master.open(self._ifname)
        self._master.open("\\Device\\NPF_{2AFC35B5-1EE7-49B9-927D-D2CE5EDC52DD}")
        # self._master.open('eth0')

        # config_init returns the number of slaves found
        if self._master.config_init() > 0:

            print("{} slaves found and configured".format(
                len(self._master.slaves)))
            

            for i, slave in enumerate(self._master.slaves):
            #     assert(slave.man == self.BECKHOFF_VENDOR_ID)
            #     assert(
            #         slave.id == self._expected_slave_mapping[i].product_code)
            #         slave.config_func = self._expected_slave_mapping[i].config_func
                print(f"Slave name: {slave.name}")
            # PREOP_STATE to SAFEOP_STATE request - each slave's config_func is called
            self._master.config_map()

            # wait 50 ms for all slaves to reach SAFE_OP state
            if self._master.state_check(pysoem.SAFEOP_STATE, 50000) != pysoem.SAFEOP_STATE:
                self._master.read_state()
                for slave in self._master.slaves:
                    if not slave.state == pysoem.SAFEOP_STATE:
                        print('{} did not reach SAFEOP state'.format(slave.name))
                        print('al status code {} ({})'.format(hex(slave.al_status),
                                                              pysoem.al_status_code_to_string(slave.al_status)))
                raise Exception('not all slaves reached SAFEOP state')

            self._master.state = pysoem.OP_STATE
            self._master.write_state()

            self._master.state_check(pysoem.OP_STATE, 50000)
            if self._master.state != pysoem.OP_STATE:
                self._master.read_state()
                for slave in self._master.slaves:
                    if not slave.state == pysoem.OP_STATE:
                        print('{} did not reach OP state'.format(slave.name))
                        print('al status code {} ({})'.format(hex(slave.al_status),
                                                              pysoem.al_status_code_to_string(slave.al_status)))
                raise Exception('not all slaves reached OP state')

            try:
                data1 = 1 #b"\x05\x00\x00\x00"
                # data2 = 1 #b"\x06\x00\x00\x00"
                all_times = []
                while 1:

                    # GPIO.output(20,GPIO.HIGH)
                    start = time.time()

                    # # Write Output PDO
                    packed_output = struct.pack('ll',data1,0)
                    self._master.slaves[0].output = packed_output   #data                                        
                    self._master.send_processdata()
                    
                    data1 = data1 + 1
                    if (data1 == 8): data1 = 1

                    # # Read Input PDO
                    self._master.receive_processdata(2000)
                    voltage__bytes = self._master.slaves[0].input
                    print(f"input as bytes: {voltage__bytes}")                                        
                    vals_all = struct.unpack('lll', voltage__bytes)
                    print(f'slot1: {vals_all[0]}, missed counter: {vals_all[1]}, valid counter: {vals_all[2]}')
                    
                    # GPIO.output(20,GPIO.LOW)
                    end = time.time()
                    elapsed = (end - start ) * 1000
                    all_times.append(elapsed)
                    print(f"Took {elapsed} ms to process PDO")
                    average = (sum(all_times)) / (len(all_times))
                    print(f"Average time to process: {average}")
                    time.sleep(.5)

            except KeyboardInterrupt:
                # ctrl-C abort handling
                print('stopped')

            self._master.state = pysoem.INIT_STATE
            # request INIT state for all slaves
            self._master.write_state()
            self._master.close()
        else:
            print('slaves not found')


if __name__ == '__main__':

    print('minimal_example')

    
    MinimalExample().run()

