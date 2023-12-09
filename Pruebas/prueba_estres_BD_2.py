import concurrent.futures
import sqlite3

class TestDatabaseStress:
    def create_table(self):
        # Crea la conexión y el cursor para crear la tabla
        connection = sqlite3.connect("tu_base_de_datos.db")
        cursor = connection.cursor()

        try:
            # Crea la tabla si no existe
            cursor.execute("CREATE TABLE IF NOT EXISTS records (name TEXT, face_encoding TEXT)")
            connection.commit()
        finally:
            # Cierra la conexión al finalizar
            connection.close()

    def insert_record(self, record_data):
        # Crea una nueva conexión y cursor para cada hilo
        connection = sqlite3.connect("tu_base_de_datos.db")
        cursor = connection.cursor()

        try:
            cursor.execute("INSERT INTO records (name, face_encoding) VALUES (?, ?)", record_data)
            connection.commit()
        finally:
            # Cierra la conexión al finalizar
            connection.close()

    def test_database_stress(self):
        num_threads = 10
        record_data = ("Nombre", "Cadena_de_codificación_de_la_cara")  # Define tus propios valores

        # Crea la tabla antes de ejecutar la prueba de estrés
        self.create_table()

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            # Pasa el cursor correspondiente a cada hilo
            results = list(executor.map(self.insert_record, [record_data] * num_threads))

if __name__ == "__main__":
    test_stress = TestDatabaseStress()
    test_stress.test_database_stress()
