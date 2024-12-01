import boto3
import time
import os

# Configuration Variables
ATHENA_QUERY = "SELECT * FROM your_table LIMIT 100"  # Replace with your query
ATHENA_DATABASE = "your_database"  # Replace with your Athena database name
S3_OUTPUT_LOCATION = "s3://your-bucket/athena-output/"  # Replace with your S3 output path
LOCAL_OUTPUT_FILE = "/tmp/athena_query_result.csv"  # Path to save the result locally

def execute_athena_query():
    # Initialize the Athena client
    athena_client = boto3.client('athena')
    s3_client = boto3.client('s3')

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
