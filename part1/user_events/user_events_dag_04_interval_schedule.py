import datetime as dt

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from part1.user_events.calculate_stats import calculate_stats

# schedule이 timedelta인 경우
# 아래 코드의 경우 7/21, 7/24, 7/27 dag 실행
# 7/27 dag의 경우 interval이 3일이므로 7/30일에 실행됨
dag = DAG(
    dag_id="04_interval_schedule",
    schedule_interval=dt.timedelta(days=3),
    start_date=dt.datetime(year=2023, month=7, day=21),
    end_date=dt.datetime(year=2023, month=7, day=27)
)

fetch_events = BashOperator(
    task_id="fetch_events",
    bash_command=(
        "mkdir -p /home/airflow/data && "
        "curl -o /home/airflow/data/events.json "
        "http://events-api:5000/events"
    ),
    dag=dag
)

calculate_stats = PythonOperator(
    task_id="calculate_stats",
    python_callable=calculate_stats,
    op_kwargs={
        "input_path": "/home/airflow/data/events.json",
        "output_path": "/home/airflow/data/stats.csv"
    },
    dag=dag
)

fetch_events >> calculate_stats
