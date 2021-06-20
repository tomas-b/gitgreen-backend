from flask import Flask, jsonify
import os
import requests
from flask_cors import CORS, cross_origin
import json
import random
import base64
from git import Repo
from pathlib import Path

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def homepage():
    return ';)'


@app.route('/cb/<code>')
@cross_origin()
def githubCallback(code):

    data = {
        'client_id': os.environ.get('client_id'),
        'client_secret': os.environ.get('client_secret'),
        'code': code
    }

    oauthAPI = requests.post('https://github.com/login/oauth/access_token', data=data, headers={'Accept': 'application/json'})
    oauthResponse = oauthAPI.json()

    # if 'error' in oauthResponse:
    #     return oauthResponse

    accessTokenHeader = { 'Authorization': 'token '+oauthResponse['access_token'], 'accept': 'application/vnd.github.v3+json' }
    gbUserAPI = requests.get('https://api.github.com/user', headers=accessTokenHeader).json()
    gbUserAPImail = requests.get('https://api.github.com/user/emails', headers=accessTokenHeader).json()
    username = gbUserAPI['login']
    useremail = gbUserAPImail[0]['email']

    # return oauthResponse['access_token']

    repoName = 'GG-' + ''.join(random.choice('ABCDEF1234567890') for _ in range(6))
    repoDir = os.path.join(Path().absolute(), 'repos', repoName)
    os.makedirs(repoDir)


    os.system("git config --global user.name "+username)
    os.system("git config --global user.email "+useremail)


    data = json.dumps({
        "name": repoName,
        "description": "gitgreen repooo",
        "homepage": "https://gitgreen.com"
    })

    createRepo = requests.post('https://api.github.com/user/repos', data=data, headers=accessTokenHeader)
    # return createRepo.json()#['html_url']
    urlRepo = 'https://' +username + ':' + oauthResponse['access_token'] + '@github.com/' + createRepo.json()['full_name']

    repo = Repo.clone_from(urlRepo, repoDir)

    f = open(os.path.join(repoDir, 'sup.txt'), 'w')
    f.write("sup!")
    f.close()

    repo.git.add('.')
    repo.git.commit(m='testinnn', date='2021-1-1')
    repo.git.push('-u', 'origin', 'master')

    return urlRepo


    # content = base64.b64encode("gitgreen_data".encode("ascii")).decode('ascii')
    # data = json.dumps({
    #     "message": "gitgreen is fun!",
    #     "content": content,
    #     "author": { "name":"tim", "email":"tim@tim.tim", "date": "2021-05-12T05:58:41Z"},
    #     "committer": { "name":"tim", "email":"tim@tim.tim", "date": "2021-05-12T05:58:41Z"}
    # })

    # fileURL = createRepo.json()['url'] + '/contents/data.txt'
    # # return data
    # filePut = requests.put(fileURL, data=data, headers=accessTokenHeader)

    # return filePut.json()



if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)