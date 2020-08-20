
from flask import Flask,request
import inspect
import logging
import pkgutil
from neo4j import GraphDatabase
from py2neo import Graph
from py2neo.cypher import cypher_escape
from flask import jsonify

from py2neo import Node, Relationship

#from flask import Flask, jsonify, make_response, request, send_from_directory
#from flask_cors import CORS
from extensions import neo4j
import json
import os

from flask import Flask, jsonify, make_response, request, send_from_directory
from flask_cors import CORS
from marshmallow.exceptions import ValidationError

from constants import ServerDefaults
from project_config import ProjectConfig
from exceptions import DagHandlerValidationError
from dag_handler import DagHandler
from app_schemas import MinimalWmlSchema

#from importlib import import_module

#from marshmallow.exceptions import ValidationError

'''
from operator_index import OperatorIndex



import logging


from flask import Flask, jsonify, make_response, request, send_from_directory
from flask_cors import CORS



from constants import ServerDefaults
from project_config import ProjectConfig
from exceptions import DagHandlerValidationError
from dag_handler import DagHandler
from operator_index import OperatorIndex
from app_schemas import OperatorSchema, MinimalWmlSchema'''

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"

#_operator_index: OperatorIndex = None


"""def get_operator_index() -> OperatorIndex:
    global _operator_index

    if not _operator_index:
        _operator_index = OperatorIndex()
    return _operator_index

@app.route('/')
def get_operators():
    something = jsonify(get_operator_index().marshall_operator_list())

    return something, 200

@app.route('/v1/dag/<name>', methods=["POST"])
def post_dag(name):

    wml_dict = request.json

    try:
        wml_dict_parsed = MinimalWmlSchema().load(
            wml_dict, partial=False, unknown=EXCLUDE
        )

    except ValidationError as e:
        logging.exception("Error parsing WML")
        return "Unable to deserialise WML contents", 400

    try:
        print(wml_dict_parsed) 
        dag_handler = DagHandler.load_from_wml(wml_dict_parsed)
        py_content = dag_handler.compile_to_python()
    except DagHandlerValidationError as e:
        logging.exception(f"Unable to convert WML '{name}' to DAG")
        return f"Error: {e}", 400
    except Exception as e:
        logging.exception(f"Unknwon error while converting WML {name}")
        return f"Internal error converting WML", 500

    f_path = os.path.join(
        "dags", f"{dag_handler.snake_name}.py"
    )
    with open(f_path, "w") as f:
        f.write(py_content)

    return "Created", 201"""

@app.route('/operators', methods= ["PUT"])
def update_operators():

    data = request.json

    driver = neo4j.get_db()

    session = driver.session()

    nodeID = data['operatorProperties']['NodeID']
    operatorInfo = data['operatorProperties']['operatorInfo']

    operator_update_query = 'MATCH (n:Operator) WHERE n.NodeID = $nodeID SET n.operatorInfo = $operatorInfo'

    result = session.run(operator_update_query, nodeID = nodeID, operatorInfo = operatorInfo).data()

    final = json.dumps(result)

    return final

@app.route('/operators', methods= ["GET"])
def get_db():

    driver = neo4j.get_db()

    session = driver.session() 

    get_operator_query = 'match (Operators)-[]->(o:Operator) return properties(o) AS operatorProperties'  

    operator_val  = session.run(get_operator_query).data()

    return jsonify(operator_val)


@app.route('/workflow', methods= ["POST"])
def worflowSave():

    workflow_config = request.json

    workflowID = str(workflow_config["WorkflowID"])

    WorkflowDefination = str(workflow_config["WorkflowDefination"])

    WorkflowName = str(workflow_config["WorkflowName"])

    WorkflowVersion = str(workflow_config["WorkflowVersion"])

    WorkflowDescription = str(workflow_config["WorkflowDescription"])

    driver = neo4j.get_db()

    session = driver.session()

    workflow_save_query = 'CREATE (n:SharedDataWorkFlow{WorkflowID: $workflowID, WorkflowName: $WorkflowName, WorkflowVersion: $WorkflowVersion, WorkflowDescription: $WorkflowDescription , WorkflowDefination: $WorkflowDefination }) return n;'

    result = session.run(workflow_save_query, workflowID = workflowID, WorkflowName = WorkflowName, WorkflowVersion = WorkflowVersion, WorkflowDescription = WorkflowDescription, WorkflowDefination = WorkflowDefination)

    #final_result = json.dumps(result)

    return str(result)


@app.route('/workflow', methods= ["GET"])
def getWorkflow():

    data = request.json

    driver = neo4j.get_db()

    session = driver.session()

    get_workflow_query = 'MATCH (n:SharedDataWorkFlow) RETURN properties(n) AS SharedDataWorkFlow'

    result = session.run(get_workflow_query).data()

    return str(result)

@app.route('/workflow', methods= ["PUT"])
def updateWorkflow():

    workflow_config = request.json

    WorkflowDefination = str(workflow_config["WorkflowDefination"])

    WorkflowName = str(workflow_config["WorkflowName"])

    WorkflowVersion = str(workflow_config["WorkflowVersion"])

    WorkflowDescription = str(workflow_config["WorkflowDescription"])

    driver = neo4j.get_db()

    session = driver.session()

    nodeID = workflow_config['NodeID']

    operator_update_query = 'MATCH (n:SharedDataWorkFlow) WHERE n.NodeID = $nodeID SET n.WorkflowName= $WorkflowName, n.WorkflowVersion= $WorkflowVersion, n.WorkflowDescription= $WorkflowDescription , n.WorkflowDefination= $WorkflowDefination   '

    result = session.run(operator_update_query, nodeID = nodeID,WorkflowName = WorkflowName, WorkflowVersion = WorkflowVersion, WorkflowDescription = WorkflowDescription, WorkflowDefination = WorkflowDefination)

    return str(result) 

@app.route("/v1/dags/<name>", methods=["POST"])
def post_dag(name):

    wml_dict = request.json


    try:
        wml_dict_parsed = MinimalWmlSchema().load(
            wml_dict, partial=False
        )

    except ValidationError as e:
        logging.exception("Error parsing WML")
        return "Unable to deserialise WML contents", 400

    try:
        dag_handler = DagHandler.load_from_wml(wml_dict_parsed)
        py_content = dag_handler.compile_to_python()
    except DagHandlerValidationError as e:
        logging.exception(f"Unable to convert WML '{name}' to DAG")
        return f"Error: {e}", 400
    except Exception as e:
        logging.exception(f"Unknwon error while converting WML {name}")
        return f"Internal error converting WML", 500

    f_path = os.path.join(
        "dags", f"{dag_handler.snake_name}.py"
    )

    with open(f_path, "w") as f:
        f.write(py_content)

    return "Created", 201


def build_app(proj_conf, dev_server=False):

    app.config["project_conf"] = proj_conf


    if dev_server:
        logging.warning("Running a dev-build with CORS enabled")
        CORS(app)

    return app

'''
def build_app(proj_conf, dev_server=False):
    app.config["project_conf"] = proj_conf

    if dev_server:
        logging.warning("Running a dev-build with CORS enabled")
        CORS(app)

    return app'''       


if __name__ == "__main__":

    app = build_app(ProjectConfig, False)
    app.run(host='127.0.0.1', port = 5000, debug=True)
'''
if __name__ == '__main__':
    app.run()'''




