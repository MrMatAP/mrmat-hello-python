from flask_restplus import Namespace, Resource, fields
api = Namespace('osb', description='microRPP Default OSB Adapter')


from .model.osb_error_response import OSBErrorResponse
from .model.osb_generic_response import OSBGenericResponse
from .model.osb_provision_request import OSBProvisionRequest
from .osb_adapter import *
