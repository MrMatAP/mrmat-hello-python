from flask_restplus import Namespace, Resource, fields

api = Namespace('rest', description='microRPP Default REST Adapter')


@api.route('/')
class RESTAdapter(Resource):
    """
    microRPP Default REST Adapter
    """

    @api.doc('Get all known resource instances')
    def get(self):
        return {'hello': 'world'}

    @api.doc('Create a new resource instance')
    def post(self):
        return {}


@api.route('/<string:instance_id>')
class RESTAdapterInstance(Resource):

    @api.doc('Get an individual resource instance')
    def get(self, instance_id):
        return {'id': instance_id}

    @api.doc('Modify an existing resource instance')
    def put(self, instance_id):
        return {'id': instance_id}

    @api.doc('Remove an existing resource instance')
    def delete(self, instance_id):
        return {'id': instance_id}
