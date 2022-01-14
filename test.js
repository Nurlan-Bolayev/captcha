import {fetch} from 'node-fetch'

 async function fetch_captcha_code_post(url, body, method, token){
              const response_ = await fetch(url , {

                method : method,
                body : JSON.stringify(body),
                headers : {
                  'Content-Type' : 'application/json',
                  'Token' : token
                }
              

              })
              return response_.json() 

            }

let token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRob3JpemVkIjp0cnVlLCJleHAiOjE2NDIxODE2MzQsInVzZXJfaWQiOiI2MWQ1NDAyYTZjOWZkYWRkZDQ5Mzg3MGUifQ.ueJTvyxn8j-_JlBGb5gV-Syy5UeYDaAzlJEDoUBtjBY'
const post_req = fetch_captcha_code_post('https://captcha-api-qfegkg7fda-ew.a.run.app/api/v1/captchas/add', {"base64": "TEpXNDJF", "captcha": "LJW42E"} , 'post' , token)

console.log(post_req)