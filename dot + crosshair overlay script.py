import tkinter as tk
from pynput.keyboard import Key, Listener
import threading
import ctypes
import itertools

tinker = tk.Tk() # --> определение ткинтера
is_visible = True # --> переменная для отображения точки (включение\выключение)
crosshair_visible = False # --> выключение\включение прицела
dot_visible = True # --> выключение\включение точки
colors = itertools.cycle(['#ff0000', '#34a8ff', '#050505', '#ffffff']) # --> цвета для change_color()
current_color = next(colors)
x1, y1, x2, y2 = 5, 5, 8, 8 # --> первичные координаты точки

def make_window_clickthrough(hwnd) -> None: # --> позволяет мыши не появляться во время взаимодействия с игрой\окном
    extended_style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
    extended_style |= 0x00000020  # WS_EX_TRANSPARENT
    extended_style |= 0x00080000  # WS_EX_LAYERED
    ctypes.windll.user32.SetWindowLongW(hwnd, -20, extended_style)

def change_color() -> None: # --> меняет цвет прицела
    global current_color
    current_color = next(colors)
    canvas.itemconfig(dot, fill=current_color, outline=current_color)
    canvas.itemconfig(crosshair_h, fill=current_color)
    canvas.itemconfig(crosshair_v, fill=current_color)

def on_press(key) -> None: # --> добавляет действия по нажатию определённой клавиши
    global is_visible, x1, y1, x2, y2, current_color, crosshair_visible, dot_visible

    if key == Key.end: # --> отрисовка прицела\точки
        if dot_visible: # --> если точка видна, прицел не показываем
            canvas.itemconfig(dot, state='hidden')
            crosshair_visible = True
            dot_visible = False
            canvas.itemconfig(crosshair_h, state='normal')
            canvas.itemconfig(crosshair_v, state='normal')
        else: # --> если точка не видна, прицел показываем
            canvas.itemconfig(crosshair_h, state='hidden')
            canvas.itemconfig(crosshair_v, state='hidden')
            crosshair_visible = False
            dot_visible = True
            canvas.itemconfig(dot, state='normal')

    elif key == Key.delete: # --> меняет цвет
        tinker.after(0, change_color)

    elif key == Key.page_up: # --> меняет размер(больше)
        if x2 - x1 < 20 and y2 - y1 < 10:
            x1 -= 0.5 
            y1 -= 0.5
            x2 += 0.5
            y2 += 0.5
            tinker.after(0, canvas_cords)

    elif key == Key.page_down: # --> меняет размер(меньше)
        if x2 - x1 > 3 and y2 - y1 > 3:
            x1 += 0.5
            y1 += 0.5 
            x2 -= 0.5
            y2 -= 0.5
            tinker.after(0, canvas_cords)

    elif key == Key.insert: # --> убивает процесс
        tinker.destroy()

    elif key == Key.home: # --> показывает\скрывает прицел
        if is_visible:
            tinker.withdraw()
        else:
            tinker.deiconify()
        is_visible = not is_visible

def canvas_cords() -> None: # --> обновляет размер
    canvas.coords(dot, x1, y1, x2, y2)

def keyboard_listener() -> None: # --> слушает нажатия клавишь
    with Listener(on_press=on_press) as listener:
        listener.join()

def main() -> None: # --> мейн функция, создание прозрачного окна, определение переменных dot, crosshair_v, crosshair_h, canvas 
    global canvas, dot, crosshair_h, crosshair_v

    screen_width = tinker.winfo_screenwidth() # --> сбор информации по ширине
    screen_height = tinker.winfo_screenheight() # --> сбор информации по высоте

    print(f"Ur current resolution: {screen_width}x{screen_height}\n") # --> вывод твоего текущего разрешения экрана
    print("Press (End) to toggle between dot and crosshair.")
    print("Press (Delete) to change the color.")
    print("Press (Insert) to exit the overlay.")
    print("Press (Home) to show or hide overlay.")
    print("Press (PAGEUP/PAGEDOWN) to modulate dot size.")

    tinker.overrideredirect(True)
    tinker.attributes("-topmost", True) # --> поверх окон
    tinker.geometry(f'200x200+{screen_width//2-7}+{screen_height//2-7}') # --> размер окна процесса
    tinker.resizable(width=False, height=False) # --> можно\нельзя ли менять размер окна
    tinker.wm_attributes("-transparentcolor", "black") # --> атрибуты процесса

    canvas = tk.Canvas(tinker, width=200, height=200, bg='black', highlightthickness=0)
    canvas.pack()

    dot = canvas.create_oval(x1, y1, x2, y2, fill=current_color, outline=current_color) # --> создание овала
    crosshair_h = canvas.create_line(0, 7, 15, 7, fill=current_color, state='hidden', width=1) # --> создание первой линии прицела
    crosshair_v = canvas.create_line(7, 0, 7, 15, fill=current_color, state='hidden', width=1) # --> создание второй линии прицела

    tinker.update_idletasks()
    tinker.update()

    hwnd = ctypes.windll.user32.GetParent(tinker.winfo_id())
    make_window_clickthrough(hwnd)

    tinker.mainloop() # --> луп процесса

listener_thread = threading.Thread(target=keyboard_listener, daemon=True) # --> листенер запускается в отдельном потоке
listener_thread.start() # --> ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

main()
