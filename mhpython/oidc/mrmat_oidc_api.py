
from flask import Flask, request, session, g
from flask_restplus import Resource, Api
from flask.ext.openid import OpenID

app = Flask(__name__)
api = Api(app)
oid = OpenID(app, '/tmp/foo', safe_roots=[])


@app.before_request
def lookup_current_user():
    g.user = None
    if 'openid' in session:
        openid = session['openid']
        g.user = User.query.filter_by(openid=openid).first()


@api.route('/items', '/items/<int:item_id>')
@api.doc(params={'item_id': 'The item id'})
class Items(Resource):

    items = {}

    @api.doc(id='Get items')
    def get(self):
        return self.items

    @api.doc(id='Create an item')
    def put(self, item_id):
        self.items[item_id] = request.form['data']
        return {item_id: self.items[item_id]}


def run():
    app.run(debug=True)


if __name__ == '__main__':
    run()
