import datetime as dt

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from part1.user_events.calculate_stats import calculate_stats

# schedule이 cron식으로 표현됨
# 아래 dag는 7/10 ~ 7/29 사이의 월요일에 해당하는 날짜의 자정을 execution date로 하여 실행됨
# 따라서 7/10, 7/17, 7/24의 dag가 실행되며 7/24에 해당하는 dag는 7/31에 수행됨
dag = DAG(
    dag_id="03_cron_schedule",
    schedule_interval="0 0 * * MON",
    start_date=dt.datetime(year=2023, month=7, day=10),
    end_date=dt.datetime(year=2023, month=7, day=29)
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
