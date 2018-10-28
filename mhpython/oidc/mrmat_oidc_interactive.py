#
# A small Flask app that allows login via OIDC
# TODO: It is next to impossible to make Flask-OIDC trust our own CA
#       REQUESTS_CA_BUNDLE is ignored and the SSL context we set up
#       below does succeed in making the app listen on TLS but fails
#       to trust its own configured CA when making a request to the
#       OIDC provider

from flask import Flask
from flask_oidc import OpenIDConnect
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.verify_mode = ssl.CERT_REQUIRED
context.load_verify_locations("/Users/imfeldma/var/certs/MrMatCA.pem")
context.load_cert_chain("/Users/imfeldma/var/certs/nostromo.pem", "/Users/imfeldma/var/certs/nostromo.key")

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'SomethingReallySecret',
    'TESTING': True,
    'DEBUG': True,

    'OIDC_CLIENT_SECRETS': '/Users/imfeldma/var/oidc/mrmat-oidc-interactive.json'
})
oidc = OpenIDConnect(app)


@app.route('/')
def index():
    if oidc.user_loggedin:
        return 'Welcome %s' % oidc.user_getfield('email')
    else:
        return 'Not logged in'


@app.route('/login')
@oidc.require_login
def login():
    return 'Welcome %s' % oidc.user_getfield('email')


def run():
    app.run(debug=True, host="0.0.0.0", ssl_context=context)


if __name__ == '__main__':
    run()
