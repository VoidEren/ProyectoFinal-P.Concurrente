import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os


class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inicio de Sesión")
        self.root.geometry("800x500")
        self.root.resizable(False, False)

        # Fondo
        bg_image = Image.open("fondo_pc.jpg")  # asegúrate que el archivo exista
        bg_image = bg_image.resize((800, 500))
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Frame principal
        frame = tk.Frame(self.root, bg="white", bd=5)
        frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=300)

        tk.Label(frame, text="Iniciar Sesión", font=("Arial", 18, "bold"), bg="white").pack(pady=10)

        tk.Label(frame, text="Correo:", font=("Arial", 12), bg="white").pack()
        self.email_entry = tk.Entry(frame, font=("Arial", 12))
        self.email_entry.pack(pady=5)

        tk.Label(frame, text="Contraseña:", font=("Arial", 12), bg="white").pack()
        self.password_entry = tk.Entry(frame, font=("Arial", 12), show="*")
        self.password_entry.pack(pady=5)

        tk.Button(frame, text="Iniciar Sesión", bg="#FFA500", fg="white",
                  font=("Arial", 12, "bold"), command=self.login).pack(pady=10)

        tk.Button(frame, text="Registrarse", bg="#333", fg="white",
                  font=("Arial", 12), command=self.open_register_window).pack()

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:
            messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos.")
            return

        if os.path.exists("usuarios.json"):
            with open("usuarios.json", "r") as f:
                users = json.load(f)
            if email in users and users[email] == password:
                messagebox.showinfo("Bienvenido", f"Inicio de sesión exitoso 🎉\nHola, {email}")
                self.open_dashboard(email)
            else:
                messagebox.showerror("Error", "Correo o contraseña incorrectos.")
        else:
            messagebox.showerror("Error", "No hay usuarios registrados.")

    def open_register_window(self):
        self.top = tk.Toplevel(self.root)
        self.top.title("Registro de Usuario")
        self.top.geometry("400x350")
        self.top.resizable(False, False)

        frame = tk.Frame(self.top, bg="white", bd=5)
        frame.place(relx=0.5, rely=0.5, anchor="center", width=320, height=300)

        tk.Label(frame, text="Registro de Usuario", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

        tk.Label(frame, text="Correo:", font=("Arial", 12), bg="white").pack()
        self.email = tk.Entry(frame, font=("Arial", 12))
        self.email.pack(pady=5)

        tk.Label(frame, text="Contraseña:", font=("Arial", 12), bg="white").pack()
        self.password = tk.Entry(frame, font=("Arial", 12), show="*")
        self.password.pack(pady=5)

        tk.Label(frame, text="Confirmar Contraseña:", font=("Arial", 12), bg="white").pack()
        self.confirm = tk.Entry(frame, font=("Arial", 12), show="*")
        self.confirm.pack(pady=5)

        tk.Button(frame, text="Registrar", bg="#FFA500", fg="white", font=("Arial", 12, "bold"),
                  command=self.register).pack(pady=10)

    def register(self):
        email = self.email.get().strip()
        password = self.password.get().strip()
        confirm = self.confirm.get().strip()

        if not email or not password or not confirm:
            messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos.")
            return

        if password != confirm:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return

        users = {}
        if os.path.exists("usuarios.json"):
            with open("usuarios.json", "r") as f:
                users = json.load(f)

        if email in users:
            messagebox.showerror("Error", "Este correo ya está registrado.")
            return

        users[email] = password
        with open("usuarios.json", "w") as f:
            json.dump(users, f)

        messagebox.showinfo("Éxito", f"Usuario {email} registrado correctamente 🎉")
        self.top.destroy()

    def open_dashboard(self, email):
        """Cierra la ventana de login y abre el dashboard."""
        self.root.destroy()

        dash = tk.Tk()
        dash.title("Dashboard Principal")
        dash.geometry("800x500")
        dash.resizable(False, False)

        # Fondo para dashboard
        bg_image = Image.open("kareli.jpg")
        bg_image = bg_image.resize((800, 500))
        bg_photo = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(dash, image=bg_photo)
        bg_label.image = bg_photo  # evitar que se borre el fondo por el recolector de basura
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        tk.Label(dash, text=f"Bienvenido al Menú Principal, {email}",
                 font=("Arial", 18, "bold"), bg="white").pack(pady=50)

        tk.Button(dash, text="Cerrar Sesión", bg="#FF0000", fg="white", font=("Arial", 12),
                  command=dash.destroy).pack(pady=20)

        dash.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
