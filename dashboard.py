import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import sys


def ruta_recurso(nombre_archivo):
    """Devuelve la ruta del archivo, compatible con PyInstaller."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, nombre_archivo)
    return os.path.join(os.path.abspath("."), nombre_archivo)


class DashboardApp:
    def __init__(self, root, username, email):
        self.root = root
        self.username = username
        self.email = email
        
        self.root.title("Dashboard Principal")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Fondo para dashboard
        imagen_dashboard = ruta_recurso("kareli.jpeg")
        bg_image = Image.open(imagen_dashboard)
        bg_image = bg_image.resize((800, 600))
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Título de bienvenida
        tk.Label(self.root, text=f"Bienvenido al Menú Principal, {username}",
                 font=("Arial", 18, "bold"), bg="SystemButtonFace").pack(pady=30)

        # Frame para los botones de parciales
        buttons_frame = tk.Frame(self.root, bg="SystemButtonFace")
        buttons_frame.pack(pady=20)

        tk.Button(buttons_frame, text="Parcial 1", bg="#4CAF50", fg="white",
                  font=("Arial", 12, "bold"), width=15, height=2,
                  command=lambda: self.open_partial(1)).pack(pady=10)

        tk.Button(buttons_frame, text="Parcial 2", bg="#2196F3", fg="white",
                  font=("Arial", 12, "bold"), width=15, height=2,
                  command=lambda: self.open_partial(2)).pack(pady=10)

        tk.Button(buttons_frame, text="Parcial 3", bg="#FF9800", fg="white",
                  font=("Arial", 12, "bold"), width=15, height=2,
                  command=lambda: self.open_partial(3)).pack(pady=10)

        tk.Button(self.root, text="Cerrar Sesión", bg="#FF0000", fg="white", font=("Arial", 12),
                  command=self.root.destroy).pack(pady=30)

    def open_partial(self, partial_num):
        """Abre la ventana del parcial específico."""
        try:
            if partial_num == 1:
                import parcial1
                parcial1.main()
            elif partial_num == 2:
                import parcial2
                parcial2.main()
            elif partial_num == 3:
                import parcial3
                parcial3.main()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el parcial: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    # Ejemplo de uso
    app = DashboardApp(root, "Usuario Prueba", "prueba@example.com")
    root.mainloop()
