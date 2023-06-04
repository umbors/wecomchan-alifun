import logging
import json
import requests
import base64
import urllib

SEND_KEY = '此处改成你的sendkey'

WECOM_AGENTID = "此处改成你的应用 ID"
WECOM_SECRET = "此处改成你的应用 secret"
WECOM_ID = "此处改成你的企业 ID"


def send_to_wecom(text,wecom_cid,wecom_aid,wecom_secret,wecom_touid='@all'):
    get_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={wecom_cid}&corpsecret={wecom_secret}"
    response = requests.get(get_token_url).content
    access_token = json.loads(response).get('access_token')
    if access_token and len(access_token) > 0:
        send_msg_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
        data = {
            "touser":wecom_touid,
            "agentid":wecom_aid,
            "msgtype":"text",
            "text":{
                "content":text
            },
            "duplicate_check_interval":600
        }
        response = requests.post(send_msg_url,data=json.dumps(data)).content
        return response
    else:
        return None

def send_to_wecom_markdown(text,wecom_cid,wecom_aid,wecom_secret,wecom_touid='@all'):
    get_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={wecom_cid}&corpsecret={wecom_secret}"
    response = requests.get(get_token_url).content
    access_token = json.loads(response).get('access_token')
    if access_token and len(access_token) > 0:
        send_msg_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
        data = {
            "touser":wecom_touid,
            "agentid":wecom_aid,
            "msgtype":"markdown",
            "markdown":{
                "content":text
            },
            "duplicate_check_interval":600
        }
        response = requests.post(send_msg_url,data=json.dumps(data)).content
        return response
    else:
        return None

def send_to_wecom_pic(base64_content,wecom_cid,wecom_aid,wecom_secret,wecom_touid='@all'):
    get_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={wecom_cid}&corpsecret={wecom_secret}"
    response = requests.get(get_token_url).content
    access_token = json.loads(response).get('access_token')
    if access_token and len(access_token) > 0:
        upload_url = f'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type=image'
        upload_response = requests.post(upload_url, files={
            "picture": base64.b64decode(base64_content)
        }).json()

        logging.info('upload response: ' + str(upload_response))

        media_id = upload_response['media_id']

        send_msg_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
        data = {
            "touser":wecom_touid,
            "agentid":wecom_aid,
            "msgtype":"image",
            "image":{
                "media_id": media_id
            },
            "duplicate_check_interval":600
        }
        response = requests.post(send_msg_url,data=json.dumps(data)).content
        return response
    else:
        return None

def send_to_wecom_msgpic(title,text,picurl,wecom_cid,wecom_aid,wecom_secret,wecom_touid='@all'):
    get_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={wecom_cid}&corpsecret={wecom_secret}"
    response = requests.get(get_token_url).content
    access_token = json.loads(response).get('access_token')
    if access_token and len(access_token) > 0:
        send_msg_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
        data = {
            "touser":wecom_touid,
            "agentid":wecom_aid,
            "msgtype":"news",
            "news" : {
                "articles" : [
                    {
                        "title" : title,
                        "description" : text,
                        "picurl" : picurl
                    }
               ]
            },
            "duplicate_check_interval":600
        }
        response = requests.post(send_msg_url,data=json.dumps(data)).content
        return response
    else:
        return None

def send_to_wecom_file(base64_content,file_name,wecom_cid,wecom_aid,wecom_secret,wecom_touid='@all'):
    get_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={wecom_cid}&corpsecret={wecom_secret}"
    response = requests.get(get_token_url).content
    access_token = json.loads(response).get('access_token')
    if access_token and len(access_token) > 0:
        upload_url = f'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type=file'
        upload_response = requests.post(upload_url + "&debug=1", files={
            "media": (file_name, base64.b64decode(base64_content))  # 此处上传中文文件名文件旧版本 urllib 有 bug.
        }).json()

        logging.info('upload response: ' + str(upload_response))

        media_id = upload_response['media_id']

        send_msg_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
        data = {
            "touser":wecom_touid,
            "agentid":wecom_aid,
            "msgtype":"file",
            "file":{
                "media_id": media_id
            },
            "duplicate_check_interval":600
        }
        response = requests.post(send_msg_url,data=json.dumps(data)).content
        return response
    else:
        return None


def handler(environ, start_response):

    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
    
    request_body = environ['wsgi.input'].read(request_body_size)

    logging.info("request body: " + str(request_body))

    input_json = None

    try:
        input_json = urllib.parse.parse_qs(request_body.decode())
        for key in input_json:
            input_json[key] = input_json[key][0]
        if input_json['key'] != SEND_KEY:
            status = '403 Forbidden'
            response_headers = [('Content-type', 'text/json')]
            start_response(status, response_headers)
            return [b'{"code": -2, "msg": "invalid send key"}']

    except Exception as e:
        logging.exception(e)
        status = '403 Forbidden'
        response_headers = [('Content-type', 'text/json')]
        start_response(status, response_headers)
        return [b'{"code": -1, "msg": "invalid json input"}']

    code = 0
    msg = "ok"
    status = '200 OK'

    try:
        if 'type' not in input_json or input_json['type'] == 'text':
            result = send_to_wecom(input_json['msg'], WECOM_ID, WECOM_AGENTID, WECOM_SECRET)
        elif input_json['type'] == 'image':
            result = send_to_wecom_pic(input_json['msg'], WECOM_ID, WECOM_AGENTID, WECOM_SECRET)
        elif input_json['type'] == 'markdown':
            result = send_to_wecom_markdown(input_json['msg'], WECOM_ID, WECOM_AGENTID, WECOM_SECRET)
        elif input_json['type'] == 'news':
            result = send_to_wecom_msgpic(input_json['title'],input_json['msg'],input_json['picurl'], WECOM_ID, WECOM_AGENTID, WECOM_SECRET)   
        elif input_json['type'] == 'file':
            if 'filename' in input_json:
                result = send_to_wecom_file(input_json['msg'], input_json['filename'], WECOM_ID, WECOM_AGENTID, WECOM_SECRET)                    
            else:
                result = send_to_wecom_file(input_json['msg'], "Wepush推送", WECOM_ID, WECOM_AGENTID, WECOM_SECRET)
                msg = "filename not found. using default."
        else:
            code = -5
            msg = "invalid msg type. type should be text(default), image, markdown or file."
            status = "500 Internal Server Error"
            result = ""

        logging.info('wechat api response: ' + str(result))
        if result is None:
            status = "500 Internal Server Error"
            code = -4
            msg = "wechat api error: wrong config?"
    except Exception as e:
        status = "500 Internal Server Error"
        code = -3
        msg = "unexpected error: " + str(e)
        logging.exception(e)


    response_headers = [('Content-type', 'text/json')]
    start_response(status, response_headers)
    return [json.dumps({"code": code, "msg": msg}).encode("utf-8")]
