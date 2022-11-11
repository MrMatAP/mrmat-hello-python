from flask_restplus import fields
from .. import api

OSBGenericResponse = api.model('OSB Generic Response', {
    'operation': fields.String(description='An identifier to be used for polling the status of an asynchronous '
                                           'operation',
                               required=False,
                               example='task_10')
})
