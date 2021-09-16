from twilio.rest import Client


def send_sms(message,number):
	account_sid = 'dummy'
	auth_token = 'dummy'
	client = Client(account_sid, auth_token)

	message = client.messages.create(
								body="Kya Haal Hai Rajjo",
								from_='+919384400000',
								to='+917398600000'
								)
	print(message.sid)