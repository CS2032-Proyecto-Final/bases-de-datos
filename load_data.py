import boto3
import json

# Inicializar DynamoDB

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# Prefijo para las tablas
pref = "dev"

def load_data_to_dynamodb(table_name, data_file):
    # Añadir prefijo al nombre de la tabla
    full_table_name = f"{pref}-{table_name}"
    table = dynamodb.Table(full_table_name)
    
    # Leer los datos desde el archivo
    with open(data_file, 'r', encoding='utf-8') as file:
        items = json.load(file)
        
        # Usar batch_writer para cargar los datos
        for item in items:
            table.put_item(Item=item)
    print(f"Datos cargados en la tabla {full_table_name}")

# Cargar los datos en las tablas correspondientes
#load_data_to_dynamodb('t_users', 'users.json')
#load_data_to_dynamodb('t_books', 'books.json')
#load_data_to_dynamodb('t_favorites', 'favorites.json')
load_data_to_dynamodb('t_environments', 'environments.json')