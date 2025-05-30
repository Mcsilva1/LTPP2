import tkinter as tk
from interface import Interface

def main():
    root = tk.Tk()
    app = Interface(root)
    app.run()

if __name__ == "__main__":
    main()