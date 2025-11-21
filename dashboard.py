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
    """Reemplazo del dashboard por el menú principal.

    Esta clase actúa como adaptador: al iniciarse abre la ventana
    de `menu_principal.MenuPrincipal` en lugar de la UI anterior.
    """
    def __init__(self, root, username, email=None):
        self.root = root
        self.username = username
        self.email = email

        # Inicializar y delegar en menu_principal
        try:
            from menu_principal import MenuPrincipal
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo importar menu_principal: {e}")
            return

        # Destruir la root actual y crear una nueva ventana para el menú
        # para evitar conflictos con imágenes o referencias previas
        try:
            self.root.destroy()
        except Exception:
            pass

        new_root = tk.Tk()
        app = MenuPrincipal(new_root, username)
        new_root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    # Ejemplo de uso
    app = DashboardApp(root, "Usuario Prueba", "prueba@example.com")
    root.mainloop()
