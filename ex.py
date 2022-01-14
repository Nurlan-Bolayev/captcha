from flask import Flask
from flask import render_template
from flask import request, redirect
import requests
import base64
import os
import json
import time
from werkzeug.utils import secure_filename
import random
import datetime
UPLOAD_FOLDER = 'imgs'
app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/captcha-final', methods=['post', 'get'])
def captcha_form_s():
    print('it is the start of captcha final')
    r = random.randint(0, len(os.listdir('static/imgs'))-1)
    filename = os.listdir('static/imgs')[r]
    base64encoded_img_file = ''
    with open(f'static/imgs/{filename}', 'rb') as img_file:
        base64encoded_img_file = base64.b64encode(img_file.read())

    encoded_message = base64encoded_img_file.decode('utf-8')

    app.config['no_answer'] = True
    app.config['json'] = {"base64": "TEpXNDJF", "captcha": "LJW42E"}
    print('inside captcha_final')

    class CheckCap:
        def __str__(self) -> str:
            return 'check__captcha'

        def __init__(self):
            print('initialized captcha class')
            self.base64encoded_img = encoded_message
            self.get_url = 'https://captcha-api-qfegkg7fda-ew.a.run.app/api/v1/captchas/get_answer/'
            self.post_url = 'https://captcha-api-qfegkg7fda-ew.a.run.app/api/v1/captchas/add'
            self.keys = ['request_count', 'is_succesful']
            self.post_request_ = dict()
            self.get_request_ = dict()
            self.request_detail = {}
            self.to_print_get_ = ''
            self.to_print_post_ = ''
            self.token_url = 'https://captcha-api-qfegkg7fda-ew.a.run.app/api/v1/users/authorize'
            self.token_request_body = {
                "email": "najafquliyev@gmail.com",
                "password": "12345678"
            }
            self.set_token()
            self.headers = dict()
            self.headers["Content-Type"] = "application/json"
            self.headers["Token"] = app.config['captcha_token']

            for i in self.keys:
                if i == 'is_succesful':
                    self.post_request_[i] = False
                    self.get_request_[i] = False

                elif i == 'request_count':
                    self.post_request_[i] = 0
                    self.get_request_[i] = 0
            self.request_detail['answer_is_null'] = True

        def print(self):
            return [self.to_print_get_, self.to_print_post_]

        def not_a_valid_token(self, token):
            if token == 'no answer' or not token or len(token) != 6:
                return True
            else:
                return False

        def start(self):
            return self.post_()

        def get_(self, captcha_id=None):
            print('I am in the get request')

            if not captcha_id:
                return
            else:
                r = requests.get(url=self.get_url + captcha_id,
                                 headers=self.headers, params={})

                self.get_request_['request_count'] += 1
                self.get_request_['is_succesful'] = True
                json_data = r.json()
                self.to_print_get_ = json_data
                self.get_request_.update(json_data)
                d = 'Null' if self.not_a_valid_token(
                    json_data['answer']) else json_data['answer']
                app.config['no_answer'] = True if self.not_a_valid_token(
                    json_data['answer']) else False
                if self.not_a_valid_token(json_data['answer']):
                    print('after checking token validity')
                    time.sleep(1)
                    # self.post_()
                    return render_template('menzil_form.html', data=d, filename=filename, token=app.config.get('captcha_token'))

                print('after fetching image')

        def post_(self):
            print('I \' in the post request')
            r = requests.post(url='https://captcha-api-qfegkg7fda-ew.a.run.app/api/v1/captchas/add',  headers={
                              "Content-Type": "application/json", "Token": app.config.get('captcha_token')}, json={"base64": "TEpXNDJF", "captcha": "LJW42E"})
            self.post_request_['request_count'] += 1
            json_data = r.json()
            self.to_print_post_ = json_data
            self.post_request_['is_succesful'] = True
            json_data = r.json()
            self.get_request_.update(json_data)
            data = json.dumps(json_data)
            split_1 = data.split(',')
            s = split_1[0]
            s.replace('{"', '')
            strt_idx = 0
            for i in s:
                if i.isdigit():
                    strt_idx = s.index(i)
                    break
            captcha_id = data[strt_idx:strt_idx+24]
            if r.status_code == 201:
                return self.get_(captcha_id)

        def set_token(self):
            print('I\'m in the set token function')
            if not app.config.get('captcha_token'):
                r = requests.post(url=self.token_url,
                                  json=self.token_request_body)
                json_data = r.json()
                app.config['captcha_token_settime'] = datetime.datetime.today().now()
                app.config['captcha_token'] = json_data['token']
            else:
                now = datetime.datetime.now()
                time_diff = (
                    now - app.config['captcha_token_settime']).total_seconds()
                time_diff = time_diff * 1/3600
                if time_diff > 6:
                    r = requests.post(url=self.token_url,
                                      json=self.token_request_body)
                    json_data = r.json()
                    app.config['captcha_token_settime'] = datetime.datetime.today(
                    ).now()
                    app.config['captcha_token'] = json_data['token']
                return [app.config['captcha_token_settime']]

    if app.config.get('no_answer'):
        print('ccccccccccccccccccccc')
        check_cap = CheckCap()
        print(' calling start method')
        return check_cap.start()


@app.route('/to_captcha_form')
def to_captcha_form():
    print('it is the start of captcha form')
    r = random.randint(0, len(os.listdir('static/imgs'))-1)
    filename = os.listdir('static/imgs')[r]
    base64encoded_img_file = ''
    with open(f'static/imgs/{filename}', 'rb') as img_file:
        base64encoded_img_file = base64.b64encode(img_file.read())

    encoded_message = base64encoded_img_file.decode('utf-8')

    app.config['no_answer'] = True
    app.config['post_count'] = 0
    app.config['json'] = {"base64": "TEpXNDJF", "captcha": "LJW42E"}

    class CheckCap:
        def __str__(self) -> str:
            return 'check__captcha'

        def __init__(self):
            self.token_url = 'https://captcha-api-qfegkg7fda-ew.a.run.app/api/v1/users/authorize'
            self.token_request_body = {
                "email": "najafquliyev@gmail.com",
                "password": "12345678"
            }
            self.captcha_token_settime = ''
            self.set_token()
            print(app.config['captcha_token'])
            self.headers = dict()
            self.headers["Content-Type"] = "application/json"
            self.headers["Token"] = app.config.get('captcha_token')

            self.base64encoded_img = encoded_message
            self.get_url = 'https://captcha-api-qfegkg7fda-ew.a.run.app/api/v1/captchas/get_answer/'
            self.post_url = 'https://captcha-api-qfegkg7fda-ew.a.run.app/api/v1/captchas/add'
            self.keys = ['request_count', 'is_succesful']
            self.post_request_ = dict()
            self.get_request_ = dict()
            self.request_detail = {}
            self.to_print_get_ = ''
            self.to_print_post_ = ''
            for i in self.keys:
                if i == 'is_succesful':
                    self.post_request_[i] = False
                    self.get_request_[i] = False

                elif i == 'request_count':
                    self.post_request_[i] = 0
                    self.get_request_[i] = 0
            self.request_detail['answer_is_null'] = True

        def print(self):
            return [self.to_print_get_, self.to_print_post_]

        def start(self):
            print('start function inside to cap')
            print(app.config['post_count'])
            return self.post_()

        def set_token(self):
            print('I\'m in the set token function')
            if not app.config.get('captcha_token'):
                r = requests.post(url=self.token_url,
                                  json=self.token_request_body)
                json_data = r.json()
                app.config['captcha_token'] = json_data['token']
                app.config['captcha_token_settime'] = datetime.datetime.today().now()

            else:
                now = datetime.datetime.now()
                time_diff = (now - app.config['captcha_token_settime'])
                time_diff = time_diff.total_seconds()
                time_diff = time_diff * 1/3600
                if time_diff > 6:
                    r = requests.post(url=self.token_url,
                                      json=self.token_request_body)
                    json_data = r.json()
                    app.config['captcha_token'] = json_data['token']
                    app.config['captcha_token_settime'] = datetime.datetime.today(
                    ).now()
            return [app.config['captcha_token_settime']]

        def not_a_valid_token(self, token):
            if token == 'no answer' or not token or len(token) != 6:
                return True
            else:
                return False

        def render_template(self):
            return render_template('menzil_s.html', data=app.config['d'], filename=filename)

        def get_(self, captcha_id=None):
            print('I am in the get request')

            if not captcha_id:
                return
            else:
                r = requests.get(url=self.get_url + captcha_id,
                                 headers=self.headers, params={})

                self.get_request_['request_count'] += 1
                self.get_request_['is_succesful'] = True
                json_data = r.json()
                self.to_print_get_ = json_data
                self.get_request_.update(json_data)
                d = 'Null' if self.not_a_valid_token(
                    json_data['answer']) else json_data['answer']
                app.config['d'] = d
                app.config['no_answer'] = True if self.not_a_valid_token(
                    json_data['answer']) else False

                if self.not_a_valid_token(json_data['answer']):
                    print('after checking token validity')
                    time.sleep(1)
                #    self.post_()
                    return render_template('menzil_s.html', data=d, filename=filename, token=app.config.get('captcha_token'))

                else:
                    return render_template('menzil_fo.html', data=d, filename=filename)

        def post_(self):

            print('I\'m in the post request')
            r = requests.post(url='https://captcha-api-qfegkg7fda-ew.a.run.app/api/v1/captchas/add',  headers={
                              "Content-Type": "application/json", "Token": app.config.get('captcha_token')}, json={"base64": "TEpXNDJF", "captcha": "LJW42E"})
            self.post_request_['request_count'] += 1
            json_data = r.json()
            self.to_print_post_ = json_data
            self.post_request_['is_succesful'] = True
            json_data = r.json()
            self.get_request_.update(json_data)
            data = json.dumps(json_data)
            split_1 = data.split(',')
            s = split_1[0]
            s.replace('{"', '')
            strt_idx = 0
            for i in s:
                if i.isdigit():
                    strt_idx = s.index(i)
                    break
            captcha_id = data[strt_idx:strt_idx+24]
            if r.status_code == 201:
                return self.get_(captcha_id)

    print('Initializing captcha class in to captcha form')
    if app.config.get('no_answer'):
        print('123412343124')
        check_cap = CheckCap()
        print('calling start function')
        return check_cap.start()


app.run(debug=True)
