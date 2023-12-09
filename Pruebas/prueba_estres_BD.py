import unittest
import sqlite3
from concurrent.futures import ThreadPoolExecutor

class TestDatabaseStress(unittest.TestCase):
    def setUp(self):
        # Conectar a la base de datos en memoria (puedes ajustar la conexión según tu configuración)
        self.connection = sqlite3.connect(':memory:')
        self.cursor = self.connection.cursor()

        # Crear la tabla de registros (ajusta la creación de la tabla según tu esquema)
        self.cursor.execute('''
            CREATE TABLE records (
                id INTEGER PRIMARY KEY,
                name TEXT,
                face_encoding BLOB
            )
        ''')

    def tearDown(self):
        # Cerrar la conexión después de cada prueba
        self.connection.close()

    def insert_record(self, record_data):
        # Insertar un registro en la base de datos
        self.cursor.execute("INSERT INTO records (name, face_encoding) VALUES (?, ?)", record_data)
        self.connection.commit()

    def test_database_stress(self):
        # Número de hilos concurrentes (ajusta según tus necesidades)
        num_threads = 10

        # Datos del registro a insertar (ajusta según tus necesidades)
        record_data = ('Person', b'\x01\x02\x03')

        # Ejecutar las inserciones concurrentemente
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            # Lista para almacenar los resultados de las inserciones
            results = list(executor.map(self.insert_record, [record_data] * num_threads))

        # Verificar que todas las inserciones se realizaron correctamente
        self.assertEqual(len(results), num_threads)

if __name__ == '__main__':
    unittest.main()
