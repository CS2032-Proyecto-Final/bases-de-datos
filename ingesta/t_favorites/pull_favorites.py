import boto3
import csv
import os

# Variable global para definir el nombre de la tabla
TABLE_NAME = "t_favorites"

def export_table_to_csv_dynamodb(prefix, table_name=TABLE_NAME):
    """
    Exporta los datos de una tabla DynamoDB a un archivo CSV sin encabezados.
    
    Args:
        prefix (str): Prefijo del directorio donde se guardará el archivo (dev, test, prod).
        table_name (str): Nombre de la tabla DynamoDB.
    """
    # Crear cliente DynamoDB
    dynamodb = boto3.client('dynamodb', region_name='us-east-1')

    # Crear directorio de salida si no existe
    output_dir = f"./{prefix}-{table_name}"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Definir ruta del archivo CSV
    csv_file_path = os.path.join(output_dir, f"{table_name}.csv")

    # Abrir el archivo CSV para escribir
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Iniciar paginación para scan
        paginator = dynamodb.get_paginator('scan')
        response_iterator = paginator.paginate(TableName=f"{prefix}-{table_name}")

        # Iterar sobre las páginas
        for page in response_iterator:
            items = page.get('Items', [])
            for item in items:
                # Convertir el formato de DynamoDB a un formato plano
                flat_item = {k: list(v.values())[0] for k, v in item.items()}
                # Escribir los valores como una fila en el archivo CSV
                writer.writerow(flat_item.values())

    print(f"Exported table {table_name} to {csv_file_path}")

# Llamadas a la función con diferentes prefijos
prefix = os.environ.get("STAGE")
export_table_to_csv_dynamodb(prefix)
