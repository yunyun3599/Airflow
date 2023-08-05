# 데이터를 증분 방식으로 실행 일자에 해당하는 데이터만 처리

import datetime as dt

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from part1.user_events.calculate_stats import calculate_stats

# 해당 일자의 데이터만 가지고 와 처리하는 dag
# execution_date 매개변수 사용 필요
# execution_date: DAG를 시작하는 시간의 특정 날짜가 아니라 스케줄 간격으로 실행되는 시작 시간을 나타내는 타임 스탬프
# next_execution_date: 스케줄 간격의 종료 시간
# previous_execution_date: 과거의 스케줄 간격의 시작을 정의
dag = DAG(
    dag_id="05_query_with_dates",
    schedule_interval="@daily",
    start_date=dt.datetime(year=2023, month=7, day=21),
    end_date=dt.datetime(year=2023, month=7, day=27)
)

fetch_events = BashOperator(
    task_id="fetch_events",
    bash_command=(
        "mkdir -p /home/airflow/data && "
        "curl -o /home/airflow/data/events.json "
        "http://events-api:5000/events?"
        "start_date={{execution_date.strftime('%Y-%m-%d')}}"
        "&end_date={{next_execution_date.strftime('%Y-%m-%d')}}"
    ),
    dag=dag
)

'''
    다른 매개변수를 이용해 다음과 같이 표기도 가능  
    bash_command=(
        ...
        "start_date={{ds}}"
        "&end_date={{next_ds}}"
    ),
    '''

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
