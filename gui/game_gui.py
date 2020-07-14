import tkinter as tk

window = tk.Tk()

board_frame = tk.Frame()

pegs = []

btn = tk.Button(master=board_frame, width=100, height=100)

board_frame.pack()
window.mainloop()


frame1 = tk.Frame(master=window, width=100, height=100, bg="red")
frame1.pack()

frame2 = tk.Frame(master=window, width=50, height=50, bg="yellow")
frame2.pack()

frame3 = tk.Frame(master=window, width=25, height=25, bg="blue")
frame3.pack()

