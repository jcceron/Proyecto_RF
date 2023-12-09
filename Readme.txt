# Aplicación de reconocimiento facial

## Descripción
Esta aplicación de reconocimiento facial está diseñada para identificar rostros en imágenes 
y proporcionar información sobre la identidad de las personas detectadas. 
La aplicación utiliza la librería `face_recognition` de Python y cuenta con funcionalidades 
para realizar operaciones de reconocimiento facial, almacenar resultados en una base de datos SQLite 
y consultar registros almacenados.

## Funcionalidades Principales
- **Reconocimiento Facial:** Carga una imagen y realiza el reconocimiento facial, mostrando el resultado 
con el nombre de la persona identificada y el porcentaje de coincidencia.
- **Almacenamiento en Base de Datos:** Permite grabar los resultados de reconocimiento facial en una base 
de datos SQLite para consultas posteriores.
- **Consulta de Registros:** Muestra los registros almacenados en la base de datos.
- **Eliminación de Registros:** Permite eliminar todos los registros almacenados en la base de datos.

## Requisitos
- Python 3.x
- Librería `face_recognition`
- Librería `Pillow`
- Librería `SQLite3`
- Librería `tk`

## Instalación
1. Clona este repositorio: `git clone https://github.com/jcceron/proyecto_IA_EV.git`
2. Entra al directorio del proyecto: `proyecto_IA_EV`
3. Instala las dependencias: `pip install -r requirements.txt`

## Uso
1. Ejecuta la aplicación: `python main.py`
2. Carga una imagen para realizar el reconocimiento facial.
3. Utiliza los botones proporcionados para realizar diversas operaciones.

## Configuración
- La configuración de la aplicación se encuentra en el archivo `config.py`. Puedes ajustar parámetros como la ruta de la base de datos y otras configuraciones.

## Contribuciones
Si deseas contribuir a este proyecto, sigue estos pasos:
1. Haz un fork del repositorio.
2. Crea una rama para tu contribución: `git checkout -b mi-contribucion`
3. Realiza tus cambios y haz commit: `git commit -m "Añadir nueva funcionalidad"`
4. Haz push a tu rama: `git push origin mi-contribucion`
5. Crea un Pull Request en GitHub.

## Autor
- Juan Carlos Cerón Lombana

## Licencia
Este proyecto está bajo la licencia [MIT](LICENSE).

