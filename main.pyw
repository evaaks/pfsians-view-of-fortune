from tkinter import Tk
from gui import GUI


def gui_demo():
    root = Tk()
    GUI(root)
    root.mainloop()


if __name__ == '__main__':
    gui_demo()
