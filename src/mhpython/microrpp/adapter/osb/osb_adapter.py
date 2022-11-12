from flask_restplus import Resource, fields
from . import api, OSBErrorResponse, OSBGenericResponse


@api.route('/v2/catalog')
class OSBAdapterCatalog(Resource):

    catalog_model = api.parser()
    catalog_model.add_argument('X-Broker-API-Version',
                               location='headers',
                               required=True,
                               choices='2.13',
                               help='OSB API version supported by the client')

    @api.doc('Get the catalog of service and plan offerings')
    @api.response(200, 'The catalog is returned')
    @api.expect(catalog_model)
    def get(self):
        return {'get': 'catalog'}


@api.route('/v2/service_instances/<string:instance_id>/last_operation')
@api.doc(params={'instance_id': 'The instance id whose status should be polled'})
class OSBAdapterPolling(Resource):

    polling_model = api.parser()
    polling_model.add_argument('X-Broker-API-Version',
                               location='headers',
                               required=True,
                               choices='2.13',
                               help='OSB API version supported by the client')
    polling_model.add_argument('service_id', location='query', required=False,
                               help='ID of the service from the catalog. If present, MUST be a non-empty string')
    polling_model.add_argument('plan_id', location='query', required=False,
                               help='ID of the plan from the catalog. If present, MUST be a non-empty string')
    polling_model.add_argument('operation', location='query', required=False,
                               help='A broker-provided identifier for the operation. When a value for operation is '
                                    'included with asynchronous responses for provision, update and deprovision '
                                    'requests, the platform MUST provide the same value using this query parameter as '
                                    'a percent-encoded string. If present, MUST be a non-empty string')


    OSBPollingResponse = api.model('OSB Polling Response', {
        'state': fields.String(description='The current state of the asynchronous request',
                               required=True,
                               enum=['in progress', 'succeeded', 'failed'],
                               example='succeeded'),
        'description': fields.String(required=False,
                                     description='Optional details about the status of an asynchronous operation',
                                     example='The service instance has successfully been provisioned')
    })

    @api.doc('Poll the status of a previously submitted asynchronous operation')
    @api.response(200, 'The current status of the asynchronous operation is returned', OSBPollingResponse)
    @api.response(400, 'The request is malformed or missing mandatory data', model=OSBErrorResponse)
    @api.response(410, 'The resource instance has been removed already', model=OSBGenericResponse)
    @api.expect(polling_model)
    def get(self, instance_id):
        return {'poll': instance_id}


@api.route('/v2/service_instances/<string:instance_id>')
class OSBAdapterProvisioning(Resource):

    provision_model = api.parser()
    provision_model.add_argument('X-Broker-API-Version',
                                 type=str,
                                 location='headers',
                                 required=True,
                                 choices='2.13',
                                 help='OSB API version supported by the client')
    provision_model.add_argument('X-Broker-API-Originating-Entity',
                                 type=str,
                                 location='headers',
                                 required=False,
                                 help='The originating entity on whose behalf this request is raised')
    provision_model.add_argument('accepts_incomplete',
                                 type=bool,
                                 location='query',
                                 required=False,
                                 help='A value of true indicates that the marketplace and its clients support '
                                      'asynchronous broker operations. If this parameter is not included in the '
                                      'request, and the broker can only provision a service instance of the requested '
                                      'plan asynchronously, the broker MUST reject the request with a 422 '
                                      'Unprocessable Entity.')
    provision_model.add_argument('body',
                                 )

    @api.doc('Provision a new service instance',
             params={'instance_id': 'The globally unique instance_id to be created'})
    @api.response(200, 'The service instance already exists, is fully provisioned and the requested parameters are '
                       'identical to the existing service instance', model=OSBGenericResponse)
    @api.response(201, 'The service instance has been provisioned as the result of this request', model=OSBGenericResponse)
    @api.response(202, 'The service instance is being provisioned asynchronously', model=OSBGenericResponse)
    @api.response(400, 'The request is malformed or missing mandatory data', model=OSBErrorResponse)
    @api.response(422, 'This broker only supports asynchronous processing, which the client did not explicitly state '
                       'to support', model=OSBErrorResponse)
    @api.expect(provision_model)
    def put(self, instance_id):
        return {'provision': instance_id}

    @api.doc('Update an existing service instance')
    @api.param('instance_id', 'The globally unique instance id of the resource to be modified')
    def patch(self, instance_id):
        return {'modify': instance_id}

    @api.doc('Deprovision an existing service instance')
    @api.param('instance_id', 'The globally unique instance id of the resource to be removed')
    def delete(self, instance_id):
        return {'deprovision', instance_id}


@api.route('/v2/service_instances/<string:instance_id>/service_bindings/<string:binding_id>')
class OSBAdapterBinding(Resource):

    @api.doc('Bind an existing service instance')
    def put(self, instance_id, binding_id):
        return {'bind': {'instance_id': instance_id, 'binding_id': binding_id}}

    @api.doc('Unbind an existing service instance')
    def delete(self, instance_id, binding_id):
        return {'unbind': {'instance_id': instance_id, 'binding_id': binding_id}}

