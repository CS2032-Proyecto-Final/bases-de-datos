import boto3
import csv
import os
from loguru import logger
from datetime import datetime

# Configuración de logger con milisegundos
LOG_FILE_PATH = "/logs/pull_users.log"
logger.add(LOG_FILE_PATH, format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}", level="INFO", rotation="10 MB")

# Variable global para definir el nombre de la tabla
TABLE_NAME = "t_users"

def export_table_to_csv_dynamodb(prefix, table_name=TABLE_NAME):
    """
    Exporta los datos de una tabla DynamoDB a un archivo CSV sin encabezados.
    
    Args:
        prefix (str): Prefijo del directorio donde se guardará el archivo (dev, test, prod).
        table_name (str): Nombre de la tabla DynamoDB.
    """
    logger.info(f"Iniciando exportación de la tabla '{table_name}' para el prefijo '{prefix}'.")
    start_time = datetime.now()

    try:
        # Crear cliente DynamoDB
        dynamodb = boto3.client('dynamodb', region_name='us-east-1')

        # Crear directorio de salida si no existe
        output_dir = f"./{prefix}-{table_name}"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.info(f"Directorio creado: {output_dir}")

        # Definir ruta del archivo CSV
        csv_file_path = os.path.join(output_dir, f"{table_name}.csv")

        # Abrir el archivo CSV para escribir
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)

            # Iniciar paginación para scan
            paginator = dynamodb.get_paginator('scan')
            response_iterator = paginator.paginate(TableName=f"{prefix}-{table_name}")

            # Contador para filas exportadas
            row_count = 0

            # Iterar sobre las páginas
            for page in response_iterator:
                items = page.get('Items', [])
                for item in items:
                    # Convertir el formato de DynamoDB a un formato plano
                    flat_item = {k: list(v.values())[0] for k, v in item.items()}
                    # Escribir los valores como una fila en el archivo CSV
                    writer.writerow(flat_item.values())
                    row_count += 1

        logger.success(f"Exportación completada. Archivo generado: {csv_file_path}. Total de filas exportadas: {row_count}")
    except Exception as e:
        logger.error(f"Error durante la exportación: {str(e)}")
    finally:
        end_time = datetime.now()
        logger.info(f"Exportación finalizada. Tiempo total: {end_time - start_time}")

# Llamadas a la función con diferentes prefijos
prefix = os.environ.get("STAGE")  # Default "dev" if not set
export_table_to_csv_dynamodb(prefix)
