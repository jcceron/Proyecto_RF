import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import face_recognition
import os
import sqlite3

class FacialRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Facial Recognition App")
        
        # Variables
        self.person_id_var = tk.StringVar()
        self.image_path = None

        # Componentes de la interfaz de usuario
        tk.Label(root, text="Person ID:").grid(row=0, column=0, sticky="e")
        tk.Entry(root, textvariable=self.person_id_var).grid(row=0, column=1)
        tk.Button(root, text="Choose Image", command=self.choose_image).grid(row=1, column=0, columnspan=2, pady=10)
        tk.Button(root, text="Recognize", command=self.recognize_faces).grid(row=2, column=0, columnspan=2, pady=10)

        # Visualización de imágenes
        self.image_label = tk.Label(root)
        self.image_label.grid(row=3, column=0, columnspan=2)

        # Visualización de resultados
        self.result_label = tk.Label(root, text="")
        self.result_label.grid(row=4, column=0, columnspan=2, pady=10)

        # Conéctese a una base de datos SQLite en memoria
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()

        # Crear una tabla para los resultados del reconocimiento
        self.cursor.execute("""
            CREATE TABLE recognition_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id TEXT,
                image_path TEXT,
                confidence REAL
            )
        """)

        # Botón para operaciones de base de datos
        tk.Button(root, text="Save Result", command=self.save_result).grid(row=5, column=0, pady=10)
        tk.Button(root, text="Show Database Records", command=self.show_database_records).grid(row=5, column=1, pady=10)
        tk.Button(root, text="Delete Database Records", command=self.delete_database_records).grid(row=5, column=2, pady=10)
        
        tk.Button(root, text="Verify Saved Result", command=self.verify_saved_result).grid(row=5, column=3, pady=10)

    def choose_image(self):
        # Borrar resultados anteriores
        self.result_label.config(text="")
        # Abrir cuadro de diálogo de archivo para elegir la imagen
        self.image_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("JPEG files", "*.jpg")])

        # Mostrar la imagen elegida
        self.display_image()

    def display_image(self):
        # Mostrar la imagen elegida
        if self.image_path:
            image = Image.open(self.image_path)
            #image = image.resize((300, 300), Image.ANTIALIAS)
            image = image.resize((300, 300), Image.ANTIALIAS if hasattr(Image, 'ANTIALIAS') else Image.BICUBIC)
            photo = ImageTk.PhotoImage(image)
            self.image_label.configure(image=photo)
            self.image_label.image = photo

    def recognize_faces(self):
        if self.image_path:
            # Borrar resultados anteriores
            self.result_label.config(text="")

            # Cargue la imagen para reconocer
            unknown_image = face_recognition.load_image_file(self.image_path)

            # Encuentre todas las ubicaciones de rostros y codificaciones de rostros en la imagen desconocida
            face_locations = face_recognition.face_locations(unknown_image)
            face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

            # Haz un bucle sobre cada cara que se encuentra en la imagen desconocida
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # Comparar la codificación facial con todas las codificaciones faciales conocidas
                results = self.compare_with_known_faces(face_encoding)

                # Mostrar los resultados
                self.display_recognition_results(results)

    def compare_with_known_faces(self, unknown_face_encoding):
        # Recupere la lista de codificaciones faciales conocidas
        known_faces_dir = "imagenes_conocidas"
        known_face_encodings = self.get_known_face_encodings(known_faces_dir)

        # Comparar la codificación facial con todas las codificaciones faciales conocidas
        results = []
        for known_face_id, known_face_encoding in known_face_encodings.items():
            # Calcular la distancia euclidiana (diferencia porcentual)
            face_distance = face_recognition.face_distance([known_face_encoding], unknown_face_encoding)
            confidence = (1 - face_distance[0]) * 100

            # Almacene el resultado del reconocimiento en la base de datos en memoria
            self.store_recognition_result(known_face_id, confidence)

            # Anexar resultados
            results.append((known_face_id, confidence))

        # Ordenar los resultados por confianza en orden descendente
        results.sort(key=lambda x: x[1], reverse=True)

        # Obtenga la identificación de la persona con la mayor confianza
        top_person_id = results[0][0]

        # Update the person ID entry field
        self.person_id_var.set(top_person_id.split(".")[0])  # Eliminar extensión de archivo

        # Almacene el resultado con la mayor confianza en la base de datos
        self.store_recognition_result_to_db(results[0])

        return results[:1]  # Devolver solo el resultado superior

    def get_known_face_encodings(self, known_faces_dir):
        known_face_encodings = {}
        for filename in os.listdir(known_faces_dir):
            path = os.path.join(known_faces_dir, filename)
            image = face_recognition.load_image_file(path)
            face_encoding = face_recognition.face_encodings(image)[0]
            known_face_encodings[filename] = face_encoding
        return known_face_encodings

    def store_recognition_result(self, person_id, confidence):
        # Almacene el resultado del reconocimiento en la base de datos en memoria
        self.cursor.execute("INSERT INTO recognition_results (person_id, image_path, confidence) VALUES (?, ?, ?)",
                            (person_id, self.image_path, confidence))
        self.conn.commit()

    def store_recognition_result_to_db(self, result):
        # Almacene el resultado con la mayor confianza en la base de datos en memoria
        person_id, confidence = result
        self.cursor.execute("INSERT INTO recognition_results (person_id, image_path, confidence) VALUES (?, ?, ?)",
                            (person_id, self.image_path, confidence))
        self.conn.commit()
        
    def verify_saved_result(self):
        # Verifique que el resultado esté guardado en la base de datos
        self.cursor.execute("SELECT * FROM recognition_results")
        records = self.cursor.fetchall()

        if records:
            print("Records in the database:")
            for record in records:
                print(record)
        else:
            print("No records in the database.")

    def display_recognition_results(self, results):
        # Mostrar los resultados
        for person_id, confidence in results:
            result_text = f"Recognition Result for {person_id}: Confidence: {confidence:.2f}%"
            self.result_label.config(text=result_text)
            
    def show_database_records(self):
        # Recuperar y mostrar registros de la base de datos en memoria
        records = self.retrieve_database_records()
        self.display_database_records(records)

    def save_result(self):
        # Guarde el resultado actual en la base de datos
        person_id, image_path, confidence = self.get_current_result()
        if person_id and image_path and confidence:
            self.store_in_database(person_id, image_path, confidence)
            messagebox.showinfo("Resultado guardado", "Resultado guardado en la base de datos.")
        else:
            messagebox.showinfo("Sin resultado", "No hay ningún resultado que guardar. Realice primero el reconocimiento facial.")

    def delete_database_records(self):
        # Eliminar todos los registros de la base de datos
        response = messagebox.askquestion("Eliminar registros", "¿Está seguro de que desea eliminar todos los registros?")
        if response == "yes":
            self.cursor.execute("DELETE FROM recognition_results")
            self.conn.commit()
            messagebox.showinfo("Registros eliminados", "Todos los registros eliminados de la base de datos.")

    def retrieve_database_records(self):
        # Recuperar todos los registros de la base de datos en memoria
        self.cursor.execute("SELECT * FROM recognition_results")
        records = self.cursor.fetchall()
        return records

    def display_database_records(self, records):
        # Mostrar los registros en una nueva ventana
        records_window = tk.Toplevel(self.root)
        records_window.title("Registros de la base de datos")

        # Crear una vista de árbol para mostrar registros
        # tree = tk.ttk.Treeview(records_window)
        tree = ttk.Treeview(records_window)
        tree["columns"] = ("Person ID", "Image Path", "Confidence")
        tree.heading("#0", text="ID")
        tree.column("#0", width=50, minwidth=50, stretch=tk.NO)
        tree.heading("Person ID", text="Person ID")
        tree.column("Person ID", anchor=tk.W, width=100)
        tree.heading("Image Path", text="Image Path")
        tree.column("Image Path", anchor=tk.W, width=150)
        tree.heading("Confidence", text="Confidence")
        tree.column("Confidence", anchor=tk.W, width=200)

        # Insertar registros en la vista de árbol
        for record in records:
            tree.insert("", tk.END, values=record)

        tree.pack(expand=tk.YES, fill=tk.BOTH)

    def get_current_result(self):
        # Recuperar los detalles del resultado actual
        try:
            with open("results.txt", "r") as file:
                lines = file.readlines()
                if len(lines) >= 2:
                    person_id = lines[0].split(":")[1].strip()
                    image_path = lines[1].split(":")[1].strip()
                    confidence = float(lines[2].split(":")[1].strip().strip('%')) / 100.0
                    return person_id, image_path, confidence
                else:
                # El archivo no tiene suficientes líneas
                    return None
        except FileNotFoundError:
            # El archivo no existe
            return None

if __name__ == "__main__":
    root = tk.Tk()
    app = FacialRecognitionApp(root)
    root.mainloop()
