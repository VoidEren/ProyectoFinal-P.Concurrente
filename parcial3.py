import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import sys


def ruta_recurso(nombre_archivo):
    """Devuelve la ruta del archivo, compatible con PyInstaller."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, nombre_archivo)
    # Usar el directorio del script actual
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, nombre_archivo)


# Variable global para mantener la referencia de la imagen
bg_photo_ref = None


def main():
    global bg_photo_ref
    
    root = tk.Tk()
    root.title("Parcial 3")
    root.geometry("800x600")
    root.resizable(False, False)

    # ----- FONDO -----
    try:
        imagen_dashboard = ruta_recurso("fondochido.jpg")
        print(f"Cargando imagen desde: {imagen_dashboard}")
        print(f"Existe: {os.path.exists(imagen_dashboard)}")
        
        bg_image = Image.open(imagen_dashboard)
        bg_image = bg_image.resize((800, 600))
        bg_photo_ref = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(root, image=bg_photo_ref)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print(f"Error al cargar imagen: {e}")
        root.configure(bg="#cccccc")

    # ----- CONTENIDO SOBRE EL FONDO -----
    frame = tk.Frame(root, bg="gray30")  # Color gris oscuro
    frame.pack(pady=30)

    tk.Label(frame, text="Parcial 3", font=("Arial", 24, "bold"), bg="gray30", fg="white").pack(pady=10)

    tk.Label(frame, text="Aquí van los archivos y contenido del Parcial 3",
             font=("Arial", 14), bg="gray30", fg="white").pack(pady=10)

    tk.Button(
        frame, text="Cerrar", bg="#FF0000", fg="white",
        font=("Arial", 12), command=root.destroy
    ).pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
