import tkinter as tk
from pynput.keyboard import Key, Listener
import threading
import random

root = tk.Tk()
is_visible = True
current_color = 'red'

def change_color():
    global current_color
    current_color = random.choice(["red", "blue", "green"])
    canvas.itemconfig(dot, fill=current_color, outline=current_color)

def on_press(key):
    global is_visible

    if key == Key.ctrl_l or key == Key.ctrl_r:
        root.after(0, change_color)

    if key == Key.space:
        root.destroy()

    if key == Key.shift:
        if is_visible:
            root.withdraw()
        else:
            root.deiconify()
        is_visible = not is_visible

def keyboard_listener():
    with Listener(on_press=on_press) as listener:
        listener.join()

def main():
    global canvas, dot

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    print(screen_width,"x", screen_height)
    print("Press (Ctrl) to change the color.")
    print("Press (Space) to exit the overlay.")
    print("Press (Shift) to show or hide overlay.")

    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.geometry(f'20x20+{screen_width//2-10}+{screen_height//2-10}')
    root.resizable(width=False, height=False)
    root.wm_attributes("-transparentcolor", "black")

    canvas = tk.Canvas(root, width=20, height=20, bg='black', highlightthickness=0)
    canvas.pack()
    dot = canvas.create_oval(5, 5, 8, 8, fill=current_color, outline=current_color)

    root.mainloop()

listener_thread = threading.Thread(target=keyboard_listener, daemon=True)
listener_thread.start()

main()