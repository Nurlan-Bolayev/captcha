from re import I
from flask import Flask
from flask import render_template
from flask import request, redirect
import requests
import base64
import os
import sys
import json
from werkzeug.utils import secure_filename
import random
UPLOAD_FOLDER = 'imgs'
app = Flask(__name__,static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/')
def home() :
    return render_template('home.html')

@app.route('/captcha-final', methods = ['post', 'get'])
def captcha_form_s() :
    r = random.randint(0, len(os.listdir('static/imgs'))-1)
    filename = os.listdir('static/imgs')[r]
    base64encoded_img_file = ''    
    with open(f'static/imgs/{filename}', 'rb') as img_file :
        base64encoded_img_file = base64.b64encode(img_file.read())  
    
    encoded_message = base64encoded_img_file.decode('utf-8')
    
    headers = dict()
    headers["Content-Type"] = "application/json"
    headers["Token"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRob3JpemVkIjp0cnVlLCJleHAiOjE2NDIwMDUyOTUsInVzZXJfaWQiOiI2MWQ1NDAyYTZjOWZkYWRkZDQ5Mzg3MGUifQ.0cXque1UTtF_024rjiFjaEdcE8MLC57uWi7Ky_LSf-c"  

    print('oooo')
    class CheckCap :
        def __str__(self) -> str:
            return 'check__captcha' 
        def __init__(self) :
            self.base64encoded_img = encoded_message
            self.get_url = 'https://captcha-api-qfegkg7fda-ew.a.run.app/api/v1/captchas/get_answer/'
            self.post_url = 'https://captcha-api-qfegkg7fda-ew.a.run.app/api/v1/captchas/add'
            self.keys = ['request_count' , 'is_succesful']
            self.post_request_ = dict()
            self.get_request_ = dict()
            self.request_detail = {}
            self.to_print_get_ = ''
            self.to_print_post_ = ''
            
            for i in self.keys :
                if i == 'is_succesful' :
                   self.post_request_[i] = False
                   self.get_request_[i] = False
                   
                elif i == 'request_count' :
                   self.post_request_[i] = 0
                   self.get_request_[i] = 0
            self.request_detail['answer_is_null'] = True
                          
        def print(self) :
            return [self.to_print_get_ , self.to_print_post_]
              
        def start (self) :
           return self.post_()  
        def get_ (self, captcha_id = None ) :
            print('this is a get request')
            print(captcha_id)
            if not captcha_id :
                return
            else :
                r = requests.get(url = self.get_url + captcha_id, headers=headers , params= {} )
            
                self.get_request_['request_count'] += 1
                self.get_request_['is_succesful'] = True
                json_data = r.json()
                self.to_print_get_ = json_data
                self.get_request_.update(json_data)
                d = 'Null' if not json_data['answer'] else json_data
                return render_template('menzil_form.html', data = d, filename = filename)
                # if not json_data['answer'] :
                #     time.sleep(4)
                #     self.request_detail['answer_is_null'] = True
                #     xy = True
                #     # Show result on the page and refresh every 4 minutes
                #     print(self.print())
                #     return self.post_()
                # elif json_data['answer'] :
                #     self.request_detail['answer_is_null'] = False
                #     return render_template('menzil_s.html', data = json_data['answer'])
            
            

        def post_ (self) :
            print('this is a post request')
            r = requests.post(url = 'https://captcha-api-qfegkg7fda-ew.a.run.app/api/v1/captchas/add',  headers={"Content-Type" : "application/json" , "Token" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRob3JpemVkIjp0cnVlLCJleHAiOjE2NDIwMDUyOTUsInVzZXJfaWQiOiI2MWQ1NDAyYTZjOWZkYWRkZDQ5Mzg3MGUifQ.0cXque1UTtF_024rjiFjaEdcE8MLC57uWi7Ky_LSf-c"}, json={"base64" : "TEpXNDJF" , "captcha" : "LJW42E"}) 
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
            for i in s :
                if i.isdigit() :
                    strt_idx = s.index(i)
                    break
            captcha_id = data[strt_idx:strt_idx+24]
            if r.status_code == 201 :
                return self.get_(captcha_id)
        
            
    check_cap = CheckCap()
    return check_cap.start()

@app.route('/to_captcha_form')
def to_captcha_form() :
    r = random.randint(0, len(os.listdir('static/imgs'))-1)
    filename = os.listdir('static/imgs')[r]
    base64encoded_img_file = ''    
    with open(f'static/imgs/{filename}', 'rb') as img_file :
        base64encoded_img_file = base64.b64encode(img_file.read())  
    
    encoded_message = base64encoded_img_file.decode('utf-8')
    
    headers = dict()
    headers["Content-Type"] = "application/json"
    headers["Token"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRob3JpemVkIjp0cnVlLCJleHAiOjE2NDE1NzUzMzIsInVzZXJfaWQiOiI2MWQ1NDAyYTZjOWZkYWRkZDQ5Mzg3MGUifQ.HL7ZtgAOnZi30sjhMNyFCv8fLAictCBiwAgvRtg0n9Q"  

    print('oooo')
    class CheckCap :
        def __str__(self) -> str:
            return 'check__captcha' 
        def __init__(self) :
            self.base64encoded_img = encoded_message
            self.get_url = 'https://captcha-api-qfegkg7fda-ew.a.run.app/api/v1/captchas/get_answer/'
            self.post_url = 'https://captcha-api-qfegkg7fda-ew.a.run.app/api/v1/captchas/add'
            self.keys = ['request_count' , 'is_succesful']
            self.post_request_ = dict()
            self.get_request_ = dict()
            self.request_detail = {}
            self.to_print_get_ = ''
            self.to_print_post_ = ''
            
            for i in self.keys :
                if i == 'is_succesful' :
                   self.post_request_[i] = False
                   self.get_request_[i] = False
                   
                elif i == 'request_count' :
                   self.post_request_[i] = 0
                   self.get_request_[i] = 0
            self.request_detail['answer_is_null'] = True
                          
        def print(self) :
            return [self.to_print_get_ , self.to_print_post_]
              
        def start (self) :
           return self.post_()  
        def get_ (self, captcha_id = None ) :
            print('this is a get request')
            print(captcha_id)
            if not captcha_id :
                return
            else :
                r = requests.get(url = self.get_url + captcha_id, headers=headers , params= {} )
            
                self.get_request_['request_count'] += 1
                self.get_request_['is_succesful'] = True
                json_data = r.json()
                self.to_print_get_ = json_data
                self.get_request_.update(json_data)
                d = 'Null' if not json_data.get('answer') else json_data['answer']
                return render_template('menzil_s.html', data = d, filename = filename)
                # if not json_data['answer'] :
                #     time.sleep(4)
                #     self.request_detail['answer_is_null'] = True
                #     xy = True
                #     # Show result on the page and refresh every 4 minutes
                #     print(self.print())
                #     return self.post_()
                # elif json_data['answer'] :
                #     self.request_detail['answer_is_null'] = False
                #     return render_template('menzil_s.html', data = json_data['answer'])
            
            

        def post_ (self) :
            print('this is a post request')
            r = requests.post(url = 'https://captcha-api-qfegkg7fda-ew.a.run.app/api/v1/captchas/add',  headers={"Content-Type" : "application/json" , "Token" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRob3JpemVkIjp0cnVlLCJleHAiOjE2NDIwMDUyOTUsInVzZXJfaWQiOiI2MWQ1NDAyYTZjOWZkYWRkZDQ5Mzg3MGUifQ.0cXque1UTtF_024rjiFjaEdcE8MLC57uWi7Ky_LSf-c"}, json={"base64" : "TEpXNDJF" , "captcha" : "LJW42E"}) 
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
            for i in s :
                if i.isdigit() :
                    strt_idx = s.index(i)
                    break
            captcha_id = data[strt_idx:strt_idx+24]
            if r.status_code == 201 :
                return self.get_(captcha_id)
        
            
    check_cap = CheckCap()
    return check_cap.start()

app.run(debug = True)