import time
import checksum
import base64
import requests
import json
from collections import OrderedDict


currentTime = str(int(round(time.time() * 1000)))
MERCHANT_KEY = 'dummy'

requestData1 = '{"request":{"requestType": null,"merchantGuid":"dummy","merchantOrderId":"dummy","salesWalletName":"PayTM","salesWalletGuid":"dummy","payeeEmailId":null,"payeePhoneNumber":"7777777777","payeeSsoId":null,"appliedToNewUsers":"N","amount":"1","currencyCode":"INR","pendingDaysLimit":"0","callbackURL":"https://paytm.com/market/salesToUserCredit","cashbackPPIType":"0"},"metadata":"TestingData","ipAddress":"127.0.0.0:5000","platformName":"PayTM","operationType":"SALES_TO_USER_CREDIT"}'

checksum = checksum.generate_checksum_by_str(requestData1, MERCHANT_KEY)

headers = {
'Content-Type': 'application/json',
'mid': 'dummy',
'checksumhash': checksum
}

r2 = requests.post('https://trust-uat.paytm.in/wallet-web/asyncSalesToUserCredit', data=requestData1, headers=headers)

print(r2.status_code)
print('Request:')
print(requestData1)
print('Headers:')
print(headers)
print('Response:')
print(r2.text)