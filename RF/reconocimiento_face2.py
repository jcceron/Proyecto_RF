import tkinter as tk
from tkinter import filedialog
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

        # UI Components
        tk.Label(root, text="Person ID:").grid(row=0, column=0, sticky="e")
        tk.Entry(root, textvariable=self.person_id_var).grid(row=0, column=1)
        tk.Button(root, text="Choose Image", command=self.choose_image).grid(row=1, column=0, columnspan=2, pady=10)
        tk.Button(root, text="Recognize", command=self.recognize_faces).grid(row=2, column=0, columnspan=2, pady=10)

        # Image Display
        self.image_label = tk.Label(root)
        self.image_label.grid(row=3, column=0, columnspan=2)

        # Result Display
        self.result_label = tk.Label(root, text="")
        self.result_label.grid(row=4, column=0, columnspan=2, pady=10)

        # Database Initialization
        self.conn = sqlite3.connect(':memory:')  # Use an in-memory database for demonstration purposes
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
        # Clear previous results
        self.result_label.config(text="")
        # Open file dialog to choose image
        self.image_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("JPEG files", "*.jpg")])

        # Display chosen image
        self.display_image()

    def display_image(self):
        # Display the chosen image
        if self.image_path:
            image = Image.open(self.image_path)
            #image = image.resize((300, 300), Image.ANTIALIAS)
            image = image.resize((300, 300), Image.ANTIALIAS if hasattr(Image, 'ANTIALIAS') else Image.BICUBIC)
            photo = ImageTk.PhotoImage(image)
            self.image_label.configure(image=photo)
            self.image_label.image = photo

    def recognize_faces(self):
        if self.image_path:
            # Clear previous results
            self.result_label.config(text="")

            # Load the image to recognize
            unknown_image = face_recognition.load_image_file(self.image_path)

            # Find all face locations and face encodings in the unknown image
            face_locations = face_recognition.face_locations(unknown_image)
            face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

            # Loop over each face found in the unknown image
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # Compare the face encoding with all known face encodings
                results = self.compare_with_known_faces(face_encoding)

                # Display the results
                self.display_recognition_results(results)

    def compare_with_known_faces(self, unknown_face_encoding):
        # Retrieve the list of known face encodings (you can replace this with your own logic)
        known_faces_dir = "imagenes_conocidas"
        known_face_encodings = self.get_known_face_encodings(known_faces_dir)

        # Compare the face encoding with all known face encodings
        results = []
        for known_face_id, known_face_encoding in known_face_encodings.items():
            # Calculate the Euclidean distance (percentage difference)
            face_distance = face_recognition.face_distance([known_face_encoding], unknown_face_encoding)
            confidence = (1 - face_distance[0]) * 100

            # Store the recognition result in the in-memory database
            self.store_recognition_result(known_face_id, confidence)

            # Append results
            results.append((known_face_id, confidence))

        return results

    def get_known_face_encodings(self, known_faces_dir):
        known_face_encodings = {}
        for filename in os.listdir(known_faces_dir):
            path = os.path.join(known_faces_dir, filename)
            image = face_recognition.load_image_file(path)
            face_encoding = face_recognition.face_encodings(image)[0]
            known_face_encodings[filename] = face_encoding
        return known_face_encodings

    def store_recognition_result(self, person_id, confidence):
        # Store the recognition result in the in-memory database
        self.cursor.execute("INSERT INTO recognition_results (person_id, image_path, confidence) VALUES (?, ?, ?)",
                            (person_id, self.image_path, confidence))
        self.conn.commit()

    def display_recognition_results(self, results):
        # Display the results
        for person_id, confidence in results:
            result_text = f"Resultados de reconocimiento para {person_id}: Coincidencia: {confidence:.2f}%"
            self.result_label.config(text=self.result_label.cget("text") + "\n" + result_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = FacialRecognitionApp(root)
    root.mainloop()
