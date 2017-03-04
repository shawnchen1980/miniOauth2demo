from flask import Flask, render_template, request, redirect, jsonify, url_for, flash


import flask
# IMPORTS FOR THIS STEP
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from apiclient import discovery
app = Flask(__name__)




# Show all restaurants
@app.route('/')
def showRestaurants():
    return render_template('test.html')

# Show all restaurants
@app.route('/oauth2callback')
def showRestaurants1():
    #return render_template('test2.html',data=flask.request.args.get('code'))
    auth_code=flask.request.args.get('code')
    
    flow = flow_from_clientsecrets(
      'client_secrets.json',
      scope='https://www.googleapis.com/auth/drive.metadata.readonly')
    flow.redirect_uri = 'http://localhost:5000/oauth2callback'
    credentials = flow.step2_exchange(auth_code)
    http_auth = credentials.authorize(httplib2.Http())
    drive = discovery.build('drive', 'v2', http_auth)
    files = drive.files().list().execute()
    return json.dumps(files)
    #try:
    #except FlowExchangeError:
    #    response = make_response(
    #        json.dumps('Failed to upgrade the authorization code.'), 401)
    #    response.headers['Content-Type'] = 'application/json'
    #    return response
    



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
