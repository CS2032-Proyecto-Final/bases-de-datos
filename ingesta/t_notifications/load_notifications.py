import os
import boto3
from botocore.exceptions import NoCredentialsError

# Variables globales
BASE_DIRECTORY = "."  # Directorio base donde se encuentran los archivos locales
BOOKS_SUBFOLDER = "notifications"  # Carpeta en el bucket para almacenar los .csv de libros

# Conexión a S3 usando las credenciales configuradas en ~/.aws/credentials
s3 = boto3.client('s3')

# Función para subir un archivo a S3
def upload_to_s3(file_path, bucket, s3_file_path):
    try:
        s3.upload_file(file_path, bucket, s3_file_path)
        print(f"Archivo {file_path} subido exitosamente a {s3_file_path} en {bucket}")
    except FileNotFoundError:
        print(f"El archivo {file_path} no fue encontrado.")
    except NoCredentialsError:
        print("Credenciales no disponibles.")

# Función para realizar la ingesta de archivos de libros
def ingest():
    stage = os.environ.get("STAGE")  # Prefijo basado en el entorno
    for root, dirs, files in os.walk(BASE_DIRECTORY):
        for file in files:
            if file.endswith(".csv"):
                # Verificar si el archivo pertenece a un prefijo válido
                if root.startswith(f"./{stage}-t_{BOOKS_SUBFOLDER}"):
                    # Crear el nombre del bucket según el prefijo
                    bucket_name = f"{stage}-bibliokuna-ingesta"
                    
                    # Crear la ruta del archivo CSV dentro de la carpeta `books/` en el bucket
                    s3_file_path = f"{BOOKS_SUBFOLDER}/{file}"  # Directamente en books/ sin subdirectorios

                    # Subir archivo al bucket S3
                    file_path = os.path.join(root, file)
                    upload_to_s3(file_path, bucket_name, s3_file_path)

# Llamada a la función para realizar la ingesta
ingest()
