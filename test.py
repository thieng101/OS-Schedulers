import tkinter as tk
from tkinter import ttk

def test_tkinter():
    root = tk.Tk()
    root.title("Test Tkinter")
    root.geometry("800x600")
    label = ttk.Label(root, text="If you see this, Tkinter is working!", font=("Arial", 24))
    label.pack(expand=True)
    root.mainloop()

if __name__ == "__main__":
    test_tkinter()
