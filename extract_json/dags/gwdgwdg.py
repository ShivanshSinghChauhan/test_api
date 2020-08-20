from airflow.models.dag import DAG
from airflow.models.baseoperator import BaseOperator
from airflow.models.baseoperator import BaseOperator


gwdgwdg = DAG(**{"dag_id": "gwdgwdg"})


thywtersh = BaseOperator(**{"task_id": "thywtersh"}, dag=gwdgwdg)
rtwhsrtjhtwr = BaseOperator(**{"task_id": "rtwhsrtjhtwr"}, dag=gwdgwdg)


thywtersh >> rtwhsrtjhtwr
