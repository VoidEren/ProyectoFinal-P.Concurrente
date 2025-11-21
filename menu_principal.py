import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import sys
import json
from pdf2image import convert_from_path


def ruta_recurso(nombre_archivo):
    """Devuelve la ruta del archivo, compatible con PyInstaller."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, nombre_archivo)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, nombre_archivo)


class MenuPrincipal:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title("Programación Concurrente - Menú Principal")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        
        # Fondo
        self.root.configure(bg="#1a1a2e")
        
        # Título
        title_frame = tk.Frame(self.root, bg="#16213e")
        title_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(title_frame, text=f"Bienvenido {username}", 
                font=("Arial", 20, "bold"), bg="#16213e", fg="white").pack(pady=10)
        tk.Label(title_frame, text="Programación Concurrente", 
                font=("Arial", 16), bg="#16213e", fg="#0f3460").pack()
        
        # Frame principal con scroll
        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Botones de menús
        self.crear_botones_menu(main_frame)
    
    def crear_botones_menu(self, parent):
        """Crea los botones del menú principal"""
        menus = [
            ("📚 Documentación", self.abrir_documentacion),
            ("🧵 Hilos", self.abrir_hilos),
            ("🔌 Sockets", self.abrir_sockets),
            ("🚦 Semáforos", self.abrir_semaforos),
            ("🎨 Patrones", self.abrir_patrones),
            ("❓ Ayuda", self.abrir_ayuda),
            ("❌ Salir", self.salir),
        ]
        
        for texto, comando in menus:
            btn = tk.Button(parent, text=texto, font=("Arial", 14, "bold"),
                           bg="#0f3460", fg="white", height=2, relief=tk.FLAT,
                           command=comando)
            btn.pack(fill=tk.X, pady=10)
            # Efecto hover
            btn.bind("<Enter>", lambda e: e.widget.config(bg="#e94560"))
            btn.bind("<Leave>", lambda e: e.widget.config(bg="#0f3460"))
    
    def abrir_documentacion(self):
        """Abre el menú de documentación"""
        self.crear_submenu("Documentación", [
            ("Introducción de Concurrencia", self.vista_previa_pdf_introduccion),
            ("Diferencia entre Programacion concurrente y secuencial", self.vista_previa_pdf_diferencial),
            ("Problemas y patologias", self.vista_previa_pdf_patologias),
            ("Conceptos de Programación Concurrente Sockets", self.vista_previa_pdf_sockets),
            ("Conceptos de Programación Concurrente Sockets con UDP y TCP",self.vista_previa_pdf_socketsyutp),
            ("Coordinación, Colaboración, CDirecta, CIndirecta, etc. y Semáforos",self.vista_previa_pdf_ccccysemaforos),
            ("Tkinter", self.vista_previa_pdf_tkinter),
            ("Patron productor-consumidor", self.vista_previa_pdf_patronconsumidor),
            ("Patrones de futuro (Future) y promesa (Promess)", self.vista_previa_pdf_patronesfuturenpromess),
            ("Patrón de El Modelo de Actores ", self.vista_previa_pdf_actores)
        ])

    def vista_previa_pdf_introduccion(self):
        """Muestra una ventana con el PDF de introducción a concurrencia usando pdf2image"""
        # Obtener ruta absoluta del PDF
        script_dir = os.path.dirname(os.path.abspath(__file__))
        pdf_path = os.path.join(script_dir, "Apuntes", "Apunte_1-1.pdf")
        
        if not os.path.exists(pdf_path):
            messagebox.showerror("Error", f"No se encontró el PDF: {pdf_path}")
            return
        
        try:
            preview_win = tk.Toplevel(self.root)
            preview_win.title("Visualizador PDF - Introducción de Concurrencia")
            preview_win.geometry("900x1000")
            preview_win.configure(bg="#1a1a2e")
            
            # Convertir todas las páginas del PDF a imágenes
            pages = convert_from_path(pdf_path, dpi=150)
            
            if not pages:
                messagebox.showerror("Error", "No se pudo convertir el PDF a imágenes.")
                return
            
            # Frame principal con barra de navegación
            top_frame = tk.Frame(preview_win, bg="#16213e")
            top_frame.pack(fill=tk.X, padx=10, pady=10)
            
            # Variable para rastrear página actual
            self.current_page = [0]
            self.total_pages = [len(pages)]

            # Preparar canvas con scrollbars para mostrar la página completa
            canvas_frame = tk.Frame(preview_win, bg="#1a1a2e")
            canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            canvas = tk.Canvas(canvas_frame, bg="white")
            v_scroll = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
            h_scroll = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=canvas.xview)
            canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
            v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
            h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Escalar cada página al ancho objetivo para que se vea completa
            target_width = 860
            self.photo_images = []
            self.raw_sizes = []
            for page in pages:
                w, h = page.size
                scale = min(1.0, target_width / w)
                new_w = int(w * scale)
                new_h = int(h * scale)
                resized = page.resize((new_w, new_h), Image.LANCZOS)
                self.photo_images.append(ImageTk.PhotoImage(resized))
                self.raw_sizes.append((new_w, new_h))

            # Crear un item en el canvas para la imagen actual
            img_container = canvas.create_image(0, 0, anchor='nw', image=self.photo_images[0])
            canvas.config(scrollregion=(0, 0, self.raw_sizes[0][0], self.raw_sizes[0][1]))

            # Función para mostrar página (ajusta scrollregion)
            def show_page(page_num):
                if 0 <= page_num < len(self.photo_images):
                    canvas.itemconfig(img_container, image=self.photo_images[page_num])
                    canvas.config(scrollregion=(0, 0, self.raw_sizes[page_num][0], self.raw_sizes[page_num][1]))
                    self.current_page[0] = page_num
                    page_label.config(text=f"Página {page_num + 1} de {self.total_pages[0]}")
                    canvas.xview_moveto(0)
                    canvas.yview_moveto(0)
            
            # Botones de navegación
            btn_frame = tk.Frame(top_frame, bg="#16213e")
            btn_frame.pack(fill=tk.X, pady=10)
            
            btn_prev = tk.Button(btn_frame, text="◀ Anterior", command=lambda: show_page(self.current_page[0] - 1),
                                bg="#0f3460", fg="white", font=("Arial", 10, "bold"))
            btn_prev.pack(side=tk.LEFT, padx=5)
            
            page_label = tk.Label(top_frame, text=f"Página 1 de {self.total_pages[0]}", 
                                 font=("Arial", 10), bg="#16213e", fg="white")
            page_label.pack(side=tk.LEFT, padx=20)
            
            btn_next = tk.Button(btn_frame, text="Siguiente ▶", command=lambda: show_page(self.current_page[0] + 1),
                                bg="#0f3460", fg="white", font=("Arial", 10, "bold"))
            btn_next.pack(side=tk.LEFT, padx=5)
            
            # Mostrar la primera página
            show_page(0)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar el PDF: {str(e)}")

    def vista_previa_pdf_diferencial(self):
        """Muestra una ventana con el PDF de introducción a concurrencia usando pdf2image"""
        # Obtener ruta absoluta del PDF
        script_dir = os.path.dirname(os.path.abspath(__file__))
        pdf_path = os.path.join(script_dir, "Apuntes", "Apunte_1-2.pdf")
        
        if not os.path.exists(pdf_path):
            messagebox.showerror("Error", f"No se encontró el PDF: {pdf_path}")
            return
        
        try:
            preview_win = tk.Toplevel(self.root)
            preview_win.title("Visualizador PDF - Introducción de Concurrencia")
            preview_win.geometry("900x1000")
            preview_win.configure(bg="#1a1a2e")
            
            # Convertir todas las páginas del PDF a imágenes
            pages = convert_from_path(pdf_path, dpi=150)
            
            if not pages:
                messagebox.showerror("Error", "No se pudo convertir el PDF a imágenes.")
                return
            
            # Frame principal con barra de navegación
            top_frame = tk.Frame(preview_win, bg="#16213e")
            top_frame.pack(fill=tk.X, padx=10, pady=10)
            
            # Variable para rastrear página actual
            self.current_page = [0]
            self.total_pages = [len(pages)]

            # Preparar canvas con scrollbars para mostrar la página completa
            canvas_frame = tk.Frame(preview_win, bg="#1a1a2e")
            canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            canvas = tk.Canvas(canvas_frame, bg="white")
            v_scroll = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
            h_scroll = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=canvas.xview)
            canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
            v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
            h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Escalar cada página al ancho objetivo para que se vea completa
            target_width = 860
            self.photo_images = []
            self.raw_sizes = []
            for page in pages:
                w, h = page.size
                scale = min(1.0, target_width / w)
                new_w = int(w * scale)
                new_h = int(h * scale)
                resized = page.resize((new_w, new_h), Image.LANCZOS)
                self.photo_images.append(ImageTk.PhotoImage(resized))
                self.raw_sizes.append((new_w, new_h))

            # Crear un item en el canvas para la imagen actual
            img_container = canvas.create_image(0, 0, anchor='nw', image=self.photo_images[0])
            canvas.config(scrollregion=(0, 0, self.raw_sizes[0][0], self.raw_sizes[0][1]))

            # Función para mostrar página (ajusta scrollregion)
            def show_page(page_num):
                if 0 <= page_num < len(self.photo_images):
                    canvas.itemconfig(img_container, image=self.photo_images[page_num])
                    canvas.config(scrollregion=(0, 0, self.raw_sizes[page_num][0], self.raw_sizes[page_num][1]))
                    self.current_page[0] = page_num
                    page_label.config(text=f"Página {page_num + 1} de {self.total_pages[0]}")
                    canvas.xview_moveto(0)
                    canvas.yview_moveto(0)
            
            # Botones de navegación
            btn_frame = tk.Frame(top_frame, bg="#16213e")
            btn_frame.pack(fill=tk.X, pady=10)
            
            btn_prev = tk.Button(btn_frame, text="◀ Anterior", command=lambda: show_page(self.current_page[0] - 1),
                                bg="#0f3460", fg="white", font=("Arial", 10, "bold"))
            btn_prev.pack(side=tk.LEFT, padx=5)
            
            page_label = tk.Label(top_frame, text=f"Página 1 de {self.total_pages[0]}", 
                                 font=("Arial", 10), bg="#16213e", fg="white")
            page_label.pack(side=tk.LEFT, padx=20)
            
            btn_next = tk.Button(btn_frame, text="Siguiente ▶", command=lambda: show_page(self.current_page[0] + 1),
                                bg="#0f3460", fg="white", font=("Arial", 10, "bold"))
            btn_next.pack(side=tk.LEFT, padx=5)
            
            # Mostrar la primera página
            show_page(0)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar el PDF: {str(e)}")

    def vista_previa_pdf_patologias(self):
        """Muestra una ventana con el PDF de introducción a concurrencia usando pdf2image"""
        # Obtener ruta absoluta del PDF
        script_dir = os.path.dirname(os.path.abspath(__file__))
        pdf_path = os.path.join(script_dir, "Apuntes", "Apunte_1-3.pdf")
        
        if not os.path.exists(pdf_path):
            messagebox.showerror("Error", f"No se encontró el PDF: {pdf_path}")
            return
        
        try:
            preview_win = tk.Toplevel(self.root)
            preview_win.title("Visualizador PDF - Introducción de Concurrencia")
            preview_win.geometry("900x1000")
            preview_win.configure(bg="#1a1a2e")
            
            # Convertir todas las páginas del PDF a imágenes
            pages = convert_from_path(pdf_path, dpi=150)
            
            if not pages:
                messagebox.showerror("Error", "No se pudo convertir el PDF a imágenes.")
                return
            
            # Frame principal con barra de navegación
            top_frame = tk.Frame(preview_win, bg="#16213e")
            top_frame.pack(fill=tk.X, padx=10, pady=10)
            
            # Variable para rastrear página actual
            self.current_page = [0]
            self.total_pages = [len(pages)]

            # Preparar canvas con scrollbars para mostrar la página completa
            canvas_frame = tk.Frame(preview_win, bg="#1a1a2e")
            canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            canvas = tk.Canvas(canvas_frame, bg="white")
            v_scroll = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
            h_scroll = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=canvas.xview)
            canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
            v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
            h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Escalar cada página al ancho objetivo para que se vea completa
            target_width = 860
            self.photo_images = []
            self.raw_sizes = []
            for page in pages:
                w, h = page.size
                scale = min(1.0, target_width / w)
                new_w = int(w * scale)
                new_h = int(h * scale)
                resized = page.resize((new_w, new_h), Image.LANCZOS)
                self.photo_images.append(ImageTk.PhotoImage(resized))
                self.raw_sizes.append((new_w, new_h))

            # Crear un item en el canvas para la imagen actual
            img_container = canvas.create_image(0, 0, anchor='nw', image=self.photo_images[0])
            canvas.config(scrollregion=(0, 0, self.raw_sizes[0][0], self.raw_sizes[0][1]))

            # Función para mostrar página (ajusta scrollregion)
            def show_page(page_num):
                if 0 <= page_num < len(self.photo_images):
                    canvas.itemconfig(img_container, image=self.photo_images[page_num])
                    canvas.config(scrollregion=(0, 0, self.raw_sizes[page_num][0], self.raw_sizes[page_num][1]))
                    self.current_page[0] = page_num
                    page_label.config(text=f"Página {page_num + 1} de {self.total_pages[0]}")
                    canvas.xview_moveto(0)
                    canvas.yview_moveto(0)
            
            # Botones de navegación
            btn_frame = tk.Frame(top_frame, bg="#16213e")
            btn_frame.pack(fill=tk.X, pady=10)
            
            btn_prev = tk.Button(btn_frame, text="◀ Anterior", command=lambda: show_page(self.current_page[0] - 1),
                                bg="#0f3460", fg="white", font=("Arial", 10, "bold"))
            btn_prev.pack(side=tk.LEFT, padx=5)
            
            page_label = tk.Label(top_frame, text=f"Página 1 de {self.total_pages[0]}", 
                                 font=("Arial", 10), bg="#16213e", fg="white")
            page_label.pack(side=tk.LEFT, padx=20)
            
            btn_next = tk.Button(btn_frame, text="Siguiente ▶", command=lambda: show_page(self.current_page[0] + 1),
                                bg="#0f3460", fg="white", font=("Arial", 10, "bold"))
            btn_next.pack(side=tk.LEFT, padx=5)
            
            # Mostrar la primera página
            show_page(0)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar el PDF: {str(e)}")
    
    def vista_previa_pdf_sockets(self):
        """Muestra una ventana con el PDF de introducción a concurrencia usando pdf2image"""
        # Obtener ruta absoluta del PDF
        script_dir = os.path.dirname(os.path.abspath(__file__))
        pdf_path = os.path.join(script_dir, "Apuntes", "Apunte_1-4.pdf")
        
        if not os.path.exists(pdf_path):
            messagebox.showerror("Error", f"No se encontró el PDF: {pdf_path}")
            return
        
        try:
            preview_win = tk.Toplevel(self.root)
            preview_win.title("Visualizador PDF - Introducción de Concurrencia")
            preview_win.geometry("900x1000")
            preview_win.configure(bg="#1a1a2e")
            
            # Convertir todas las páginas del PDF a imágenes
            pages = convert_from_path(pdf_path, dpi=150)
            
            if not pages:
                messagebox.showerror("Error", "No se pudo convertir el PDF a imágenes.")
                return
            
            # Frame principal con barra de navegación
            top_frame = tk.Frame(preview_win, bg="#16213e")
            top_frame.pack(fill=tk.X, padx=10, pady=10)
            
            # Variable para rastrear página actual
            self.current_page = [0]
            self.total_pages = [len(pages)]

            # Preparar canvas con scrollbars para mostrar la página completa
            canvas_frame = tk.Frame(preview_win, bg="#1a1a2e")
            canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            canvas = tk.Canvas(canvas_frame, bg="white")
            v_scroll = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
            h_scroll = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=canvas.xview)
            canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
            v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
            h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Escalar cada página al ancho objetivo para que se vea completa
            target_width = 860
            self.photo_images = []
            self.raw_sizes = []
            for page in pages:
                w, h = page.size
                scale = min(1.0, target_width / w)
                new_w = int(w * scale)
                new_h = int(h * scale)
                resized = page.resize((new_w, new_h), Image.LANCZOS)
                self.photo_images.append(ImageTk.PhotoImage(resized))
                self.raw_sizes.append((new_w, new_h))

            # Crear un item en el canvas para la imagen actual
            img_container = canvas.create_image(0, 0, anchor='nw', image=self.photo_images[0])
            canvas.config(scrollregion=(0, 0, self.raw_sizes[0][0], self.raw_sizes[0][1]))

            # Función para mostrar página (ajusta scrollregion)
            def show_page(page_num):
                if 0 <= page_num < len(self.photo_images):
                    canvas.itemconfig(img_container, image=self.photo_images[page_num])
                    canvas.config(scrollregion=(0, 0, self.raw_sizes[page_num][0], self.raw_sizes[page_num][1]))
                    self.current_page[0] = page_num
                    page_label.config(text=f"Página {page_num + 1} de {self.total_pages[0]}")
                    canvas.xview_moveto(0)
                    canvas.yview_moveto(0)
            
            # Botones de navegación
            btn_frame = tk.Frame(top_frame, bg="#16213e")
            btn_frame.pack(fill=tk.X, pady=10)
            
            btn_prev = tk.Button(btn_frame, text="◀ Anterior", command=lambda: show_page(self.current_page[0] - 1),
                                bg="#0f3460", fg="white", font=("Arial", 10, "bold"))
            btn_prev.pack(side=tk.LEFT, padx=5)
            
            page_label = tk.Label(top_frame, text=f"Página 1 de {self.total_pages[0]}", 
                                 font=("Arial", 10), bg="#16213e", fg="white")
            page_label.pack(side=tk.LEFT, padx=20)
            
            btn_next = tk.Button(btn_frame, text="Siguiente ▶", command=lambda: show_page(self.current_page[0] + 1),
                                bg="#0f3460", fg="white", font=("Arial", 10, "bold"))
            btn_next.pack(side=tk.LEFT, padx=5)
            
            # Mostrar la primera página
            show_page(0)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar el PDF: {str(e)}")

    def vista_previa_pdf_socketsyutp(self):
        """Muestra una ventana con el PDF de introducción a concurrencia usando pdf2image"""
        # Obtener ruta absoluta del PDF
        script_dir = os.path.dirname(os.path.abspath(__file__))
        pdf_path = os.path.join(script_dir, "Apuntes", "Apunte_1-5.pdf")
        
        if not os.path.exists(pdf_path):
            messagebox.showerror("Error", f"No se encontró el PDF: {pdf_path}")
            return
        
        try:
            preview_win = tk.Toplevel(self.root)
            preview_win.title("Visualizador PDF - Introducción de Concurrencia")
            preview_win.geometry("900x1000")
            preview_win.configure(bg="#1a1a2e")
            
            # Convertir todas las páginas del PDF a imágenes
            pages = convert_from_path(pdf_path, dpi=150)
            
            if not pages:
                messagebox.showerror("Error", "No se pudo convertir el PDF a imágenes.")
                return
            
            # Frame principal con barra de navegación
            top_frame = tk.Frame(preview_win, bg="#16213e")
            top_frame.pack(fill=tk.X, padx=10, pady=10)
            
            # Variable para rastrear página actual
            self.current_page = [0]
            self.total_pages = [len(pages)]

            # Preparar canvas con scrollbars para mostrar la página completa
            canvas_frame = tk.Frame(preview_win, bg="#1a1a2e")
            canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            canvas = tk.Canvas(canvas_frame, bg="white")
            v_scroll = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
            h_scroll = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=canvas.xview)
            canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
            v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
            h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Escalar cada página al ancho objetivo para que se vea completa
            target_width = 860
            self.photo_images = []
            self.raw_sizes = []
            for page in pages:
                w, h = page.size
                scale = min(1.0, target_width / w)
                new_w = int(w * scale)
                new_h = int(h * scale)
                resized = page.resize((new_w, new_h), Image.LANCZOS)
                self.photo_images.append(ImageTk.PhotoImage(resized))
                self.raw_sizes.append((new_w, new_h))

            # Crear un item en el canvas para la imagen actual
            img_container = canvas.create_image(0, 0, anchor='nw', image=self.photo_images[0])
            canvas.config(scrollregion=(0, 0, self.raw_sizes[0][0], self.raw_sizes[0][1]))

            # Función para mostrar página (ajusta scrollregion)
            def show_page(page_num):
                if 0 <= page_num < len(self.photo_images):
                    canvas.itemconfig(img_container, image=self.photo_images[page_num])
                    canvas.config(scrollregion=(0, 0, self.raw_sizes[page_num][0], self.raw_sizes[page_num][1]))
                    self.current_page[0] = page_num
                    page_label.config(text=f"Página {page_num + 1} de {self.total_pages[0]}")
                    canvas.xview_moveto(0)
                    canvas.yview_moveto(0)
            
            # Botones de navegación
            btn_frame = tk.Frame(top_frame, bg="#16213e")
            btn_frame.pack(fill=tk.X, pady=10)
            
            btn_prev = tk.Button(btn_frame, text="◀ Anterior", command=lambda: show_page(self.current_page[0] - 1),
                                bg="#0f3460", fg="white", font=("Arial", 10, "bold"))
            btn_prev.pack(side=tk.LEFT, padx=5)
            
            page_label = tk.Label(top_frame, text=f"Página 1 de {self.total_pages[0]}", 
                                 font=("Arial", 10), bg="#16213e", fg="white")
            page_label.pack(side=tk.LEFT, padx=20)
            
            btn_next = tk.Button(btn_frame, text="Siguiente ▶", command=lambda: show_page(self.current_page[0] + 1),
                                bg="#0f3460", fg="white", font=("Arial", 10, "bold"))
            btn_next.pack(side=tk.LEFT, padx=5)
            
            # Mostrar la primera página
            show_page(0)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar el PDF: {str(e)}")

    def vista_previa_pdf_ccccysemaforos(self):
        """Muestra una ventana con el PDF de introducción a concurrencia usando pdf2image"""
        # Obtener ruta absoluta del PDF
        script_dir = os.path.dirname(os.path.abspath(__file__))
        pdf_path = os.path.join(script_dir, "Apuntes", "Apunte_2-1.pdf")
        
        if not os.path.exists(pdf_path):
            messagebox.showerror("Error", f"No se encontró el PDF: {pdf_path}")
            return
        
        try:
            preview_win = tk.Toplevel(self.root)
            preview_win.title("Visualizador PDF - Introducción de Concurrencia")
            preview_win.geometry("900x1000")
            preview_win.configure(bg="#1a1a2e")
            
            # Convertir todas las páginas del PDF a imágenes
            pages = convert_from_path(pdf_path, dpi=150)
            
            if not pages:
                messagebox.showerror("Error", "No se pudo convertir el PDF a imágenes.")
                return
            
            # Frame principal con barra de navegación
            top_frame = tk.Frame(preview_win, bg="#16213e")
            top_frame.pack(fill=tk.X, padx=10, pady=10)
            
            # Variable para rastrear página actual
            self.current_page = [0]
            self.total_pages = [len(pages)]

            # Preparar canvas con scrollbars para mostrar la página completa
            canvas_frame = tk.Frame(preview_win, bg="#1a1a2e")
            canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            canvas = tk.Canvas(canvas_frame, bg="white")
            v_scroll = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
            h_scroll = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=canvas.xview)
            canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
            v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
            h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Escalar cada página al ancho objetivo para que se vea completa
            target_width = 860
            self.photo_images = []
            self.raw_sizes = []
            for page in pages:
                w, h = page.size
                scale = min(1.0, target_width / w)
                new_w = int(w * scale)
                new_h = int(h * scale)
                resized = page.resize((new_w, new_h), Image.LANCZOS)
                self.photo_images.append(ImageTk.PhotoImage(resized))
                self.raw_sizes.append((new_w, new_h))

            # Crear un item en el canvas para la imagen actual
            img_container = canvas.create_image(0, 0, anchor='nw', image=self.photo_images[0])
            canvas.config(scrollregion=(0, 0, self.raw_sizes[0][0], self.raw_sizes[0][1]))

            # Función para mostrar página (ajusta scrollregion)
            def show_page(page_num):
                if 0 <= page_num < len(self.photo_images):
                    canvas.itemconfig(img_container, image=self.photo_images[page_num])
                    canvas.config(scrollregion=(0, 0, self.raw_sizes[page_num][0], self.raw_sizes[page_num][1]))
                    self.current_page[0] = page_num
                    page_label.config(text=f"Página {page_num + 1} de {self.total_pages[0]}")
                    canvas.xview_moveto(0)
                    canvas.yview_moveto(0)
            
            # Botones de navegación
            btn_frame = tk.Frame(top_frame, bg="#16213e")
            btn_frame.pack(fill=tk.X, pady=10)
            
            btn_prev = tk.Button(btn_frame, text="◀ Anterior", command=lambda: show_page(self.current_page[0] - 1),
                                bg="#0f3460", fg="white", font=("Arial", 10, "bold"))
            btn_prev.pack(side=tk.LEFT, padx=5)
            
            page_label = tk.Label(top_frame, text=f"Página 1 de {self.total_pages[0]}", 
                                 font=("Arial", 10), bg="#16213e", fg="white")
            page_label.pack(side=tk.LEFT, padx=20)
            
            btn_next = tk.Button(btn_frame, text="Siguiente ▶", command=lambda: show_page(self.current_page[0] + 1),
                                bg="#0f3460", fg="white", font=("Arial", 10, "bold"))
            btn_next.pack(side=tk.LEFT, padx=5)
            
            # Mostrar la primera página
            show_page(0)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar el PDF: {str(e)}")

    def vista_previa_pdf_patronconsumidor(self):
        """Muestra una ventana con el PDF de introducción a concurrencia usando pdf2image"""
        # Obtener ruta absoluta del PDF
        script_dir = os.path.dirname(os.path.abspath(__file__))
        pdf_path = os.path.join(script_dir, "Apuntes", "Apunte_2-3.pdf")
        
        if not os.path.exists(pdf_path):
            messagebox.showerror("Error", f"No se encontró el PDF: {pdf_path}")
            return
        
        try:
            preview_win = tk.Toplevel(self.root)
            preview_win.title("Visualizador PDF - Introducción de Concurrencia")
            preview_win.geometry("900x1000")
            preview_win.configure(bg="#1a1a2e")
            
            # Convertir todas las páginas del PDF a imágenes
            pages = convert_from_path(pdf_path, dpi=150)
            
            if not pages:
                messagebox.showerror("Error", "No se pudo convertir el PDF a imágenes.")
                return
            
            # Frame principal con barra de navegación
            top_frame = tk.Frame(preview_win, bg="#16213e")
            top_frame.pack(fill=tk.X, padx=10, pady=10)
            
            # Variable para rastrear página actual
            self.current_page = [0]
            self.total_pages = [len(pages)]

            # Preparar canvas con scrollbars para mostrar la página completa
            canvas_frame = tk.Frame(preview_win, bg="#1a1a2e")
            canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            canvas = tk.Canvas(canvas_frame, bg="white")
            v_scroll = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
            h_scroll = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=canvas.xview)
            canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
            v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
            h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Escalar cada página al ancho objetivo para que se vea completa
            target_width = 860
            self.photo_images = []
            self.raw_sizes = []
            for page in pages:
                w, h = page.size
                scale = min(1.0, target_width / w)
                new_w = int(w * scale)
                new_h = int(h * scale)
                resized = page.resize((new_w, new_h), Image.LANCZOS)
                self.photo_images.append(ImageTk.PhotoImage(resized))
                self.raw_sizes.append((new_w, new_h))

            # Crear un item en el canvas para la imagen actual
            img_container = canvas.create_image(0, 0, anchor='nw', image=self.photo_images[0])
            canvas.config(scrollregion=(0, 0, self.raw_sizes[0][0], self.raw_sizes[0][1]))

            # Función para mostrar página (ajusta scrollregion)
            def show_page(page_num):
                if 0 <= page_num < len(self.photo_images):
                    canvas.itemconfig(img_container, image=self.photo_images[page_num])
                    canvas.config(scrollregion=(0, 0, self.raw_sizes[page_num][0], self.raw_sizes[page_num][1]))
                    self.current_page[0] = page_num
                    page_label.config(text=f"Página {page_num + 1} de {self.total_pages[0]}")
                    canvas.xview_moveto(0)
                    canvas.yview_moveto(0)
            
            # Botones de navegación
            btn_frame = tk.Frame(top_frame, bg="#16213e")
            btn_frame.pack(fill=tk.X, pady=10)
            
            btn_prev = tk.Button(btn_frame, text="◀ Anterior", command=lambda: show_page(self.current_page[0] - 1),
                                bg="#0f3460", fg="white", font=("Arial", 10, "bold"))
            btn_prev.pack(side=tk.LEFT, padx=5)
            
            page_label = tk.Label(top_frame, text=f"Página 1 de {self.total_pages[0]}", 
                                 font=("Arial", 10), bg="#16213e", fg="white")
            page_label.pack(side=tk.LEFT, padx=20)
            
            btn_next = tk.Button(btn_frame, text="Siguiente ▶", command=lambda: show_page(self.current_page[0] + 1),
                                bg="#0f3460", fg="white", font=("Arial", 10, "bold"))
            btn_next.pack(side=tk.LEFT, padx=5)
            
            # Mostrar la primera página
            show_page(0)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar el PDF: {str(e)}")

    def vista_previa_pdf_tkinter(self):
        """Muestra una ventana con el PDF de introducción a concurrencia usando pdf2image"""
        # Obtener ruta absoluta del PDF
        script_dir = os.path.dirname(os.path.abspath(__file__))
        pdf_path = os.path.join(script_dir, "Apuntes", "Apunte_2-2.pdf")
        
        if not os.path.exists(pdf_path):
            messagebox.showerror("Error", f"No se encontró el PDF: {pdf_path}")
            return
        
        try:
            preview_win = tk.Toplevel(self.root)
            preview_win.title("Visualizador PDF - Introducción de Concurrencia")
            preview_win.geometry("900x1000")
            preview_win.configure(bg="#1a1a2e")
            
            # Convertir todas las páginas del PDF a imágenes
            pages = convert_from_path(pdf_path, dpi=150)
            
            if not pages:
                messagebox.showerror("Error", "No se pudo convertir el PDF a imágenes.")
                return
            
            # Frame principal con barra de navegación
            top_frame = tk.Frame(preview_win, bg="#16213e")
            top_frame.pack(fill=tk.X, padx=10, pady=10)
            
            # Variable para rastrear página actual
            self.current_page = [0]
            self.total_pages = [len(pages)]

            # Preparar canvas con scrollbars para mostrar la página completa
            canvas_frame = tk.Frame(preview_win, bg="#1a1a2e")
            canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            canvas = tk.Canvas(canvas_frame, bg="white")
            v_scroll = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
            h_scroll = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=canvas.xview)
            canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
            v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
            h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Escalar cada página al ancho objetivo para que se vea completa
            target_width = 860
            self.photo_images = []
            self.raw_sizes = []
            for page in pages:
                w, h = page.size
                scale = min(1.0, target_width / w)
                new_w = int(w * scale)
                new_h = int(h * scale)
                resized = page.resize((new_w, new_h), Image.LANCZOS)
                self.photo_images.append(ImageTk.PhotoImage(resized))
                self.raw_sizes.append((new_w, new_h))

            # Crear un item en el canvas para la imagen actual
            img_container = canvas.create_image(0, 0, anchor='nw', image=self.photo_images[0])
            canvas.config(scrollregion=(0, 0, self.raw_sizes[0][0], self.raw_sizes[0][1]))

            # Función para mostrar página (ajusta scrollregion)
            def show_page(page_num):
                if 0 <= page_num < len(self.photo_images):
                    canvas.itemconfig(img_container, image=self.photo_images[page_num])
                    canvas.config(scrollregion=(0, 0, self.raw_sizes[page_num][0], self.raw_sizes[page_num][1]))
                    self.current_page[0] = page_num
                    page_label.config(text=f"Página {page_num + 1} de {self.total_pages[0]}")
                    canvas.xview_moveto(0)
                    canvas.yview_moveto(0)
            
            # Botones de navegación
            btn_frame = tk.Frame(top_frame, bg="#16213e")
            btn_frame.pack(fill=tk.X, pady=10)
            
            btn_prev = tk.Button(btn_frame, text="◀ Anterior", command=lambda: show_page(self.current_page[0] - 1),
                                bg="#0f3460", fg="white", font=("Arial", 10, "bold"))
            btn_prev.pack(side=tk.LEFT, padx=5)
            
            page_label = tk.Label(top_frame, text=f"Página 1 de {self.total_pages[0]}", 
                                 font=("Arial", 10), bg="#16213e", fg="white")
            page_label.pack(side=tk.LEFT, padx=20)
            
            btn_next = tk.Button(btn_frame, text="Siguiente ▶", command=lambda: show_page(self.current_page[0] + 1),
                                bg="#0f3460", fg="white", font=("Arial", 10, "bold"))
            btn_next.pack(side=tk.LEFT, padx=5)
            
            # Mostrar la primera página
            show_page(0)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar el PDF: {str(e)}")

    def vista_previa_pdf_patronesfuturenpromess(self):
        """Muestra una ventana con el PDF de introducción a concurrencia usando pdf2image"""
        # Obtener ruta absoluta del PDF
        script_dir = os.path.dirname(os.path.abspath(__file__))
        pdf_path = os.path.join(script_dir, "Apuntes", "Apunte_2-4.pdf")
        
        if not os.path.exists(pdf_path):
            messagebox.showerror("Error", f"No se encontró el PDF: {pdf_path}")
            return
        
        try:
            preview_win = tk.Toplevel(self.root)
            preview_win.title("Visualizador PDF - Introducción de Concurrencia")
            preview_win.geometry("900x1000")
            preview_win.configure(bg="#1a1a2e")
            
            # Convertir todas las páginas del PDF a imágenes
            pages = convert_from_path(pdf_path, dpi=150)
            
            if not pages:
                messagebox.showerror("Error", "No se pudo convertir el PDF a imágenes.")
                return
            
            # Frame principal con barra de navegación
            top_frame = tk.Frame(preview_win, bg="#16213e")
            top_frame.pack(fill=tk.X, padx=10, pady=10)
            
            # Variable para rastrear página actual
            self.current_page = [0]
            self.total_pages = [len(pages)]

            # Preparar canvas con scrollbars para mostrar la página completa
            canvas_frame = tk.Frame(preview_win, bg="#1a1a2e")
            canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            canvas = tk.Canvas(canvas_frame, bg="white")
            v_scroll = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
            h_scroll = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=canvas.xview)
            canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
            v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
            h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Escalar cada página al ancho objetivo para que se vea completa
            target_width = 860
            self.photo_images = []
            self.raw_sizes = []
            for page in pages:
                w, h = page.size
                scale = min(1.0, target_width / w)
                new_w = int(w * scale)
                new_h = int(h * scale)
                resized = page.resize((new_w, new_h), Image.LANCZOS)
                self.photo_images.append(ImageTk.PhotoImage(resized))
                self.raw_sizes.append((new_w, new_h))

            # Crear un item en el canvas para la imagen actual
            img_container = canvas.create_image(0, 0, anchor='nw', image=self.photo_images[0])
            canvas.config(scrollregion=(0, 0, self.raw_sizes[0][0], self.raw_sizes[0][1]))

            # Función para mostrar página (ajusta scrollregion)
            def show_page(page_num):
                if 0 <= page_num < len(self.photo_images):
                    canvas.itemconfig(img_container, image=self.photo_images[page_num])
                    canvas.config(scrollregion=(0, 0, self.raw_sizes[page_num][0], self.raw_sizes[page_num][1]))
                    self.current_page[0] = page_num
                    page_label.config(text=f"Página {page_num + 1} de {self.total_pages[0]}")
                    canvas.xview_moveto(0)
                    canvas.yview_moveto(0)
            
            # Botones de navegación
            btn_frame = tk.Frame(top_frame, bg="#16213e")
            btn_frame.pack(fill=tk.X, pady=10)
            
            btn_prev = tk.Button(btn_frame, text="◀ Anterior", command=lambda: show_page(self.current_page[0] - 1),
                                bg="#0f3460", fg="white", font=("Arial", 10, "bold"))
            btn_prev.pack(side=tk.LEFT, padx=5)
            
            page_label = tk.Label(top_frame, text=f"Página 1 de {self.total_pages[0]}", 
                                 font=("Arial", 10), bg="#16213e", fg="white")
            page_label.pack(side=tk.LEFT, padx=20)
            
            btn_next = tk.Button(btn_frame, text="Siguiente ▶", command=lambda: show_page(self.current_page[0] + 1),
                                bg="#0f3460", fg="white", font=("Arial", 10, "bold"))
            btn_next.pack(side=tk.LEFT, padx=5)
            
            # Mostrar la primera página
            show_page(0)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar el PDF: {str(e)}")

    def vista_previa_pdf_actores(self):
        """Muestra una ventana con el PDF de introducción a concurrencia usando pdf2image"""
        # Obtener ruta absoluta del PDF
        script_dir = os.path.dirname(os.path.abspath(__file__))
        pdf_path = os.path.join(script_dir, "Apuntes", "Apunte_2-5.pdf")
        
        if not os.path.exists(pdf_path):
            messagebox.showerror("Error", f"No se encontró el PDF: {pdf_path}")
            return
        
        try:
            preview_win = tk.Toplevel(self.root)
            preview_win.title("Visualizador PDF - Introducción de Concurrencia")
            preview_win.geometry("900x1000")
            preview_win.configure(bg="#1a1a2e")
            
            # Convertir todas las páginas del PDF a imágenes
            pages = convert_from_path(pdf_path, dpi=150)
            
            if not pages:
                messagebox.showerror("Error", "No se pudo convertir el PDF a imágenes.")
                return
            
            # Frame principal con barra de navegación
            top_frame = tk.Frame(preview_win, bg="#16213e")
            top_frame.pack(fill=tk.X, padx=10, pady=10)
            
            # Variable para rastrear página actual
            self.current_page = [0]
            self.total_pages = [len(pages)]

            # Preparar canvas con scrollbars para mostrar la página completa
            canvas_frame = tk.Frame(preview_win, bg="#1a1a2e")
            canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            canvas = tk.Canvas(canvas_frame, bg="white")
            v_scroll = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
            h_scroll = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=canvas.xview)
            canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
            v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
            h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Escalar cada página al ancho objetivo para que se vea completa
            target_width = 860
            self.photo_images = []
            self.raw_sizes = []
            for page in pages:
                w, h = page.size
                scale = min(1.0, target_width / w)
                new_w = int(w * scale)
                new_h = int(h * scale)
                resized = page.resize((new_w, new_h), Image.LANCZOS)
                self.photo_images.append(ImageTk.PhotoImage(resized))
                self.raw_sizes.append((new_w, new_h))

            # Crear un item en el canvas para la imagen actual
            img_container = canvas.create_image(0, 0, anchor='nw', image=self.photo_images[0])
            canvas.config(scrollregion=(0, 0, self.raw_sizes[0][0], self.raw_sizes[0][1]))

            # Función para mostrar página (ajusta scrollregion)
            def show_page(page_num):
                if 0 <= page_num < len(self.photo_images):
                    canvas.itemconfig(img_container, image=self.photo_images[page_num])
                    canvas.config(scrollregion=(0, 0, self.raw_sizes[page_num][0], self.raw_sizes[page_num][1]))
                    self.current_page[0] = page_num
                    page_label.config(text=f"Página {page_num + 1} de {self.total_pages[0]}")
                    canvas.xview_moveto(0)
                    canvas.yview_moveto(0)
            
            # Botones de navegación
            btn_frame = tk.Frame(top_frame, bg="#16213e")
            btn_frame.pack(fill=tk.X, pady=10)
            
            btn_prev = tk.Button(btn_frame, text="◀ Anterior", command=lambda: show_page(self.current_page[0] - 1),
                                bg="#0f3460", fg="white", font=("Arial", 10, "bold"))
            btn_prev.pack(side=tk.LEFT, padx=5)
            
            page_label = tk.Label(top_frame, text=f"Página 1 de {self.total_pages[0]}", 
                                 font=("Arial", 10), bg="#16213e", fg="white")
            page_label.pack(side=tk.LEFT, padx=20)
            
            btn_next = tk.Button(btn_frame, text="Siguiente ▶", command=lambda: show_page(self.current_page[0] + 1),
                                bg="#0f3460", fg="white", font=("Arial", 10, "bold"))
            btn_next.pack(side=tk.LEFT, padx=5)
            
            # Mostrar la primera página
            show_page(0)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar el PDF: {str(e)}")
    
    def abrir_hilos(self):
        """Abre el menú de hilos"""
        self.crear_submenu("Hilos", [
            ("Hilos_01", None),
            ("Hilos_02", None),
            ("Memorama con Hilos", None),
            ("Ruleta de Mario Bros", None),
        ])
    
    def abrir_sockets(self):
        """Abre el menú de sockets"""
        self.crear_submenu("Sockets", [
            ("Mensajes con Servidor/Cliente", None),
            ("Productos de Limpieza", None),
            ("TCP Algoritmos de Ordenamiento", None),
            ("UDP Algoritmos de Ordenamiento", None),
            ("UDP Sistema de Votaciones", None),
            ("Comunicación Directa", None),
            ("Comunicación Indirecta", None),
            ("Autentificación Servidor/Cliente", None),
        ])
    
    def abrir_semaforos(self):
        """Abre el menú de semáforos"""
        self.crear_submenu("Semáforos", [
            ("Sincronización", None),
            ("Servidor/Cliente", None),
            ("Condición de Carrera", None),
            ("Barbero Dormilón", None),
            ("Barbero Dormilón UDP", None),
            ("Sala de Chat Local", None),
            ("Sala de Chat Red", None),
        ])
    
    def abrir_patrones(self):
        """Abre el menú de patrones"""
        self.crear_submenu("Patrones", [
            ("Productor/Consumidor", None),
            ("Futuro/Promesa _01", None),
            ("Futuro/Promesa _02", None),
            ("Modelo de Actores", None),
            ("Modelo de Actores Servidor/Cliente", None),
            ("Reactor/Proactor", None),
        ])
    
    def abrir_ayuda(self):
        """Abre el menú de ayuda"""
        self.crear_submenu("Ayuda", [
            ("Nombres de Alumnos", self.mostrar_alumnos),
            ("Matrículas de Alumnos", self.mostrar_matriculas),
        ])
    
    def crear_submenu(self, titulo, items):
        """Crea una ventana de submenú genérica"""
        submenu = tk.Toplevel(self.root)
        submenu.title(titulo)
        submenu.geometry("500x600")
        submenu.configure(bg="#1a1a2e")
        
        # Título del submenú
        title_frame = tk.Frame(submenu, bg="#16213e")
        title_frame.pack(fill=tk.X, pady=10)
        tk.Label(title_frame, text=titulo, font=("Arial", 16, "bold"), 
                bg="#16213e", fg="white").pack(pady=10)
        
        # Frame para los items
        items_frame = tk.Frame(submenu, bg="#1a1a2e")
        items_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        for nombre, comando in items:
            btn = tk.Button(items_frame, text=nombre, font=("Arial", 11),
                           bg="#0f3460", fg="white", height=2, relief=tk.FLAT,
                           command=comando or (lambda n=nombre: messagebox.showinfo(titulo, f"Abriendo: {n}")))
            btn.pack(fill=tk.X, pady=8)
            btn.bind("<Enter>", lambda e: e.widget.config(bg="#e94560"))
            btn.bind("<Leave>", lambda e: e.widget.config(bg="#0f3460"))
        
        # Botón cerrar
        btn_cerrar = tk.Button(items_frame, text="Cerrar", font=("Arial", 11),
                              bg="#ff6b6b", fg="white", height=2, relief=tk.FLAT,
                              command=submenu.destroy)
        btn_cerrar.pack(fill=tk.X, pady=8)
        btn_cerrar.bind("<Enter>", lambda e: e.widget.config(bg="#ff5252"))
        btn_cerrar.bind("<Leave>", lambda e: e.widget.config(bg="#ff6b6b"))
    
    def mostrar_alumnos(self):
        """Muestra los nombres de los alumnos junto con su matrícula"""
        usuarios_path = ruta_recurso("usuarios.json")
        if not os.path.exists(usuarios_path):
            messagebox.showwarning("Error", "No hay datos de alumnos registrados.")
            return
        
        try:
            with open(usuarios_path, "r", encoding="utf-8") as f:
                users = json.load(f)
            
            if not users:
                messagebox.showinfo("Alumnos", "No hay alumnos registrados.")
                return
            
            # Construir la lista de alumnos con matrícula
            alumnos_info = "Alumnos Registrados:\n\n"
            for i, (username, udata) in enumerate(users.items(), 1):
                if isinstance(udata, dict):
                    matricula = udata.get("matricula", "Sin matrícula")
                    alumnos_info += f"{i}. {username} - Matrícula: {matricula}\n"
            
            messagebox.showinfo("Alumnos", alumnos_info)
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer alumnos: {str(e)}")
    
    def mostrar_matriculas(self):
        """Muestra las matrículas de los alumnos junto con su nombre"""
        usuarios_path = ruta_recurso("usuarios.json")
        if not os.path.exists(usuarios_path):
            messagebox.showwarning("Error", "No hay datos de alumnos registrados.")
            return
        
        try:
            with open(usuarios_path, "r", encoding="utf-8") as f:
                users = json.load(f)
            
            if not users:
                messagebox.showinfo("Matrículas", "No hay alumnos registrados.")
                return
            
            # Construir la lista de matrículas con alumno
            matriculas_info = "Matrículas de Alumnos:\n\n"
            for i, (username, udata) in enumerate(users.items(), 1):
                if isinstance(udata, dict):
                    matricula = udata.get("matricula", "Sin matrícula")
                    matriculas_info += f"{i}. Matrícula: {matricula} - Alumno: {username}\n"
            
            messagebox.showinfo("Matrículas", matriculas_info)
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer matrículas: {str(e)}")
    
    def salir(self):
        """Cierra la aplicación"""
        self.root.destroy()


def main(username, email):
    root = tk.Tk()
    app = MenuPrincipal(root, username)
    root.mainloop()


if __name__ == "__main__":
    main("Usuario Prueba", "prueba@example.com")