from flask import Flask,redirect,request
from paypalpay import *
app=Flask(__name__)

@app.route("/")
def Pay():
	url,payment=Createpaypalpayment(amount=1)
	return redirect(url)

@app.route("/payment/paypal/success")
def Paypalsuccess():
	pid=request.args["PayerId"]
	payid=request.args["paymentId"]
	payment_det=Executepayment(pid,payid)
	return str(payment_det)

@app.route("/payment/paypal/failed")
def Paypalfailed():
	return "Sorry Your Transaction Failed, If amount is debited please contact support."


if __name__ == '__main__':
	app.run(port=81,host='0.0.0.0',debug=True)


@app.route("/to-verify-ugc",methods=["GET","POST"])
def to_verify_ugc():
	if request.method=="POST":
		res=[]
		data=request.json
		cc=Campaign.query.filter_by(campaign_id=data["campaign_id"]).first()
		inff=cc.influencers
		if len(inff)>0:
			for inf in inff:
				posts=inf.posts
				if len(post)==0:
					return jsonify(valid=False,err="No Posts Found")
				for post in posts:
					if not post.verified:
						res.append({"file_name":post.file_name,"pd_id":post.pd_id})
			return jsonify(valid=True,res=res)
		return jsonify(valid=False,err="No Posts Found")