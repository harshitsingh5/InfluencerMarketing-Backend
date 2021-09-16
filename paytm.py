import time
import checksum
import base64
import requests
import json
from collections import OrderedDict


currentTime = str(int(round(time.time() * 1000)))
MERCHANT_KEY = 'key_here'
def Payme(amount,number,order_id):
	requestData1 = '{"request":{"requestType": null,"merchantGuid":"dummy_guid_here","merchantOrderId":'+order_id+',"salesWalletName":"PayTM","salesWalletGuid":"dummy","payeeEmailId":null,"payeePhoneNumber":'+number+',"payeeSsoId":null,"appliedToNewUsers":"N","amount":'+amount+',"currencyCode":"INR","pendingDaysLimit":"0","callbackURL":"https://paytm.com/market/salesToUserCredit","cashbackPPIType":"0"},"metadata":"TestingData","ipAddress":"127.0.0.0:81","platformName":"PayTM","operationType":"SALES_TO_USER_CREDIT"}'
	
	checksum = checksum.generate_checksum_by_str(requestData1, MERCHANT_KEY)
	
	headers = {
	'Content-Type': 'application/json',
	'mid': 'dummy_mid',
	'checksumhash': checksum
	}
	
	r2 = requests.post('https://trust-uat.paytm.in/wallet-web/asyncSalesToUserCredit', data=requestData1, headers=headers)
	return r2


def CheckStatus(order_id):
	requestData1 = '{"request":{"requestType": "merchanttxnId","txnType":"SALES_TO_USER_CREDIT","txnId": '+order_id+',"merchantGuid" : "dummy"},"ipAddress":"127.0.0.0:81","platformName":"PayTM","operationType":"CHECK_TXN_STATUS","channel":"","version":""}'

	checksum = checksum.generate_checksum_by_str(requestData1, MERCHANT_KEY)
	
	headers = {
	'Content-Type': 'application/json',
	'mid': 'dummy_mid',
	'checksumhash': checksum
	}
	
	r2 = requests.post('https://trust-uat.paytm.in/wallet-web/txnStatusList', data=requestData1, headers=headers)
	return r2


def ExecutePaytmPayment(amount,number,order_id):
	res=Payme('\"'+amount+'\"','\"'+number+'\"','\"'+order_id+'\"')
	resJ=json.loads(res.text)
	status=CheckStatus('\"'+resJ["orderId"]+'\"')
	return json.loads(status.text)

def accept_payment_from_brand():
	data_dict = {
			'MID':'dummy_mid',
			'ORDER_ID':'accept-payment-from-brand-1',
			'TXN_AMOUNT':'1',
			'CUST_ID':'acfff@paytm.com',
			'INDUSTRY_TYPE_ID':'Retail',
			'WEBSITE':'www.xyz.com',
			'CHANNEL_ID':'WEB',
		#'CALLBACK_URL':'http://localhost/pythonKit/response.cgi',
		}
	param_dict = data_dict  
	param_dict['checksumHASH'] =checksum.generate_checksum(data_dict, MERCHANT_KEY)
	return param_dict