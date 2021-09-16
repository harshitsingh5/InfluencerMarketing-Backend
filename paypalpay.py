import paypalrestsdk
import logging

paypalrestsdk.configure({
  "mode": "live", # sandbox or live
  "client_id": "dummy_client_id",
  "client_secret": "dummy_client_secret" })


def Createpaypalpayment(item="item",amount=0.0,desc=''):
	payment = paypalrestsdk.Payment({
		"intent": "sale",
		"payer": {
			"payment_method": "paypal"},
		"redirect_urls": {
			"return_url": "http://localhost:81/payment/paypal/success",
			"cancel_url": "http://localhost:81/payment/paypal/failed"},
		"transactions": [{
			"item_list": {
				"items": [{
					"name": "item",
					"sku": "item",
					"price": str(amount),
					"currency": "INR",
					"quantity": 1}]},
			"amount": {
				"total": amount,
				"currency": "INR"},
			"description": desc}]})
	if payment.create():
		print(payment)
		for link in payment.links:
			if link.rel == "approval_url":
				approval_url = str(link.href)
				return approval_url,payment
	else:
		return str(payment.error)

def Executepayment(pid,payid):
	payment = paypalrestsdk.Payment.find(payid)
	if payment.execute({"payer_id": pid}):
		return "Payment execute successfully"
	else:
		return payment.error