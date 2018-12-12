from tkinter import *

root = Tk()

def leftKey(event):
    print("Left")
def rightKey(event):
    print("Right")
def upKey(event):
    print("Up")
def downKey(event):
    print("Down")


frame = Frame(root, width=0, height=0)
root.bind("<Left>", leftKey)
root.bind('<Right>', rightKey)
root.bind('<Up>', upKey)
root.bind('<Down>', downKey)
frame.pack()
root.mainloop()
