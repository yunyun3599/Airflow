# Dag Schedule
## None
web ui에서 수동 trigger or api를 통한 trigger 등이 필요

## daily
매일 자정에 실행

### dag 실행 시점  
start_date를 2023년 1월 1일로 두었다고 할 때 dag 생성을 1월 1일 13시에 개발했다고 하면 자정이 오기 전까지 dag는 어떤 작업도 하지 않음   
daily의 자정에 도는 특성으로 인해 1월 2일 자정에 최초 실행됨  

dag는 지정된 시작 날짜로부터 매일 동일한 간격으로 Dag를 스케줄함  
Dag의 종료일을 지정하지 않으면 Dag를 끄기 전까지는 매일 Dag가 계속 실행됨  

### 예시
```
스케쥴: @daily  
dag 생성일: 2023/07/30    
dag start_date: 2023/07/28  
dag end_date: 2023/08/01  
```

위의 경우 dag 생성 후 execution_date=2023/07/28 인 dag_run 부터 수행  
7/30일에 수행 시작했으므로 7/29 dag_run까지 수행됨  
이 dag의 end_date는 2023/08/01이므로 2023/08/02되는 자정에 2023/08/01 dag가 마지막으로 수행되고 더이상 수행되지 않을 것  

## cron 기반
더 복잡한 스케줄 간격을 설정하기 위해 사용  

|\*|\*|\*|\*|\*|
|:-------:|:------:|:------:|:-----:|:--------:|
| 분(0~59) |시간(0~23)|일(1~31)|월(1~12)| 요일(0~6)|

cron job은 시간/날짜가 해당 필드의 값과 시스템 시간이 일치할 때 실행됨  
숫자 대신 asterisk로 제한되지 않은 필드로 정의 하여 신경쓰지 않는다고 표시 가능  

### 예시  
- 0 * * * * = 매시간(정시에 실행)
- 0 0 * * * = 매일(자정에 실행)
- 0 0 * * 0 = 매주(일요일 자정에 실행)
- 0 0 1 * * = 매월 1일 자정
- 45 23 * * SAT = 매주 토요일 23시 45분

### 추가 문법  
콤마(,)를 사용하여 값의 리스트를 정의하거나 대시('-')를 사용해 값으 범위를 정의하는 값의 집합을 지정 가능  
- 0 0 * * MON, WED, FRI = 매주 월, 수, 금 자정에 실행
- 0 0 * * MON-FRI = 매주 월요일부터 금요일 자정에 실행  
- 0 0,12 * * * = 매일 자정 및 오후 12시에 실행  

## Airflow 스케쥴 약어 매크로  
|  프리셋 이름  |          의미        |
|:--------:|:------------------:|
|  @once   |    1회만 실행하도록 스케쥴   |
| @hourly  |    매시간 변경 시 1회 실행  |
|  @daily  |     매일 자정에 1회 실행   |
| @weekly  |   매주 일요일 자정에 1회 실행 |
| @monthly |   매월 1일 자정에 1회 실행  |
| @yearly  | 매년 1월 1일 자정에 1회 실행 |


## 상대적인 시간 간격 설정  
3일마다 dag를 실행하고 싶은 경우 이런 스케쥴링은 cron식을 이용해 정의 불가  
이 때 사용할 수 있는 것이 `datetme.timedelta` 인스턴스  

```python
from airflow import DAG
import datetime

dag = DAG(
    dag_id="04_interval_schedule",
    schedule_interval=datetime.timedelta(days=3),
    start_date=datetime.datetime(year=2023, month=7, day=20),
    end_date=datetime.datetime(year=2023, month=7, day=29)
)
```
