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


def ruta_datos(nombre_archivo):
    """Devuelve una ruta escribible para guardar datos del usuario.
    - Si la app está congelada por PyInstaller, devuelve la carpeta del ejecutable.
    - Si no, devuelve la ruta en el directorio actual del proyecto.
    Se asegura de que el directorio exista.
    """
    if getattr(sys, 'frozen', False):
        # Intentar determinar la carpeta donde está el ejecutable real.
        # En un bundle --onefile, el proceso se extrae a un directorio temporal
        # (sys.executable apunta al ejecutable temporal). Sin embargo, a menudo
        # `sys.argv[0]` contiene la ruta original del .exe que el usuario ejecutó.
        # Si `sys.argv[0]` apunta a un directorio distinto del temp, lo usaremos.
        try:
            import tempfile
            tempdir = os.path.normcase(tempfile.gettempdir())
            candidate = os.path.abspath(sys.argv[0])
            candidate_dir = os.path.normcase(os.path.dirname(candidate))

            # Si candidate_dir parece estar dentro del temp, fallback a sys.executable
            if tempdir and os.path.commonpath([candidate_dir, tempdir]) == tempdir:
                base_dir = os.path.dirname(sys.executable)
            else:
                base_dir = candidate_dir
        except Exception:
            base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.abspath('.')

    # Asegurar que el directorio exista (si es necesario crear subcarpetas, hacerlo aquí)
    try:
        os.makedirs(base_dir, exist_ok=True)
    except Exception:
        pass

    path = os.path.join(base_dir, nombre_archivo)
    return path


class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inicio de Sesión")
        self.root.geometry("800x500")
        self.root.resizable(False, False)

        # Fondo
        fondo_path = ruta_recurso("fondo_pc.jpg")
        bg_image = Image.open(fondo_path)
        bg_image = bg_image.resize((800, 500))
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Frame principal
        frame = tk.Frame(self.root, bg="SystemButtonFace", bd=5)
        frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=300)

        tk.Label(frame, text="Iniciar Sesión", font=("Arial", 18, "bold"), bg="SystemButtonFace").pack(pady=10)

        tk.Label(frame, text="Correo:", font=("Arial", 12), bg="SystemButtonFace").pack()
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
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:
            messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos.")
            return

        # Leer usuarios: preferir archivo escribible en ruta_datos, si no existe usar recurso del bundle
        datos_path = ruta_datos("usuarios.json")
        if os.path.exists(datos_path):
            usuarios_path = datos_path
        else:
            usuarios_path = ruta_recurso("usuarios.json")

        if not os.path.exists(usuarios_path):
            messagebox.showerror("Error", "No hay usuarios registrados.")
            return

        with open(usuarios_path, "r", encoding="utf-8") as f:
            users = json.load(f)

        # Buscar usuario por correo
        found_username = None
        for uname, udata in users.items():
            if isinstance(udata, dict) and udata.get("email") == email:
                if udata.get("password") == password:
                    found_username = uname
                break

        if found_username:
            messagebox.showinfo("Inicio de sesión", f"Inicio de sesión exitoso 🎉\nBienvenido, {found_username}")
            self.open_dashboard(found_username, email)
        else:
            messagebox.showerror("Error", "Correo o contraseña incorrectos.")

    def open_register_window(self):
        self.top = tk.Toplevel(self.root)
        self.top.title("Registro de Usuario")
        self.top.geometry("400x520")
        self.top.resizable(False, False)

        frame = tk.Frame(self.top, bg="SystemButtonFace", bd=5)
        frame.place(relx=0.5, rely=0.5, anchor="center", width=320, height=470)

        tk.Label(frame, text="Registro de Usuario", font=("Arial", 16, "bold"), bg="SystemButtonFace").pack(pady=10)

        tk.Label(frame, text="Nombre de Usuario:", font=("Arial", 12), bg="SystemButtonFace").pack()
        self.username = tk.Entry(frame, font=("Arial", 12))
        self.username.pack(pady=5)

        tk.Label(frame, text="Correo:", font=("Arial", 12), bg="SystemButtonFace").pack()
        self.email = tk.Entry(frame, font=("Arial", 12))
        self.email.pack(pady=5)

        tk.Label(frame, text="Matrícula:", font=("Arial", 12), bg="SystemButtonFace").pack()
        self.matricula = tk.Entry(frame, font=("Arial", 12))
        self.matricula.pack(pady=5)

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
        matricula = self.matricula.get().strip()
        password = self.password.get().strip()
        confirm = self.confirm.get().strip()

        if not username or not email or not matricula or not password or not confirm:
            messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos.")
            return

        if password != confirm:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return

        # Validar formato de email
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            messagebox.showerror("Error", "Por favor ingresa un correo válido.")
            return

        # Preferir archivo escribible en ruta_datos para registro (especialmente cuando está frozen)
        datos_path = ruta_datos("usuarios.json")
        # Si existe un archivo en la ruta de datos, úsalo; si no, intenta leer el recurso del bundle
        if os.path.exists(datos_path):
            usuarios_path = datos_path
        else:
            usuarios_path = ruta_recurso("usuarios.json")

        users = {}
        if os.path.exists(usuarios_path):
            with open(usuarios_path, "r", encoding="utf-8") as f:
                try:
                    users = json.load(f)
                except Exception:
                    users = {}

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
            "matricula": matricula,
            "password": password
        }
        
        # Siempre escribir al archivo de datos (crearlo en la ruta escribible)
        with open(datos_path, "w", encoding="utf-8") as f:
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
