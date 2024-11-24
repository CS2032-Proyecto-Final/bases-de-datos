import boto3
import csv
import os

def export_table_to_csv_dynamodb(table_name, output_dir="clientes_db"):
    # Crear cliente DynamoDB
    dynamodb = boto3.client('dynamodb')
    
    # Crear directorio de salida si no existe
    table_dir = os.path.join(output_dir, table_name)
    if not os.path.exists(table_dir):
        os.makedirs(table_dir)

    # Definir ruta del archivo CSV
    csv_file_path = os.path.join(table_dir, f"{table_name}.csv")

    # Abrir el archivo CSV para escribir
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Iniciar paginación para scan
        paginator = dynamodb.get_paginator('scan')
        response_iterator = paginator.paginate(TableName=table_name)

        # Iterar sobre las páginas
        for page in response_iterator:
            items = page.get('Items', [])
            for item in items:
                # Convertir el formato de DynamoDB a un formato plano
                flat_item = {k: list(v.values())[0] for k, v in item.items()}
                # Escribir los valores como una fila en el archivo CSV
                writer.writerow(flat_item.values())

    print(f"Exported table {table_name} to {csv_file_path}")

# Uso de la función
export_table_to_csv_dynamodb("test-t_books")
