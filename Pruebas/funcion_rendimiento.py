import face_recognition
import os

def your_performance_function():
    # Directorio de imágenes de prueba
    test_images_dir = "test_images"

    # Lista para almacenar las rutas de las imágenes de prueba
    test_image_paths = []

    # Llena la lista de rutas de imágenes de prueba
    for filename in os.listdir(test_images_dir):
        if filename.endswith(".jpg"):
            image_path = os.path.join(test_images_dir, filename)
            test_image_paths.append(image_path)

    # Lista para almacenar las codificaciones faciales
    face_encodings = []

    # Codificar las caras en las imágenes de prueba
    for image_path in test_image_paths:
        # Carga la imagen
        image = face_recognition.load_image_file(image_path)
        # Realiza la codificación facial
        face_encoding = face_recognition.face_encodings(image)[0]
        face_encodings.append(face_encoding)

    # Realizar alguna operación adicional con las codificaciones faciales (puedes ajustar según tus necesidades)
    # En este ejemplo, simplemente se retorna la lista de codificaciones faciales
    return face_encodings

# Llama a la función de rendimiento
result = your_performance_function()

# Puedes realizar más operaciones con el resultado si es necesario
# Por ejemplo, almacenar el resultado en una base de datos, realizar comparaciones, etc.
