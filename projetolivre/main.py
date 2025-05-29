from package.interface import InterfaceBiblioteca
import tkinter as tk

def main():
    root = tk.Tk()
    app = InterfaceBiblioteca(root)
    root.mainloop()

if __name__ == "__main__":
    main()