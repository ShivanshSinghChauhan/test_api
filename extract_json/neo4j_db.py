from neo4j import GraphDatabase

class Neo4j:
    def __init__(self):
        self.app = None
        self.driver = None

    def init_app(self, app):
        self.app = app
        self.connect()

    def connect(self):
        uri = "bolt://ec2-52-52-87-0.us-west-1.compute.amazonaws.com:7687"
        self.driver = GraphDatabase.driver(uri, auth=("neo4j", "lottery123"))
        return self.driver

    def get_db(self):
        if not self.driver:
            return self.connect()
        return self.driver