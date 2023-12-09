import unittest
import os
import face_recognition

class TestFaceRecognition(unittest.TestCase):
    def setUp(self):
        # Obtén la ruta del directorio actual del script
        current_directory = os.path.dirname(__file__)
        # Construye la ruta completa al directorio 'test_images'
        self.test_images_dir = os.path.join(current_directory, 'test_imagenes')
        
        # Directorio de imágenes de prueba
        self.test_images_dir = "test_imagenes"
        # Lista para almacenar las rutas de las imágenes de prueba
        self.test_image_paths = []

        # Llena la lista de rutas de imágenes de prueba
        for filename in os.listdir(self.test_images_dir):
            if filename.endswith(".jpg"):
                image_path = os.path.join(self.test_images_dir, filename)
                self.test_image_paths.append(image_path)

    def test_face_detection(self):
        for image_path in self.test_image_paths:
            with self.subTest(image_path=image_path):
                # Carga la imagen
                image = face_recognition.load_image_file(image_path)
                # Realiza la detección de caras
                face_locations = face_recognition.face_locations(image)

                # Asegúrate de que al menos una cara sea detectada
                self.assertGreaterEqual(len(face_locations), 1)

    def test_face_recognition(self):
        # Crear una lista de nombres ficticios para las caras de prueba
        known_face_names = ["Persona1", "Persona2", "Persona3"]

        # Crear un diccionario para almacenar las caras conocidas
        known_faces = {name: [] for name in known_face_names}

        # Cargar las imágenes de prueba y asociarlas con los nombres
        for name in known_face_names:
            for filename in os.listdir(self.test_images_dir):
                if filename.startswith(name):
                    image_path = os.path.join(self.test_images_dir, filename)
                    face_image = face_recognition.load_image_file(image_path)
                    known_faces[name].append(face_recognition.face_encodings(face_image)[0])

        # Realizar el reconocimiento facial
        for name, face_encodings in known_faces.items():
            for face_encoding in face_encodings:
                with self.subTest(name=name):
                    # Simular la detección de una cara en la imagen de prueba
                    unknown_image_path = os.path.join(self.test_images_dir, f"Unknown_{name}.jpg")
                    unknown_image = face_recognition.load_image_file(unknown_image_path)
                    unknown_face_locations = face_recognition.face_locations(unknown_image)
                    unknown_face_encoding = face_recognition.face_encodings(unknown_image, unknown_face_locations)[0]

                    # Realizar el reconocimiento facial
                    matches = face_recognition.compare_faces(face_encodings, unknown_face_encoding)

                    # Asegurarse de que al menos una coincidencia sea positiva
                    self.assertTrue(any(matches))

if __name__ == '__main__':
    unittest.main()
