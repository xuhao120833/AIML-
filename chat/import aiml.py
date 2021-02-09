import tkinter as tk
from PIL import ImageTk, Image
 
root = tk.Tk()
#背景
canvas = tk.Canvas(root, width=1200,height=699,bd=0, highlightthickness=0)
imgpath = 'D:\\chat\\3.gif'
img = Image.open(imgpath)
photo = ImageTk.PhotoImage(img)
 
canvas.create_image(700, 500, image=photo)

canvas.create_window(100, 50, width=100, height=20, window=entry)
root.mainloop()