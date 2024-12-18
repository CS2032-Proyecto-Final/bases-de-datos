from airflow import DAG
from airflow.decorators import task
from airflow.hooks.base import BaseHook
from datetime import datetime
import boto3
import pandas as pd
import pymysql
from io import StringIO

# Variables globales
ATHENA_QUERY = """
SELECT 
    SPLIT_PART(r."tenant_id#type", '#', 1) AS tenant_id,
    COUNT(*) AS active_reservations
FROM 
    treservations r
WHERE 
    r.status = 'pending'
GROUP BY 
    SPLIT_PART(r."tenant_id#type", '#', 1)
ORDER BY 
    active_reservations DESC;
"""  # Replace with your query
ATHENA_DATABASE = "test-bibliokuna"  # Replace with your Athena database name
QUERY_NAME="query_4"
S3_OUTPUT_LOCATION = f"s3://athena-bibliokuna/{QUERY_NAME}/"  # Replace with your S3 output path
MYSQL_TABLE_NAME = QUERY_NAME

# Función para obtener credenciales de MySQL desde Airflow
def get_mysql_credentials():
    conn = BaseHook.get_connection("mysql_credentials")
    mysql_credentials = {
        "host": conn.host,
        "login": conn.login,
        "password": conn.password,
        "port": conn.port
    }
    return mysql_credentials

# Función para obtener credenciales de AWS desde Airflow
def get_aws_credentials():
    conn = BaseHook.get_connection("aws_credentials")
    aws_credentials = {
        "access_key": conn.login,
        "secret_access_key": conn.password,
        "session_token": conn.extra_dejson.get("aws_session_token"),
    }
    return aws_credentials

# DAG definition
dag = DAG(
    f"etl_athena_mysql_{QUERY_NAME}",
    description='Reusable ETL DAG for Athena to MySQL',
    schedule_interval='@once',
    start_date=datetime(2024, 1, 1),
    catchup=False,
)

# Tarea para extraer datos desde Athena
@task(dag=dag)
def extract_data_from_athena():
    aws_credentials = get_aws_credentials()
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_credentials["access_key"],
        aws_secret_access_key=aws_credentials["secret_access_key"],
        aws_session_token=aws_credentials["session_token"],
        region_name='us-east-1'
    )
    athena_client = boto3.client(
        'athena',
        aws_access_key_id=aws_credentials["access_key"],
        aws_secret_access_key=aws_credentials["secret_access_key"],
        aws_session_token=aws_credentials["session_token"],
        region_name='us-east-1'
    )
    
    # Ejecutar consulta en Athena
    response = athena_client.start_query_execution(
        QueryString=ATHENA_QUERY,
        QueryExecutionContext={'Database': ATHENA_DATABASE},
        ResultConfiguration={'OutputLocation': S3_OUTPUT_LOCATION}
    )
    query_execution_id = response['QueryExecutionId']

    # Esperar a que termine la consulta
    status = 'RUNNING'
    while status in ['RUNNING', 'QUEUED']:
        result = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
        status = result['QueryExecution']['Status']['State']

    if status != 'SUCCEEDED':
        raise Exception(f"Consulta fallida con estado: {status}")

    # Descargar resultados del bucket S3
    result_file = f"{S3_OUTPUT_LOCATION}{query_execution_id}.csv"
    bucket_name, key = result_file.replace("s3://", "").split("/", 1)
    response = s3_client.get_object(Bucket=bucket_name, Key=key)

    # Guardar resultados localmente
    data = response['Body'].read().decode('utf-8')
    with open(f"/tmp/extracted_data_{QUERY_NAME}.csv", 'w') as f:
        f.write(data)
    print("Datos extraídos y guardados en /tmp/extracted_data.csv")

# Tarea para transformar datos
@task(dag=dag)
def transform_data():
    # Leer el archivo CSV
    df = pd.read_csv(f"/tmp/extracted_data_{QUERY_NAME}.csv")
    # Transformación: convertir nombres de columnas a minúsculas
    df.columns = [col.lower() for col in df.columns]
    # Guardar CSV transformado
    df.to_csv(f"/tmp/transformed_data_{QUERY_NAME}.csv", index=False)
    print("Datos transformados y guardados en /tmp/transformed_data.csv")

# Tarea para cargar datos a MySQL
@task(dag=dag)
def load_data_to_mysql():
    mysql_credentials = get_mysql_credentials()
    connection = pymysql.connect(
        host=mysql_credentials["host"],
        user=mysql_credentials["login"],
        password=mysql_credentials["password"],
        port=mysql_credentials["port"],
        database="queries-bibliokuna",
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = connection.cursor()

    # Leer archivo transformado
    df = pd.read_csv(f"/tmp/transformed_data_{QUERY_NAME}.csv")

    # Crear tabla si no existe
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {MYSQL_TABLE_NAME} (
        {', '.join([f'{col} TEXT' for col in df.columns])}
    );
    """
    cursor.execute(create_table_query)

    # Insertar datos
    for _, row in df.iterrows():
        insert_query = f"""
        INSERT INTO {MYSQL_TABLE_NAME} ({', '.join(df.columns)})
        VALUES ({', '.join(['%s'] * len(row))})
        """
        cursor.execute(insert_query, tuple(row))

    connection.commit()
    cursor.close()
    connection.close()
    print("Datos cargados exitosamente a MySQL")

# Dependencias entre tareas
extract_task = extract_data_from_athena()
transform_task = transform_data()
load_task = load_data_to_mysql()

extract_task >> transform_task >> load_task
