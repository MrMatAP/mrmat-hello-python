from flask import Flask
from flask_restplus import Api, Resource, fields

from mhpython.microrpp.adapter.rest.rest_adapter import api as RESTAdapter
from mhpython.microrpp.adapter.osb import api as OSBAdapter


app = Flask(__name__)
api = Api(app, version='1.0', title='microRPP API', description='microRPP Service')
api.add_namespace(RESTAdapter, path='/rest')
api.add_namespace(OSBAdapter, path='/osb')

if __name__ == '__main__':
    app.run(debug=True)
