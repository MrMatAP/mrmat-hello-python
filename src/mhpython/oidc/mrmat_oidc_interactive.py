#
# A small Flask app that allows login via OIDC
# TODO: It is next to impossible to make Flask-OIDC trust our own CA
#       REQUESTS_CA_BUNDLE is ignored and the SSL context we set up
#       below does succeed in making the app listen on TLS but fails
#       to trust its own configured CA when making a request to the
#       OIDC provider

import flask
from flask import Flask, jsonify
from flask_pyoidc.provider_configuration import ProviderConfiguration, ClientMetadata, ClientRegistrationInfo
from flask_pyoidc.user_session import UserSession
from flask_pyoidc.flask_pyoidc import OIDCAuthentication

app = Flask(__name__)
app.config.update({
    'SERVER_NAME': 'nostromo.dyn.bobeli.org:5000',
    'SECRET_KEY': 'SomethingReallySecret',

    'TESTING': True,
    'DEBUG': True,
})

client_metadata = ClientMetadata(client_id='mrmat-oidc-interactive-static',
                                 client_secret='5fa5e476-fe8d-4124-a732-e69cb49c9e64')
# TODO: This doesn't currently work, causing "ABCMeta object got multiple values for keyword argument 'redirect_uris'
#client_registration_info = ClientRegistrationInfo(client_name='mrmat-oidc-interactive-dynamic',
#                                                  client_uri='http://nostromo.dyn.bobeli.org:5000',
#                                                 contacts=['imfeldma@bobeli.org'])
config = ProviderConfiguration(issuer='https://auth.bobeli.org/auth/realms/mrmat-test',
                               #client_registration_info=client_registration_info)
                               client_metadata=client_metadata)
auth = OIDCAuthentication({'default': config}, app)


@app.route('/')
def index():
    return 'Not logged in'


@app.route('/login')
@auth.oidc_auth('default')
def login():
    user_session = UserSession(flask.session)
    return jsonify(access_token=user_session.access_token,
                   id_token=user_session.id_token,
                   userinfo=user_session.userinfo)


@app.route('/logout')
@auth.oidc_logout
def logout():
    user_session = UserSession(flask.session)
    if not user_session.is_authenticated():
        return "You have been successfully logged out"


@auth.error_view
def error(e=None, error_description=None):
    return jsonify({'error': e, 'message': error_description})


def run():
    app.run(debug=True, host='0.0.0.0')


if __name__ == '__main__':
    run()
