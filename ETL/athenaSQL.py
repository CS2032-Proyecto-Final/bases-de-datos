import boto3
import time
import os

# Configuration Variables
ATHENA_QUERY = """SELECT 
        u.tenant_id,
        CONCAT(u.firstname, ' ', u.lastname) AS full_name,
        u.email,
        u.creation_date
    FROM 
        tusers u
    WHERE 
        u.creation_date = (SELECT MIN(creation_date) FROM tusers WHERE tenant_id = u.tenant_id)
    ORDER BY 
        u.tenant_id, u.creation_date ASC;
"""  # Replace with your query
ATHENA_DATABASE = "test-bibliokuna"  # Replace with your Athena database name
QUERY_NAME="query_1"
S3_OUTPUT_LOCATION = f"s3://athena-bibliokuna/{QUERY_NAME}"  # Replace with your S3 output path
LOCAL_OUTPUT_FILE = "./athena_query_1.csv"  # Path to save the result locally

def execute_athena_query():
    # Initialize the Athena client
    athena_client = boto3.client('athena', region_name='us-east-1')
    s3_client = boto3.client('s3', region_name='us-east-1')

    # Start Athena query execution
    response = athena_client.start_query_execution(
        QueryString=ATHENA_QUERY,
        QueryExecutionContext={'Database': ATHENA_DATABASE},
        ResultConfiguration={'OutputLocation': S3_OUTPUT_LOCATION}
    )
    query_execution_id = response['QueryExecutionId']
    print(f"Query Execution ID: {query_execution_id}")

    # Wait for the query to complete
    print("Waiting for query to complete...")
    status = 'RUNNING'
    while status in ['RUNNING', 'QUEUED']:
        result = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
        status = result['QueryExecution']['Status']['State']
        if status in ['RUNNING', 'QUEUED']:
            time.sleep(5)  # Wait before checking again

    if status != 'SUCCEEDED':
        raise Exception(f"Query failed with status: {status}")

    print("Query succeeded. Fetching result...")

    # Fetch the result file from S3
    result_file = f"{S3_OUTPUT_LOCATION}{query_execution_id}.csv"
    bucket_name, key = result_file.replace("s3://", "").split("/", 1)
    response = s3_client.get_object(Bucket=bucket_name, Key=key)

    # Save the result locally
    data = response['Body'].read().decode('utf-8')
    with open(LOCAL_OUTPUT_FILE, 'w') as f:
        f.write(data)

    print(f"Query result saved to {LOCAL_OUTPUT_FILE}")

if __name__ == "__main__":
    try:
        execute_athena_query()
    except Exception as e:
        print(f"Error: {e}")
