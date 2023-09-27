
class ui_callbacks:
    def __init__(self,ob1):
        self.gv = ob1
    
    def on_button_click(self):
        
        slot_number = self.gv.slot_entry.get()
        data_value = self.gv.data_entry.get()
        selected_command = self.gv.command_var.get()
        
        self.gv.output_text.set(f"SLOT #: {slot_number}\nDATA: {data_value}\nCOMMAND: {selected_command}")