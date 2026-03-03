from tkinter import *
import tkinter as tk
from tkinter import ttk     # подключаем пакет ttk
from PIL import Image, ImageTk

root = Tk()     # создаем корневой объект - окно
root.title("пре-альфа-бэта-хуета")     # устанавливаем заголовок окна
root.iconbitmap(default="tolik.ico")
root.geometry("600x400")    # устанавливаем размеры окна
label = Label(text="ТОЛИК001") # создаем текстовую метку
label.pack()    # размещаем метку в окне
root.attributes("-toolwindow", True)

def finish():
    root.destroy()  # ручное закрытие окна и всего приложения
    print("Приложение закрыто пользователем")

root.protocol("WM_DELETE_WINDOW", finish)

btn = ttk.Button(text="Сохранить и выйти", command = finish) # создаем кнопку из пакета ttk
btn.place(x=225,y=300,width=150,height=60)    # размещаем кнопку в окне

original_image=tk.PhotoImage(file="tolik.png")
label=tk.Label(root,image=original_image)
label.place(x=170,y=40, width=260, height=260)

root.mainloop()