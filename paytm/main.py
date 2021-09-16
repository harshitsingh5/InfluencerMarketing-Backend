import Checksum
import requests
import base64
import json


# body parameters
def brand_paytm_payment(amount,order_id,cust_id):
	# initialize a dictionary
	paytmParams = dict()
	paytmParams["body"] = {

	    # for custom checkout value is 'Payment' and for intelligent router is 'UNI_PAY'
	    "requestType" : "Payment",

	    # Find your MID in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
	    "mid" : "Studummy",

	    # Find your Website Name in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
	    "websiteName" : "www.xyz.com",

	    # Enter your unique order id
	    "orderId" : order_id,

	    # on completion of transaction, we will send you the response on this URL
	    "callbackUrl" : "www.xyz.com:81/brand-paytm-payment/response",

	    # Order Transaction Amount here
	    "txnAmount" : {

	        # Transaction Amount Value
	        "value" : amount,

	        # Transaction Amount Currency
	        "currency" : "INR",
	    },

	    # Customer Infomation here
	    "userInfo" : {

	        # unique id that belongs to your customer
	        "custId" : cust_id,
	    },
	}

	# Generate checksum by parameters we have in body
	# Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys 
	checksum = Checksum.generate_checksum_by_str(json.dumps(paytmParams["body"]), "dummy")

	# head parameters
	paytmParams["head"] = {

	    # put generated checksum value here
	    "signature"	: checksum
	}

	# prepare JSON string for request
	post_data = json.dumps(paytmParams)

	# for Staging
	url = "https://securegw.paytm.in/order/process"

	# for Production
	# url = "https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid=YOUR_MID_HERE&orderId=YOUR_ORDER_ID"

	response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
	return response



def check_status(orderId):
	# initialize a dictionary
	paytmParams = dict()
	paytmParams = dict()

	# Find your MID in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
	paytmParams["MID"] = "Studummy"

	# Enter your order id which needs to be check status for
	paytmParams["ORDERID"] = orderId

	# Generate checksum by parameters we have in body
	# Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys 
	checksum = Checksum.generate_checksum(paytmParams, "dummy")

	# put generated checksum value here
	paytmParams["CHECKSUMHASH"] = checksum

	# prepare JSON string for request
	post_data = json.dumps(paytmParams)

	# for Staging
	url = "https://securegw.paytm.in/order/status"

	# for Production
	# url = "https://securegw.paytm.in/order/status"

	response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
	return response



def execute_brand_paytm_payment(amount,order_id,cust_id):
	start=brand_paytm_payment(amount,order_id,cust_id)
	return start





























 

# MERCHANT_KEY = 'ZxW2xIGSt7NK5Zmb';
# # def brand_paytm_pay(amount,)
# data_dict = {
#             'MID':'Studen81446331199922',
#             'ORDER_ID':'dddgfgfeeed',
#             'TXN_AMOUNT':'1',
#             'CUST_ID':'acfff@paytm.com',
#             'INDUSTRY_TYPE_ID':'Retail104',
#             'WEBSITE':'www.xyz.com',
#             'CHANNEL_ID':'WEB',
# 	    #'CALLBACK_URL':'http://localhost/pythonKit/response.cgi',
#         }


# param_dict = data_dict  
# param_dict['CHECKSUMHASH'] =Checksum.generate_checksum(data_dict, MERCHANT_KEY)



#for key in param_dict:
 #   print(key.strip()+param_dict[key].strip())

# print('<h1>Merchant Check Out Page</h1></br>')
# print('<form method="post" action="https://pguat.paytm.com/oltp-web/processTransaction" name="f1">')
# for key in param_dict:
#     print('<input type="hidden" name="'+key.strip()+'"value="'+param_dict[key].strip()+'">')
# print('<script type="text/javascript">')
# print('document.f1.submit();')
# print('</script>')
# print('</form>')