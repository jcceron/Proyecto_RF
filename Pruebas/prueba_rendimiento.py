import unittest
import timeit
# Ajusta el import según tu implementación
from funcion_rendimiento import your_performance_function 

class TestPerformance(unittest.TestCase):
    def test_performance(self):
        # Definir la función o método que deseas evaluar
        def wrapper():
            your_performance_function()  # Ajusta según tu función de rendimiento

        # Configurar la prueba de rendimiento con timeit
        time_taken = timeit.timeit(wrapper, number=200)  # Ajusta el número de iteraciones según tus necesidades

        # Establecer un límite de tiempo aceptable (ajusta según tus requerimientos)
        acceptable_time = 1.0  # en segundos

        # Verificar si el tiempo tomado está dentro del límite aceptable
        self.assertLessEqual(time_taken, acceptable_time)

if __name__ == '__main__':
    unittest.main()
