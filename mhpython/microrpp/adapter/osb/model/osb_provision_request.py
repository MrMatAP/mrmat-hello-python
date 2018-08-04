from flask_restplus import fields
from .. import api

OSBProvisionRequest = api.model('OSB Provision Request', {
    'service_id': fields.String(required=True,
                                description='The ID of the service (from the catalog). MUST be globally unique. MUST '
                                            'be a non-empty string'),
    'plan_id': fields.String(required=True,
                             description='The ID of the plan (from the catalog) for which the service instance has '
                                         'been requested. MUST be unique within the service. MUST be a non-empty '
                                         'string'),
    # TODO: context & parameters
    'organization_guid': fields.String(required=False,
                                       description='Deprecated in favor of context. The platform GUID for the '
                                                   'organization under which the service instance is to be '
                                                   'provisioned. Although most brokers will not use this field, it '
                                                   'might be helpful for executing operations on a user''s behalf. '
                                                   'MUST be a non-empty string.'),
    'space_guid': fields.String(required=False,
                                description='Deprecated in favor of context. The identifier for the project space '
                                            'within the platform organization. Although most brokers will not use this '
                                            'field, it might be helpful for executing operations on a user''s behalf. '
                                            'MUST be a non-empty string.')
})
