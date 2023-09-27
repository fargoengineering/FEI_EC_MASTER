import tkinter as tk

def on_button_click():
    slot_number = slot_entry.get()
    data_value = data_entry.get()
    selected_command = command_var.get()
    
    output_text.set(f"SLOT #: {slot_number}\nDATA: {data_value}\nCOMMAND: {selected_command}")

# Create the main window
root = tk.Tk()
root.title("Input Form GUI")

# Increase the window size
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
command_options = ["Option 1", "Option 2", "Option 3"]
command_var = tk.StringVar(root)
command_dropdown = tk.OptionMenu(root, command_var, *command_options)
command_dropdown.pack(pady=5)

# Create a button
button = tk.Button(root, text="Submit", command=on_button_click)
button.pack(pady=10)

# Create a label to display the output
output_text = tk.StringVar(root)
output_label = tk.Label(root, textvariable=output_text, fg="blue", font=("Arial", 12))
output_label.pack(pady=10)

# Run the GUI main loop
root.mainloop()
