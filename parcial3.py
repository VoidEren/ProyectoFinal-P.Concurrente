import tkinter as tk
from tkinter import messagebox


def main():
    root = tk.Tk()
    root.title("Parcial 3")
    root.geometry("600x400")
    root.resizable(False, False)

    tk.Label(root, text="Parcial 3", font=("Arial", 24, "bold")).pack(pady=20)
    
    tk.Label(root, text="Aquí van los archivos y contenido del Parcial 3", 
             font=("Arial", 14)).pack(pady=20)

    # Aquí puedes agregar más contenido
    tk.Button(root, text="Cerrar", bg="#FF0000", fg="white", 
              font=("Arial", 12), command=root.destroy).pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    main()
