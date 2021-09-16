import json
import requests
class smsAlertMsg(object):
    def __init__(self, **kwargs):
        self.auth_key = "dummy"

        self.sender_id = "PUNNON"
        self.route = "PUNNON"

        self.sms_url = 'http://smsalert.co.in/api/push.json?'


    def send_sms(self, message, mobile):
        res = requests.get(self.sms_url,
                           params={'apikey': self.auth_key,
                                   'mobileno': mobile,
                                   'text': message,
                                   'sender': self.sender_id,
                                   'response': 'json'})
        return json.loads(res.content)