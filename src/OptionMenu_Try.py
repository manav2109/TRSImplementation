import tkinter as tk

def option_changed(event):
    selected_option = var.get()
    print(f"Selected option: {selected_option}")
    # Add your callback logic here

root = tk.Tk()
root.title("OptionMenu with Callback")

options = ["Option 1", "Option 2", "Option 3"]

var = tk.StringVar(root)
var.set(options[0])  # default value

option_menu = tk.OptionMenu(root, var, *options, command=option_changed)
option_menu.pack(padx=20, pady=20)

root.mainloop()
