from global_vars import *
from UserInterface.ui_callbacks import *

class generate_ui:
    def __init__(self,ob1):
        self.gv = ob1
        self.uc = ui_callbacks(ob1)
        
        
    def generate_ui(self):
        root = tk.Tk()
        root.title("FEI NGIO DRIVER")
        root.geometry("900x700")
        
        # Create labels and entry widgets for "SLOT #" and "DATA"
        slot_label = tk.Label(root, text="SLOT #:")
        slot_label.pack(pady=5)
        slot_entry = tk.Entry(root)
        slot_entry.pack(pady=5)

        data_label = tk.Label(root, text="DATA:")
        data_label.pack(pady=5)
        data_entry = tk.Entry(root)
        data_entry.pack(pady=5)

        # Create a dropdown for "COMMAND"
        command_label = tk.Label(root, text="COMMAND:")
        command_label.pack(pady=5)
        command_options = ["NumberSlots", "LightShow", "IdentifySlot", "SetSlotType","SetBLEStatus"]
        command_var = tk.StringVar(root)
        command_dropdown = tk.OptionMenu(root, command_var, *command_options)
        command_dropdown.pack(pady=5)

        # Create a button
        button = tk.Button(root, text="Submit", command=self.on_button_click)
        button.pack(pady=10)

        # Create a label to display the output
        output_text = tk.StringVar(root)
        output_label = tk.Label(root, textvariable=output_text, fg="blue", font=("Arial", 12))
        output_label.pack(pady=10)
        
        # start the ui
        root.mainloop()
    
    def on_button_click(self):        
        slot_number = self.slot_entry.get()
        data_value = self.data_entry.get()
        selected_command = self.command_var.get()
        
        self.output_text.set(f"SLOT #: {slot_number}\nDATA: {data_value}\nCOMMAND: {selected_command}")
            