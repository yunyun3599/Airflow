import datetime as dt

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from part1.user_events.calculate_stats import calculate_stats

# schedule이 @daily이면 매일 자정에 실행됨
# airflow는 시작 날짜를 기준으로 첫 번째 DAG의 실행을 스케줄(시작 날짜 + 간격)함
# 그 후의 실행은 첫 번째 스케줄된 간격 이후 계속해서 해당 간격으로 실행됨
dag = DAG(
    dag_id="02_daily_schedule",
    schedule_interval="@daily",
    start_date=dt.datetime(year=2023, month=7, day=27),
    end_date=dt.datetime(year=2023, month=7, day=30)
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
