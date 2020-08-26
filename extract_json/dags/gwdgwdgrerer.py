from airflow.models.dag import DAG
from airflow.models.baseoperator import BaseOperator
from airflow.models.baseoperator import BaseOperator


gwdgwdgrerer = DAG(**{"dag_id": "gwdgwdgrerer"})


thywtersh = BaseOperator(**{"task_id": "thywtersh"}, dag=gwdgwdgrerer)
rtwhsrtjhtwr = BaseOperator(**{"task_id": "rtwhsrtjhtwr"}, dag=gwdgwdgrerer)


thywtersh >> rtwhsrtjhtwr
