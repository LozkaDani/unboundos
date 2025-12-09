import tkinter as tk
from tkinter import scrolledtext
import os

text = ""

root = tk.Tk()
root.title("Graphic Unbound Text Editor (GUTE)")
root.geometry("1080x720")
root.iconbitmap("./root/system/apps_assets/icons/gute.ico")


current_file = ""
default_font = ("Consolas", 11)

def create_open_window():
    open_window = tk.Toplevel()
    open_window.title("Path to the File")
    open_window.geometry("200x200")
    open_window.iconbitmap("./root/system/apps_assets/icons/gute.ico")
    
    path_to_file = tk.Entry(open_window)
    path_to_file.focus_set()
    enter_button = tk.Button(open_window, text="Enter", command=lambda: open_path(path_to_file.get(), open_window))

    path_to_file.pack()
    enter_button.pack()

    root.wait_window(open_window)

def open_path(path, window):
    global text, current_file
    try:
        # Попробуем разные кодировки для русских файлов
        encodings = ['utf-8', 'cp1251', 'windows-1251', 'koi8-r']
        
        for encoding in encodings:
            try:
                with open(path, "r", encoding=encoding) as f:
                    text = f.read()
                # Вставляем текст в текстовое поле
                text_area.delete('1.0', tk.END)
                text_area.insert('1.0', text)
                
                # Обновляем заголовок окна
                root.title(f"GUTE - {os.path.basename(path)}")
                
                # Сохраняем путь к текущему файлу
                current_file = path
                
                window.destroy()
                return
            except UnicodeDecodeError:
                continue
        
        # Если ни одна кодировка не подошла, попробуем latin-1
        with open(path, "r", encoding='latin-1') as f:
            text = f.read()
        text_area.delete('1.0', tk.END)
        text_area.insert('1.0', text)
        root.title(f"GUTE - {os.path.basename(path)}")
        current_file = path
        
    except FileNotFoundError:
        tk.messagebox.showerror("Ошибка", f"Файл не найден: {path}")
    except Exception as e:
        tk.messagebox.showerror("Ошибка", f"Не удалось открыть файл:\n{str(e)}")
    
    window.destroy()

# Создаем меню
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)


upper_menu = tk.Menu(menu_bar, tearoff=0) 
menu_bar.add_cascade(label="File", menu=upper_menu)
upper_menu.add_command(label="Open", command=create_open_window)
#upper_menu.add_command(label="Сохранить", command=save_file)
upper_menu.add_separator()
upper_menu.add_command(label="Exit", command=root.quit)


header_frame = tk.Frame(root)
header_frame.pack(fill=tk.X, padx=10, pady=5)

gute = tk.Label(header_frame, text="GU TEXT EDITOR", font=("Arial", 14, "bold"))
fast_keys = tk.Label(header_frame, text="Fast Keys: Ctrl+S - Save, Ctrl+O - Open file")
open_window_button = tk.Button(root, text="Open file", command=lambda: create_open_window(), width=20, height=2)

#text_l = tk.Label(root, text=text)
# Текстовое поле с прокруткой
text_frame = tk.Frame(root)

# Добавляем скроллбар и текстовое поле
text_scroll = tk.Scrollbar(text_frame)
text_scroll.pack(side=tk.RIGHT, fill=tk.Y)

text_area = scrolledtext.ScrolledText(text_frame, 
                                     wrap=tk.WORD,
                                     yscrollcommand=text_scroll.set,
                                     font=default_font,
                                     bg='white',
                                     fg='black',
                                     padx=10,
                                     pady=10)

text_scroll.config(command=text_area.yview)

root.bind('<Control-o>', lambda e: create_open_window())
gute.pack(side = tk.LEFT)
fast_keys.pack(side = tk.RIGHT)
open_window_button.pack(pady=10)
#text_l.pack()
text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
text_area.pack(fill=tk.BOTH, expand=True)
root.mainloop()