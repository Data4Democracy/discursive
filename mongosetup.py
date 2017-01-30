from pymongo import MongoClient


class MongoConnection():
    def __init__(self, config):
        self.connection_string = "mongodb://" + config['user'] + ":" + config['password'] + "@" + config['host'] + ":" + config['port'] + "/" + config['db']
        self.client = MongoClient(self.connection_string)
        self.db = self.client.get_default_database() # default database is the one named in the connection url

    def get_collection(self, name):
        self.collection = self.db[name]
        return self.collection

    def close_connection(self):
        self.client.close()
