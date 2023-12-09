import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import face_recognition
import sqlite3

class FacialRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación de reconocimiento facial")

        # Variables
        self.person_id_var = tk.StringVar()
        self.image_path = None

        # Componentes de la interfaz de usuario
        tk.Label(root, text="Identificación:").grid(row=0, column=0, sticky="e")
        tk.Entry(root, textvariable=self.person_id_var).grid(row=0, column=1)
        tk.Button(root, text="Seleccione la fotografía:", command=self.choose_image).grid(row=1, column=0, columnspan=2, pady=10)
        tk.Button(root, text="Reconocer:", command=self.recognize_face).grid(row=2, column=0, columnspan=2, pady=10)

        # Visualización de imágenes
        self.image_label = tk.Label(root)
        self.image_label.grid(row=3, column=0, columnspan=2)

        # Visualización de resultados
        self.result_label = tk.Label(root, text="")
        self.result_label.grid(row=4, column=0, columnspan=2, pady=10)

        # Inicialización de la base de datos
        self.conn = sqlite3.connect(':memory:')  # Uso de una base de datos en memoria con fines de demostración
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE recognition_results (
                id INTEGER PRIMARY KEY,
                person_id TEXT,
                image_path TEXT,
                confidence REAL
            )
        ''')

    def choose_image(self):
        # Abrir cuadro de diálogo de archivo para elegir la imagen
        self.image_path = filedialog.askopenfilename(title="Seleccione el archivo de la imagen", filetypes=[("JPEG files", "*.jpg")])

        # Mostrar la imagen elegida
        self.display_image()

    def display_image(self):
        # Mostrar la imagen elegida
        if self.image_path:
            image = Image.open(self.image_path)
            # image = image.resize((300, 300), Image.ANTIALIAS)
            image = image.resize((300, 300), Image.ANTIALIAS if hasattr(Image, 'ANTIALIAS') else Image.BICUBIC)
            photo = ImageTk.PhotoImage(image)
            self.image_label.configure(image=photo)
            self.image_label.image = photo

    def recognize_face(self):
        if self.image_path:
            # Cargar la codificación de caras conocidas
            known_face_encoding = self.get_known_face_encoding()

            # Cargue la imagen para reconocer
            unknown_image = face_recognition.load_image_file(self.image_path)

            # Encuentre todas las ubicaciones de rostros y codificaciones de rostros en la imagen desconocida
            face_locations = face_recognition.face_locations(unknown_image)
            face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

            # Haz un bucle sobre cada cara que se encuentra en la imagen desconocida
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # Comparar la codificación facial con la codificación facial conocida
                results = face_recognition.compare_faces([known_face_encoding], face_encoding)

                # Calcular la distancia euclidiana (diferencia porcentual)
                face_distance = face_recognition.face_distance([known_face_encoding], face_encoding)
                confidence = (1 - face_distance[0]) * 100

                # Mostrar el resultado
                result_text = f"Resultado del reconocimiento: {'Cotejado' if results[0] else 'No Cotejado'}"
                confidence_text = f"Confianza: {confidence:.2f}%"
                self.result_label.config(text=f"{result_text}\n{confidence_text}")

                # Almacenar el resultado del reconocimiento en la base de datos
                self.store_recognition_result(confidence)

    def get_known_face_encoding(self):
        # Recupere la codificación facial conocida
        known_image_path = "imagenes_conocidas/image.jpg"
        known_image = face_recognition.load_image_file(known_image_path)
        known_face_encoding = face_recognition.face_encodings(known_image)[0]
        return known_face_encoding

    def store_recognition_result(self, confidence):
        # Almacene el resultado del reconocimiento en la base de datos en memoria
        person_id = self.person_id_var.get()
        self.cursor.execute("INSERT INTO recognition_results (person_id, image_path, confidence) VALUES (?, ?, ?)",
                            (person_id, self.image_path, confidence))
        self.conn.commit()

if __name__ == "__main__":
    root = tk.Tk()
    app = FacialRecognitionApp(root)
    root.mainloop()
