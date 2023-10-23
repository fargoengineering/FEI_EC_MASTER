from fei_ethercat import *
class ui_callbacks:
    def __init__(self,ob1,ob2):
        self.gv = ob1
        self.ec = ob2
    
    def on_button_click(self):
        c = 1
        slot_number = self.gv.slot_entry.get()
        data_value = self.gv.data_entry.get()
        selected_command = self.gv.command_var.get()
        
        self.gv.output_text.set(f"SLOT #: {slot_number}\nDATA: {data_value}\nCOMMAND: {selected_command}")
        
        if selected_command == "SetSlotType":
            c = 5
        if selected_command == "SetBLEStatus":
            c = 6
        
        self.ec.update_pdo(c,data_value,slot_number)