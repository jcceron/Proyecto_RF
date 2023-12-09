import unittest
import sqlite3
import os

class TestDatabase(unittest.TestCase):
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

    def test_insert_record(self):
        # Insertar un registro en la base de datos
        self.cursor.execute("INSERT INTO records (name, face_encoding) VALUES (?, ?)", ('Person1', b'\x01\x02\x03'))
        self.connection.commit()

        # Recuperar el registro y verificar la coincidencia
        self.cursor.execute("SELECT * FROM records WHERE name=?", ('Person1',))
        record = self.cursor.fetchone()

        # Asegurarse de que el registro sea recuperado correctamente
        self.assertIsNotNone(record)
        self.assertEqual(record[1], 'Person1')  # Verificar el nombre
        self.assertEqual(record[2], b'\x01\x02\x03')  # Verificar la codificación facial

    def test_retrieve_record(self):
        # Insertar un registro en la base de datos
        self.cursor.execute("INSERT INTO records (name, face_encoding) VALUES (?, ?)", ('Person2', b'\x04\x05\x06'))
        self.connection.commit()

        # Recuperar el registro y verificar la coincidencia
        self.cursor.execute("SELECT * FROM records WHERE name=?", ('Person2',))
        record = self.cursor.fetchone()

        # Asegurarse de que el registro sea recuperado correctamente
        self.assertIsNotNone(record)
        self.assertEqual(record[1], 'Person2')  # Verificar el nombre
        self.assertEqual(record[2], b'\x04\x05\x06')  # Verificar la codificación facial

if __name__ == '__main__':
    unittest.main()
