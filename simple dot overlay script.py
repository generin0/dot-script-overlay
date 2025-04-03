import tkinter as tk
from pynput.keyboard import Key, Listener
import threading
import itertools

tinker = tk.Tk()
is_visible = True
colors = itertools.cycle(['red', 'blue', 'green', 'white'])
current_color = next(colors)

def change_color():
    global current_color
    current_color = next(colors)
    canvas.itemconfig(dot, fill=current_color, outline=current_color)
 
def on_press(key):
    global is_visible

    if key == Key.ctrl_l or key == Key.ctrl_r:
        tinker.after(0, change_color)

    if key == Key.space:
        tinker.destroy()

    if key == Key.shift:
        if is_visible:
            tinker.withdraw()
        else:
            tinker.deiconify()
        is_visible = not is_visible

def keyboard_listener():
    with Listener(on_press=on_press) as listener:
        listener.join()

def main():
    global canvas, dot

    screen_width = tinker.winfo_screenwidth()
    screen_height = tinker.winfo_screenheight()

    print(screen_width,"x", screen_height)
    print("Press (Ctrl) to change the color.")
    print("Press (Space) to exit the overlay.")
    print("Press (Shift) to show or hide overlay.")

    tinker.overrideredirect(True)
    tinker.attributes("-topmost", True)
    tinker.geometry(f'20x20+{screen_width//2-10}+{screen_height//2-10}')
    tinker.resizable(width=False, height=False)
    tinker.wm_attributes("-transparentcolor", "black")

    canvas = tk.Canvas(tinker, width=20, height=20, bg='black', highlightthickness=0)
    canvas.pack()
    dot = canvas.create_oval(5, 5, 8, 8, fill=current_color, outline=current_color)

    tinker.mainloop()

listener_thread = threading.Thread(target=keyboard_listener, daemon=True)
listener_thread.start()

main()
