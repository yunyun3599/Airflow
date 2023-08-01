import datetime as dt

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from part1.user_events.calculate_stats import calculate_stats

# schedule이 None이면 Dag가 예약 실행되지 않고, UI 또는 API를 통해서 수동으로 트리거되면 실행함
dag = DAG(
    dag_id="01_unscheduled",
    start_date=dt.datetime(2023, 7, 1),
    schedule_interval=None
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
