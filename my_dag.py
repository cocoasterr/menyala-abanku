from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.http_operator import SimpleHttpOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 3, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'my_batch_process',
    default_args=default_args,
    description='Batch process for API calls',
    schedule_interval=timedelta(days=1),  # Run the batch process daily
)

def store_auth_token(**kwargs):
    auth_token = kwargs['task_instance'].xcom_pull(task_ids='login')['token']
    kwargs['ti'].xcom_push(key='auth_token', value=auth_token)

def your_function1(**kwargs):
    # Placeholder for /daftar logic
    print("Executing /daftar")
    return {'message': 'User registered successfully'}

def your_function2(**kwargs):
    # Placeholder for /login logic
    print("Executing /login")
    return {'token': 'sample_auth_token', 'message': 'Login successful'}

# def your_function3(**kwargs):
#     auth_token = kwargs['ti'].xcom_pull(task_ids='store_auth_token', key='auth_token')
#     headers = {'Authorization': f'Bearer {auth_token}'}

#     # Placeholder for /transfer logic
#     print("Executing /transfer")
#     # Replace the URL with your actual API endpoint for /transfer
#     url = 'https://your-api-domain.com/transfer'
    
#     # The SimpleHttpOperator allows making HTTP requests
#     transfer_task = SimpleHttpOperator(
#         task_id='transfer',
#         method='POST',  # Change to your HTTP method
#         http_conn_id='http_conn_id',  # Specify your HTTP connection ID
#         endpoint=url,
#         headers=headers,
#         data={},  # Add your payload data here
#         response_check=lambda response: True if response.status_code == 200 else False,
#         dag=dag,
#     )

#     return transfer_task.execute(kwargs)

# Define tasks
start_task = DummyOperator(task_id='start', dag=dag)
end_task = DummyOperator(task_id='end', dag=dag)

task_daftar = PythonOperator(
    task_id='daftar',
    python_callable=your_function1,
    provide_context=True,
    dag=dag,
)

task_login = PythonOperator(
    task_id='login',
    python_callable=your_function2,
    provide_context=True,
    dag=dag,
)

task_store_auth_token = PythonOperator(
    task_id='store_auth_token',
    python_callable=store_auth_token,
    provide_context=True,
    dag=dag,
)

# task_transfer = PythonOperator(
#     task_id='transfer',
#     python_callable=your_function3,
#     provide_context=True,
#     dag=dag,
# )

# Set task dependencies
start_task >> task_daftar >> task_login >> task_store_auth_token >> task_transfer >> end_task
