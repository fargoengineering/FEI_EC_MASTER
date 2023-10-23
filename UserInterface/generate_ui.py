import threading
from global_vars import *
from UserInterface.ui_callbacks import *
from fei_pdo import *

class generate_ui:
    def __init__(self,ob1,ob2):
        self.gv = ob1
        self.ec = ob2
        # self.uc = ui_callbacks(ob1,self.ec)
        self.pdo = fei_pdo()
        
        
    def generate_ui(self):
        self.root = tk.Tk()
        self.root.title("FEI NGIO TEST")
        self.root.geometry("700x600")
        
        # Create labels and entry widgets for "SLOT #" and "DATA"
        self.slot_label = tk.Label(self.root, text="SLOT #:")
        self.slot_label.pack(pady=5)
        self.slot_entry = tk.Entry(self.root)
        self.slot_entry.pack(pady=5)
        
        self.data1_label = tk.Label(self.root, text=f"DATA 1/2")
        self.data1_label.pack(pady=3)
        self.data1_entry = tk.Entry(self.root)
        self.data1_entry.pack(pady=3)
        
        self.data2_label = tk.Label(self.root, text=f"DATA 3/4")
        self.data2_label.pack(pady=3)
        self.data2_entry = tk.Entry(self.root)
        self.data2_entry.pack(pady=3)
        
        # self.data3_label = tk.Label(self.root, text=f"DATA 3")
        # self.data3_label.pack(pady=3)
        # self.data3_entry = tk.Entry(self.root)
        # self.data3_entry.pack(pady=3)
        
        # self.data4_label = tk.Label(self.root, text=f"DATA 4")
        # self.data4_label.pack(pady=3)
        # self.data4_entry = tk.Entry(self.root)
        # self.data4_entry.pack(pady=3)
        
        self.data5_label = tk.Label(self.root, text=f"DATA 5")
        self.data5_label.pack(pady=3)
        self.data5_entry = tk.Entry(self.root)
        self.data5_entry.pack(pady=3)
        
        # Create a dropdown for "COMMAND"
        self.command_label = tk.Label(self.root, text="COMMAND:")
        self.command_label.pack(pady=5)
        # self.command_options = ["NumberSlots", "LightShow", "IdentifySlot", "SetSlotType","SetBLEStatus"]
        self.command_options = ["SetSlotType","SetBLEStatus","SetRelays"]
        self.command_var = tk.StringVar(self.root)
        self.command_dropdown = tk.OptionMenu(self.root, self.command_var, *self.command_options)
        self.command_dropdown.pack(pady=5)

        # Create a button
        # change callback function to revert to FEI_5 ESI
        self.button = tk.Button(self.root, text="Submit", command=self.on_button_click)
        self.button.pack(pady=10)

        # Create a label to display the output
        self.output_text = tk.StringVar(self.root)
        self.output_label = tk.Label(self.root, textvariable=self.output_text, fg="blue", font=("Arial", 12))
        self.output_label.pack(pady=10)
    
    def mainloop(self):
        # start the ui
        self.root.mainloop()

    def on_button_click(self):        
        c = 1
        board_num=1
        slot_number = self.slot_entry.get()
        data1_2_value = self.data1_entry.get()
        data3_4_value = self.data2_entry.get()
        # data3_value = self.data3_entry.get()
        # data4_value = self.data4_entry.get()
        data5_value = self.data5_entry.get()
        selected_command = self.command_var.get()
        
        data1_value = (int(data1_2_value) >> 8) & 0xff
        data2_value = (int(data1_2_value)) & 0xff
        data3_value = (int(data3_4_value) >> 8) & 0xff
        data4_value = (int(data3_4_value)) & 0xff
        
        if selected_command == "SetSlotType":
            c = 5
        if selected_command == "SetBLEStatus":
            c = 6
        if selected_command == "SetRelays":
            c = 7
        
        self.ec.update_pdo(c,slot_number,board_num,data1_value,data2_value,data3_value,data4_value,data5_value)
        
        self.output_text.set(self.ec.read_pdo())
    
    def read_pdo_thread(self):
        self.output_text.set(self.ec.read_pdo())        
        th1 = threading.Timer(0.5,self.read_pdo_thread)
        th1.setDaemon(True)
        th1.start()