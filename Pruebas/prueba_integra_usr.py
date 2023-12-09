import unittest
import tkinter as tk
from tkinter import ttk
from prueba import YourApp  # Ajusta el import según la estructura de tu aplicación

class TestUserInterfaceIntegration(unittest.TestCase):
    def setUp(self):
        # Crear una ventana de prueba
        self.root = tk.Tk()
        self.app = YourApp(self.root)  # Ajusta la creación de la aplicación según tu implementación

    def tearDown(self):
        # Cerrar la ventana después de cada prueba
        self.root.destroy()

    def test_button_click(self):
        # Simular un clic en un botón de la interfaz
        button = self.app.your_button  # Ajusta según el nombre de tu botón
        button.invoke()

        # Verificar el resultado esperado después de hacer clic en el botón
        result_label = self.app.result_label  # Ajusta según el nombre de tu etiqueta de resultado
        result_text = result_label.cget("text")

        expected_result = "Hello, World!"  # Ajusta según el resultado esperado
        self.assertEqual(result_text, expected_result)

if __name__ == '__main__':
    unittest.main()
