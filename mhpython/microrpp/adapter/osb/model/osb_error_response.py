from flask_restplus import fields
from .. import api

OSBErrorResponse = api.model('OSB Error Response', {
    'error': fields.String(description='An optional error code',
                           required=False,
                           enum=['AsyncRequired']),
    'description': fields.String(description='A meaningful error message explaining why the request has failed',
                                 example='Your account has exceeded its quota for service instances. Please contact '
                                         'support at http://support.example.com.')
})
