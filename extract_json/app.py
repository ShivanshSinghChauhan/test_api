from flask import Flask
from extensions import neo4j

app = Flask(__name__)
neo4j.init_app(app)