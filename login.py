import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os
import sys
import re


def ruta_recurso(nombre_archivo):
    """Devuelve la ruta del archivo, compatible con PyInstaller."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, nombre_archivo)
    return os.path.join(os.path.abspath("."), nombre_archivo)


class LoginApp:
    def __init__(self, raoot):
        self.root = root
        self.root.title("Inicio de Sesión")
        self.root.geometry("800x500")
        self.root.resizable(False, False)

        # Fondo
        fondo_path = ruta_recurso("fondo_pc.jpeg")
        bg_image = Image.open(fondo_path)
        bg_image = bg_image.resize((800, 500))
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Frame principal
        frame = tk.Frame(self.root, bg="SystemButtonFace", bd=5)
        frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=300)

        tk.Label(frame, text="Iniciar Sesión", font=("Arial", 18, "bold"), bg="SystemButtonFace").pack(pady=10)

        tk.Label(frame, text="Usuario:", font=("Arial", 12), bg="SystemButtonFace").pack()
        self.email_entry = tk.Entry(frame, font=("Arial", 12))
        self.email_entry.pack(pady=5)

        tk.Label(frame, text="Contraseña:", font=("Arial", 12), bg="SystemButtonFace").pack()
        self.password_entry = tk.Entry(frame, font=("Arial", 12), show="*")
        self.password_entry.pack(pady=5)

        tk.Button(frame, text="Iniciar Sesión", bg="#FFA500", fg="white",
                  font=("Arial", 12, "bold"), command=self.login).pack(pady=10)

        tk.Button(frame, text="Registrarse", bg="#333", fg="white",
                  font=("Arial", 12), command=self.open_register_window).pack()

    def login(self):
        username = self.email_entry.get().strip()  # Ahora usa nombre de usuario
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos.")
            return

        usuarios_path = ruta_recurso("usuarios.json")
        if os.path.exists(usuarios_path):
            with open(usuarios_path, "r", encoding="utf-8") as f:
                users = json.load(f)
            
            if username in users and users[username]["password"] == password:
                user_email = users[username]["email"]
                messagebox.showinfo("Bienvenido", f"Inicio de sesión exitoso 🎉\nHola, {username}")
                self.open_dashboard(username, user_email)
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
        else:
            messagebox.showerror("Error", "No hay usuarios registrados.")

    def open_register_window(self):
        self.top = tk.Toplevel(self.root)
        self.top.title("Registro de Usuario")
        self.top.geometry("400x450")
        self.top.resizable(False, False)

        frame = tk.Frame(self.top, bg="SystemButtonFace", bd=5)
        frame.place(relx=0.5, rely=0.5, anchor="center", width=320, height=400)

        tk.Label(frame, text="Registro de Usuario", font=("Arial", 16, "bold"), bg="SystemButtonFace").pack(pady=10)

        tk.Label(frame, text="Nombre de Usuario:", font=("Arial", 12), bg="SystemButtonFace").pack()
        self.username = tk.Entry(frame, font=("Arial", 12))
        self.username.pack(pady=5)

        tk.Label(frame, text="Correo:", font=("Arial", 12), bg="SystemButtonFace").pack()
        self.email = tk.Entry(frame, font=("Arial", 12))
        self.email.pack(pady=5)

        tk.Label(frame, text="Contraseña:", font=("Arial", 12), bg="SystemButtonFace").pack()
        self.password = tk.Entry(frame, font=("Arial", 12), show="*")
        self.password.pack(pady=5)

        tk.Label(frame, text="Confirmar Contraseña:", font=("Arial", 12), bg="SystemButtonFace").pack()
        self.confirm = tk.Entry(frame, font=("Arial", 12), show="*")
        self.confirm.pack(pady=5)

        tk.Button(frame, text="Registrar", bg="#FFA500", fg="white", font=("Arial", 12, "bold"),
                  command=self.register).pack(pady=10)

    def register(self):
        username = self.username.get().strip()
        email = self.email.get().strip()
        password = self.password.get().strip()
        confirm = self.confirm.get().strip()

        if not username or not email or not password or not confirm:
            messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos.")
            return

        if password != confirm:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return

        # Validar formato de email
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            messagebox.showerror("Error", "Por favor ingresa un correo válido.")
            return

        usuarios_path = ruta_recurso("usuarios.json")
        users = {}
        if os.path.exists(usuarios_path):
            with open(usuarios_path, "r", encoding="utf-8") as f:
                users = json.load(f)

        # Verificar si el nombre de usuario ya existe
        if username in users:
            messagebox.showerror("Error", "Este nombre de usuario ya está registrado.")
            return

        # Verificar si el correo ya existe
        for user_data in users.values():
            if isinstance(user_data, dict) and user_data.get("email") == email:
                messagebox.showerror("Error", "Este correo ya está registrado.")
                return

        # Guardar usuario con nombre como identificador
        users[username] = {
            "email": email,
            "password": password
        }
        
        with open(usuarios_path, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=4)

        messagebox.showinfo("Éxito", f"Usuario {username} ({email}) registrado correctamente 🎉")
        self.top.destroy()

    def open_dashboard(self, username, email):
        """Cierra la ventana de login y abre el dashboard."""
        self.root.destroy()

        # Importar el dashboard
        from dashboard import DashboardApp
        
        dash = tk.Tk()
        app = DashboardApp(dash, username, email)
        dash.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
