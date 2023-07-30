# Airflow
airflow study

## 사용 버전

|        종류         |                      버전                      |
|:-----------------:|:--------------------------------------------:|
|      Airflow      |                    2.1.4                     |     
|      python       |                     3.8                      |   
| docker base image | `docker pull apache/airflow:2.1.4-python3.8` |  


## airflow 실행
프로젝트 루트 디렉토리에서 아래 명령어 수행  
```shell
$ docker-compose up -d
```
프로젝트 루트 디렉토리가 컨테이너 내의 `/opt/airflow/dags`에 마운트되어 프로젝트 내의 dag 파일들을 `localhost:8080`에서 웹서버를 통해 조회 가능 