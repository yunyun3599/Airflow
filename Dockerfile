FROM apache/airflow:2.1.4-python3.8

USER root

RUN mkdir /temp
COPY ./entrypoint.sh /temp
RUN chmod +x /temp/entrypoint.sh

EXPOSE 8080

USER airflow
