#! /bin/bash

airflow db init
airflow users create \
  --username yoonjae \
  --password yoonjae \
  --firstname yoonjae \
  --lastname choi \
  --role Admin \
  --email yunyun3599@gmail.com

airflow webserver &
airflow scheduler

/bin/bash
