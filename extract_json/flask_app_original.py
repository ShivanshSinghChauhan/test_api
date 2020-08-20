
from flask import Flask
#from airflow import operators
import inspect
import logging
import pkgutil
from neo4j import GraphDatabase
from py2neo import Graph

from importlib import import_module

#from operator_index import OperatorIndex


import json
import logging
import os

from flask import Flask, jsonify, make_response, request, send_from_directory
from flask_cors import CORS
from marshmallow.exceptions import ValidationError


from constants import ServerDefaults
from project_config import ProjectConfig
from exceptions import DagHandlerValidationError
from dag_handler import DagHandler
#from operator_index import OperatorIndex
#from app_schemas import OperatorSchema, MinimalWmlSchema
from app_schemas import MinimalWmlSchema


app = Flask(__name__)

'''
def home():
    return "Hello, World!"

_operator_index: OperatorIndex = None


def get_operator_index() -> OperatorIndex:
    global _operator_index

    if not _operator_index:
        _operator_index = OperatorIndex()
    return _operator_index

@app.route("/")
def get_operators():
    something = jsonify(get_operator_index().marshall_operator_list())

    return something, 200'''

@app.route("/v1/dags/<name>", methods=["POST"])
def post_dag(name):

    wml_dict = request.json




    try:
        wml_dict_parsed = MinimalWmlSchema().load(
            wml_dict, partial=False
        )
        print("----->", wml_dict_parsed)

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

if __name__ == "__main__":
    app = build_app(ProjectConfig, False)
    app.run(debug=True)