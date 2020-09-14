import os
from flask import Flask, jsonify

app = Flask(__name__)
app.config.from_object(__name__)
app.debug=True

import ssl

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
ssl_context.load_cert_chain(certfile="localhost.crt", keyfile='localhost.key')


@app.route('/')
def hello():
    return "Hello Flask"

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return "Post %d" % post_id


@app.route("/predict", methods=['POST', 'GET'])
def predict():
    return jsonify({'class_id' : 'IMAGE_NET_XXX', 'class_name':'Cat'})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=443, ssl_context=ssl_context)