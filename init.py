from flask import Flask,render_template,redirect,url_for,request,jsonify,send_file,session
from models import *
import uuid
import random
import string
from datetime import datetime,timedelta
from flask_marshmallow import Marshmallow
from passlib.hash import sha256_crypt
import json
import requests
from flask_migrate import Migrate
import base64
import io
import csv
import twitterapi as twapi
import youtube0 as ytapi
from paypalpay import Createpaypalpayment
from pricing import calc_price
from paytm import *

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root@localhost/xyzdb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
db.app=app

migrate = Migrate(app, db)


ma=Marshmallow(app)

class Brand_details_S(ma.ModelSchema):
	class Meta:
		model = Brand_details

class Spoc_details_S(ma.ModelSchema):
	class Meta:
		model = Spoc_details

class Influencer_details_S(ma.ModelSchema):
	class Meta:
		model = Influencer_details

# class Facebook_S(ma.ModelSchema):
#     class Meta:
#         model = Facebook

# class Instagram_S(ma.ModelSchema):
#     class Meta:
#         model = Instagram

# class Twitter_S(ma.ModelSchema):
#     class Meta:
#         model = Twitter

# class Youtube_S(ma.ModelSchema):
#     class Meta:
#         model = Youtube

class Otp_details_S(ma.ModelSchema):
	class Meta:
		model = Otp_details

# class Influencers_required_S(ma.ModelSchema):
#     class Meta:
#         model = Influencers_required

class Influencers_involved_S(ma.ModelSchema):
	class Meta:
		model = Influencers_involved

class Posts_done_S(ma.ModelSchema):
	class Meta:
		model = Posts_done

class Campaign_S(ma.ModelSchema):
	class Meta:
		model = Campaign

class Location_S(ma.ModelSchema):
	class Meta:
		model = Location


# class Platform_S(ma.ModelSchema):
#     class Meta:
#         model = Platform

class Campaign_posts_S(ma.ModelSchema):
	class Meta:
		model = Campaign_posts

class Pricing_details_S(ma.ModelSchema):
	class Meta:
		model = Pricing_details

class Payments_S(ma.ModelSchema):
	class Meta:
		model = Payments

class Notifications_S(ma.ModelSchema):
	class Meta:
		model = Notifications

class Rel_influencer_notification_S(ma.ModelSchema):
	class Meta:
		model = Rel_influencer_notification

class Rel_brand_notification_S(ma.ModelSchema):
	class Meta:
		model = Rel_brand_notification


def pass_generator(size=8, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def get_tokken(use_to):
	tokken=""
	while True:
		tokken=pass_generator()
		if use_to=="brands":
			x=Brand_details.query.filter_by(c_tokken=tokken).all()
			if len(x)==0:
				break
		else:
			x=Influencer_details.query.filter_by(c_tokken=tokken).all()
			if len(x)==0:
				break
	return tokken

def send_sms(message, mobile):
		res = requests.get('http://smsalert.co.in/api/push.json?',
						   params={'apikey': "dummy_key",
								   'mobileno': mobile,
								   'text': "You OTP for Login/Signup at xyz is "+message+".Please Note this is valid only for 2 minutes.",
								   'sender': "PUNNON",
								   'response': 'json'})
		return json.loads(res.content)



@app.route("/brand-paytm-payment")
def brand_paytm_payment():
	return render_template('paytmpayment.html',param_dict=accept_payment_from_brand())








@app.route("/pricing-calculation",methods=["POST","GET"])
def pricing_calculation():
	if request.method=="POST":
		data=request.json
		dtype,service,inf_number,followers=data["dtype"],data["service"],data["inf_number"],data["followers"]
		return jsonify(calc_price(dtype,service,inf_number,200 if followers<=500 else 1000))


@app.route("/entry-location")
def entry_location():
	with open('location.csv', 'r',encoding='windows-1252') as csvfile:
		csvreader = csv.reader(csvfile)
		for row in csvreader:
			val=row[0]
			if row[1]!="":
				val=row[1]
			l=Location(location=val)
			db.session.add(l)
	db.session.commit()
	return val

@app.route("/get-matching-locations",methods=["GET","POST"])
def  get_matching_locations():
	if request.method=="POST":
		data=request.json
		# l=Location.location.like("%"+data["search"]+"%")
		result=Location.query.all()
		final_res=[]
		for r in result:
			final_res+=[r.location]
		return jsonify(valid=True,result=final_res)




@app.route("/brandlogin",methods=["GET","POST"])
def Login():
	if request.method=="POST":
		data=request.json
		user=Brand_details.query.filter_by(email=data['email']).all()
		if len(user)==0:
			return jsonify(valid=False,err = "No such User exists")
		user=user[0]
		if sha256_crypt.verify(data['password'],user.password):
			tokken=get_tokken("brands")
			user.c_tokken=tokken
			db.session.commit()
			return jsonify(valid=True,tokken=tokken)
	else:
		return jsonify(valid=False,err = "Wrong Password")

@app.route("/brandsignup",methods=["GET","POST"])
def signup():
	# try:
	if request.method=="POST":
		data = request.json
		user=Brand_details.query.filter_by(email=data['email']).all()
		if len(user)==0:
			new_brand=Brand_details(full_name=data['full_name'],brand_name=data['brand_name'],email=data['email'],password=sha256_crypt.encrypt(data['password']),verified=0,b_wallet=0,c_tokken=get_tokken("brands"),contact_no=data["contact"])
			db.session.add(new_brand)
			db.session.commit()
			otp=random.randint(1000,9999)
			otp_obj=Otp_details(otp_for=0,brand_id=new_brand.brand_id,otp_no=otp,purpose=1,valid_till=datetime.now()+timedelta(hours=1))
			db.session.add(otp_obj)
			db.session.commit()
			#msg=Message('From xyz',sender='smtp.gmail.com',recipients=[new_brand.email])
			#msg.body="Your otp for signup: "+str(otp)
			#mail.send(msg)
			return jsonify(valid=True,tokken=new_brand.c_tokken,purpose=1)
		else:
			return jsonify(valid=False,err="Account already exits!!!")
	else:
		return jsonify(valid=False,err="Method Not Allowed!!!")
	# except:
	# 	return jsonify(valid=False,err="Some Thing Went Wrong!!!")


@app.route("/infloginstatus",methods=["GET","POST"])
def infloginstatus():
	if request.method=="POST":
		data = request.json
		c_tokken=data["tokken"]
		this_inf=Influencer_details.query.filter_by(c_tokken=c_tokken).all()
		if len(this_inf)>0:
			return jsonify(valid=True)
		else:
			return jsonify(valid=False)

@app.route("/brandloginstatus",methods=["GET","POST"])
def brandloginstatus():
	if request.method=="POST":
		data = request.json
		c_tokken=data["tokken"]
		this_inf=Brand_details.query.filter_by(c_tokken=c_tokken).all()
		if len(this_inf)>0:
			return jsonify(valid=True)
		else:
			return jsonify(valid=False)
	

@app.route("/inflogin",methods=["GET","POST"])
def inflogin():
	# try:
	if request.method=="POST":
		data = request.json
		user=Influencer_details.query.filter_by(mobile_no=data['mobile_no']).all()
		if len(user)==0:
			new_brand=Influencer_details(mobile_no=data["mobile_no"],i_wallet=0,c_tokken=get_tokken("inf"))
			db.session.add(new_brand)
			db.session.commit()
			otp=random.randint(1000,9999)
			otp_obj=Otp_details(otp_for=1,influencer_id=new_brand.influencer_id,otp_no=otp,purpose=1,valid_till=datetime.now()+timedelta(hours=1))
			db.session.add(otp_obj)
			db.session.commit()
			send_sms(str(otp),data["mobile_no"])
			return jsonify(valid=True,tokken=new_brand.c_tokken,updated=False)
		else:
			otp_no=Otp_details.query.filter_by(influencer_id=user[0].influencer_id).all()
			for ot in otp_no:
				db.session.delete(ot)
			db.session.commit()
			c_tokken=get_tokken("inf")
			user[0].c_tokken=c_tokken
			otp=random.randint(1000,9999)
			otp_obj=Otp_details(otp_for=1,influencer_id=user[0].influencer_id,otp_no=otp,purpose=1,valid_till=datetime.now()+timedelta(hours=1))
			db.session.add(otp_obj)
			db.session.commit()
			send_sms(str(otp),data["mobile_no"])
			return jsonify(valid=True,tokken=user[0].c_tokken,updated=True)
	else:
		return jsonify(valid=False,err="Method Not Allowed!!!")
	# except:
	# 	return jsonify(valid=False,err="Some Thing Went Wrong!!!")



@app.route("/verifybrand-otp",methods=["GET","POST"])
def verfiy_otp():
	# try:
	if request.method=="POST":
		data = request.json
		c_tokken=data["tokken"]
		this_brand=Brand_details.query.filter_by(c_tokken=c_tokken).first()
		otp_no=Otp_details.query.filter_by(brand_id=this_brand.brand_id).first()
		if otp_no.otp_no==int(data["otp"]):
				this_brand.verified=True
				db.session.delete(otp_no)
				db.session.commit()
				return jsonify(valid=True,verified=True)
		else:
			return jsonify(valid=False,err="Wrong OTP or OTP Expired")
	else:
			return jsonify(valid=False,err="Method Not Allowed!!!")
	# except:
	# 	return jsonify(valid=False,err=data["tokken"])

@app.route("/verify-otp-inf",methods=["GET","POST"])
def verfiy_otp_inf():
	# try:
	if request.method=="POST":
		data = request.json
		c_tokken=data["tokken"]
		this_brand=Influencer_details.query.filter_by(c_tokken=c_tokken).first()
		updated=this_brand.updated
		otp_no=Otp_details.query.filter_by(influencer_id=this_brand.influencer_id).all()[-1]
		if otp_no.otp_no==int(data["otp"]):
				this_brand.verified=True
				db.session.delete(otp_no)
				db.session.commit()
				return jsonify(valid=True,verified=True,updated=updated)
		else:
			return jsonify(valid=False,err="Wrong OTP or OTP Expired")
	else:
			return jsonify(valid=False,err="Method Not Allowed!!!")
	# except:
	# 	return jsonify(valid=False,err=data["tokken"])


@app.route("/inf-daily-task-details",methods=["GET","POST"])
def inf_daily_task_details():
	if request.method=="POST":
		data=request.json
		tokken=data["tokken"]
		post=Posts_done.query.filter_by(pd_id=data["pd_id"]).first()
		camp_sch=Campaign_S()
		post_sch=Posts_done_S()
		result=post_sch.dump(post).data
		camp_data=camp_sch.dump(post.by_influencer.registered_campaigns).data
		return jsonify(valid=True,taskdetails=result,campaign=camp_data)

@app.route("/inf-daily-task",methods=["GET","POST"])
def inf_daily_task():
	if request.method=="POST":
		data=request.json
		tokken=data["tokken"]
		inf=Influencer_details.query.filter_by(c_tokken=tokken).first()
		involve=inf.involved_in
		result=[]
		post_sch=Posts_done_S()
		for i in involve:
			for j in i.posts:
				if not j.done:
					result.append(post_sch.dump(j).data)
		return jsonify(valid=True,dailytask=result)

@app.route("/inf-live-campaign",methods=["GET","POST"])
def inf_live_campaign():
	if request.method=="POST":
		data=request.json
		tokken=data["tokken"]
		inf=Influencer_details.query.filter_by(c_tokken=tokken).first()
		involve=inf.involved_in
		campaign_schema=Campaign_S()
		result=[]
		post_files=[]
		for i in involve:
			if i.accepted:
				cc=Campaign.query.filter_by(campaign_id=i.campaign_id)
				if cc.status==1:
					result.append(campaign_schema.dump(i.registered_campaigns).data)
		return jsonify(valid=True,livecampaign=result)

@app.route("/inf-activity",methods=["GET","POST"])
def inf_activity():
	if request.method=="POST":
		data=request.json
		tokken=data["tokken"]
		inf=Influencer_details.query.filter_by(c_tokken=tokken).first()
		involve=inf.involved_in
		campaign_schema=Campaign_S()
		result=[]
		post_files=[]
		total_earning=0
		count=0
		for i in involve:
			if i.active_status==3 and i.accepted:
				total_earning+=i.amount_to_be_paid
				count+=1
				result.append({"camp":i.registered_campaigns.name,"earning":i.amount_to_be_paid})
		return jsonify(valid=True,report=result,total_earning=total_earning,count=count)


@app.route("/brand-activity",methods=["GET","POST"])
def brand_activity():
	if request.method=="POST":
		data=request.json
		tokken=data["tokken"]
		brand=Brand_details.query.filter_by(c_tokken=tokken).first()
		involve=brand.campaigns
		campaign_schema=Campaign_S()
		result=[]
		total_inf_inv=0
		count=0
		for i in involve:
			if i.active_status==3 and i.accepted:
				total_inf_inv+=i.no_of_influencers1+i.no_of_influencers2
				count+=1
				result.append({"camp":i.name,"earning":i.no_of_influencers1+i.no_of_influencers2,"campaign_id":i.campaign_id})
		return jsonify(valid=True,report=result,total_earning=total_earning,count=count)



@app.route("/inf-applied-campaign",methods=["GET","POST"])
def inf_applied_campaign():
	if request.method=="POST":
		data=request.json
		tokken=data["tokken"]
		inf=Influencer_details.query.filter_by(c_tokken=tokken).first()
		involve=inf.involved_in
		campaign_schema=Campaign_S()
		result=[]
		for i in involve:
			if not i.accepted:
				result.append(campaign_schema.dump(i.registered_campaigns).data)
		return jsonify(valid=True,appliedcampaign=result)

@app.route("/inflivecampaign",methods=["GET","POST"])
def inflivecampaign():
	if request.method=="POST":
		data=request.json
		tokken=data["tokken"]
		inf=Influencer_details.query.filter_by(c_tokken=tokken).first()
		camp=Campaign.query.all()
		campaign_schema=Campaign_S()
		result=[]
		for i in camp:
			if i.status==1:
				# if inf.location[0] in i.location and inf.interests in i.business_interest:
				if i.platform=="0" and inf.use_facebook:
					result.append(campaign_schema.dump(i).data)
				elif i.platform=="1" and inf.use_instagram:
					result.append(campaign_schema.dump(i).data)
				elif i.platform=="3" and inf.use_twitter:
					result.append(campaign_schema.dump(i).data)
				elif i.platform=="2" and inf.use_youtube:
					result.append(campaign_schema.dump(i).data)
		return jsonify(valid=True,campaigns=result)

@app.route("/submit-creative",methods=["GET","POST"])
def submit_creative():
	if request.method=="POST":
		data=request.json
		inf=Influencer_details.query.filter_by(c_tokken=data["tokken"]).first()
		infv=Influencers_involved.query.filter_by(campaign_id=data["campaign_id"],influencer_id=inf.influencer_id).first()
		post=infv.posts
		post.verified=False
		if data["text"]:
			post.post_data=data["textval"]
			db.session.commit()
		elif data["img"]:
			filename="infcreative"+str(post.pd_id)+'.jpg'
			with open('./static/storeimg/'+filename, 'wb') as f:
				f.write(imgdata)
			post.file_name=filename
			db.session.commit()
		elif data["vid"]:
			post.post_data=data["textval"]
			db.session.commit()
		return jsonify(valid=True)


@app.route("/submitspoc",methods=["GET","POST"])
def submitspoc():
	# try:
		if request.method=="POST":
			data = request.json
			brand=Brand_details.query.filter_by(c_tokken=data["tokken"]).first()
			spoc=Spoc_details(name=data["full_name"],email=data["email"],contact_no=data["number"],designation=data["desig"])
			db.session.add(spoc)
			brand.spoc.append(spoc)
			db.session.commit()
			return jsonify(valid=True,msg="SPOC Updated")
		else:
			return jsonify(valid=False,err="Method Not Allowed!!!")
	# except:
	# 	return jsonify(valid=False,err=str(data))


@app.route("/submitinf-platform",methods=["GET","POST"])
def submitinf_platform():
	try:
		if request.method=="POST":
			data = request.json
			inf=Influencer_details.query.filter_by(c_tokken=data["tokken"]).first()
			fb,insta,yt,twitter=data["fb"],data["insta"],data["yt"],data["twitter"]
			msg=""
			if fb:
				pass
	# 			inf.use_facebook=True
				# f=Facebook()
			if insta:
				inf.use_instagram=True
				msg+=" Instargram"
			if yt:
				inf.use_youtube=True
				if store_youtube_account_data(data["tokken"],data["ytid"]):
					msg+=" Youtube-Verified "
				else:
					msg+=" Youtube-Not Verified "
					return jsonify(valid=False,err="Less Youtube Followers")
			if twitter:
				inf.use_twitter=True
				foll=twapi.getfollowers(data["twitterid"])
				if foll>150:
					t=Twitter(profile_url=data["twitterid"],follower_count=foll,verified=True)
					db.session.add(t)
					inf.tw_id.append(t)
					msg+=" Twitter-Verified "
				else:
					msg+=" Twitter-Not-Verified "
					return jsonify(valid=False,err="Less Twitter Followers")
			int_details=Interest_details(user_type=1,name1=1 if 1 in data["interestselected"] else 0,name2=1 if 2 in data["interestselected"] else 0,name3=1 if 3 in data["interestselected"] else 0,name4=1 if 4 in data["interestselected"] else 0,name5=1 if 5 in data["interestselected"] else 0,name6=1 if 6 in data["interestselected"] else 0,name7=1 if 7 in data["interestselected"] else 0,name8=1 if 8 in data["interestselected"] else 0,name9=1 if 9 in data["interestselected"] else 0,name10=1 if 10 in data["interestselected"] else 0,name11=1 if 11 in data["interestselected"] else 0)
			db.session.add(int_details)
			inf.interests.append(int_details)
			db.session.commit()
			return jsonify(valid=True,msg=msg)
		else:
			return jsonify(valid=False,err="Method Not Allowed!!!")
		# except:
		# 	return jsonify(valid=False,err=str(data))
	except:
		return jsonify(valid=False,err="Something Went Wrong!!!")



@app.route("/submitcomapnydetails",methods=["GET","POST"])
def submitcomapnydetails():
	# try:
	if request.method=="POST":
		data = request.json
		brand=Brand_details.query.filter_by(c_tokken=data["tokken"]).first()
		brand.company_type=data["type"]
		brand.company_turnover=data["turnover"]
		brand.company_size=data["size"]
		brand.headquarter=data["hq"]
		brand.website_url=data["url"]
		brand.gst_no=data["gst"]
		db.session.commit()
		return jsonify(valid=True,msg="SPOC Updated")
	else:
		return jsonify(valid=False,err="Method Not Allowed!!!")
	# except:
	# 	return jsonify(valid=False,err=str(data))

@app.route("/createnewcampaign",methods=["GET","POST"])
def createnewcampaign():
	if request.method=="POST":
		data=request.json
		ids=[]
		brand=Brand_details.query.filter_by(c_tokken=data["tokken"]).first()
		if data["fb"]:
			campaign=Campaign(name=data["name"],desc=data["description"],platform=0,creative_req=data["creativereq"])
			db.session.add(campaign)
			brand.campaigns.append(campaign)
			db.session.commit()
			ids+=[campaign.campaign_id]
		if data["insta"]:
			campaign=Campaign(name=data["name"],desc=data["description"],platform=1,creative_req=data["creativereq"])
			db.session.add(campaign)
			brand.campaigns.append(campaign)
			db.session.commit()
			ids+=[campaign.campaign_id]
		if data["yt"]:
			campaign=Campaign(name=data["name"],desc=data["description"],platform=2,creative_req=data["creativereq"])
			db.session.add(campaign)
			brand.campaigns.append(campaign)
			db.session.commit()
			ids+=[campaign.campaign_id]
		if data["twitter"]:
			campaign=Campaign(name=data["name"],desc=data["description"],platform=3,creative_req=data["creativereq"])
			db.session.add(campaign)
			brand.campaigns.append(campaign)
			db.session.commit()
			ids+=[campaign.campaign_id]
		if len(ids)==0:
			return jsonify(valid=False,err="No Platform Selected")
		db.session.commit()
		return jsonify(valid=True,msg="Campaign Created",campaign_ids=ids)

@app.route("/enternewcampdetails",methods=["GET","POST"])
def enternewcampdetails():
	if request.method=="POST":
		data=request.json
		cp=None
		campaigns=data["camp_ids"]
		camp_type=data["selectedTypeval"]
		for c in campaigns:
			cc=Campaign.query.filter_by(campaign_id=c).first()
			if cc:
				if not data["req"]:
					imgdata=base64.b64decode(data["imageData"])
					filename = 'camp'+str(cc.campaign_id)+'.jpg'
					with open('./static/storeimg/'+filename, 'wb') as f:
						f.write(imgdata)
					cp=Campaign_posts(file_name=filename)
					db.session.add(cp)
					cc.posts.append(cp)
					cc.image=filename
				cc.subtype=str(camp_type)
				int_details=Interest_details(user_type=1,name1=1 if 1 in data["interestselected"] else 0,name2=1 if 2 in data["interestselected"] else 0,name3=1 if 3 in data["interestselected"] else 0,name4=1 if 4 in data["interestselected"] else 0,name5=1 if 5 in data["interestselected"] else 0,name6=1 if 6 in data["interestselected"] else 0,name7=1 if 7 in data["interestselected"] else 0,name8=1 if 8 in data["interestselected"] else 0,name9=1 if 9 in data["interestselected"] else 0,name10=1 if 10 in data["interestselected"] else 0,name11=1 if 11 in data["interestselected"] else 0)
				db.session.add(int_details)
				cc.business_interest.append(int_details)
				db.session.commit()
				if int(camp_type) in [7,8]:
					loc=Location.query.filter_by(location_id=data["location"]).first()
					cc.location.append(loc)
					db.session.commit()
		return jsonify(valid=True)

@app.route("/campaign-cost-calc",methods=["GET","POST"])
def campaign_cost_calc():
	if request.method=="POST":
		data=request.json
		estimp=0
		netcost=0
		netpayout=0
		total_inf1=0
		total_inf2=0
		total_inf3=0
		total_inf4=0
		for i in data["camp_ids"]:
			campaign=Campaign.query.filter_by(campaign_id=i).first()
			service=int(campaign.subtype)
			if service<=6:
				ttype=1
			else:
				ttype=2
				service=service-6
			if int(campaign.platform)==0:
				campaign.no_of_influencers1=int(data['fb1'])
				campaign.no_of_influencers2=int(data['fb2'])
				total_inf1+=int(data['fb1'])
				total_inf1+=int(data['fb2'])
				if int(data['fb1']) not in [0,None]:
					res1=calc_price(ttype,service,int(data['fb1']),102)
					estimp+=res1['estimp']
					netcost+=res1['netcost']
				if int(data['fb2']) not in [0,None]:
					res2=calc_price(ttype,service,int(data['fb2']),502)
					estimp+=res2['estimp']
					netcost+=res2['netcost']
			elif int(campaign.platform)==1:
				campaign.no_of_influencers1=int(data['insta1'])
				campaign.no_of_influencers2=int(data['insta2'])
				total_inf2+=int(data['insta1'])
				total_inf2+=int(data['insta2'])
				if int(data['insta1']) not in [0,None]:
					res1=calc_price(ttype,service,int(data['insta1']),102)
					estimp+=res1['estimp']
					netcost+=res1['netcost']
				if int(data['insta2']) not in [0,None]:
					res2=calc_price(ttype,service,int(data['insta2']),502)
					estimp+=res2['estimp']
					netcost+=res2['netcost']
			elif int(campaign.platform)==2:
				campaign.no_of_influencers1=int(data['yt1'])
				campaign.no_of_influencers2=int(data['yt2'])
				total_inf3+=int(data['yt1'])
				total_inf3+=int(data['yt2'])
				if int(data['yt1']) not in [0,None]:
					res1=calc_price(ttype,service,int(data['yt1']),102)
					estimp+=res1['estimp']
					netcost+=res1['netcost']
				if int(data['yt2']) not in [0,None]:
					res2=calc_price(ttype,service,int(data['yt2']),502)
					estimp+=res2['estimp']
					netcost+=res2['netcost']
			elif int(campaign.platform)==3:
				campaign.no_of_influencers1=int(data['twitter1'])
				campaign.no_of_influencers2=int(data['twitter2'])
				total_inf4+=int(data['twitter1'])
				total_inf4+=int(data['twitter2'])
				if int(data['twitter1']) not in [0,None]:
					res1=calc_price(ttype,service,int(data['twitter1']),102)
					estimp+=res1['estimp']
					netcost+=res1['netcost']
				if int(data['twitter2']) not in [0,None]:
					res2=calc_price(ttype,service,int(data['twitter2']),502)
					estimp+=res2['estimp']
					netcost+=res2['netcost']
			# netpayout+=(res1['netpayout']+res2['netpayout'])
			pd=Pricing_details(est_impression=estimp,payout=netpayout,cost=netcost)
			db.session.add(pd)
			campaign.pricing.append(pd)
			campaign.status=True
		db.session.commit()
	return jsonify(valid=True,estimp=estimp,netcost=netcost,total_inf=max([total_inf1,total_inf2,total_inf3,total_inf4]))

@app.route("/create-post",methods=["GET","POST"])
def create_post():
	if request.method=="POST":
		data=request.json
		brand=Brand_details.query.filter_by(c_tokken=data["tokken"]).first()
		if brand:
			cc=Campaign.query.filter_by(brand_id=brand.brand_id,campaign_id=data["campaign_id"]).first()
			if cc:
				post=Posts_done(rules=data['rules'],desc=data['desc'],verified=True)
				db.session.add(post)
				db.session.commit()
				imgdata=base64.b64decode(data["imageData"])
				filename = 'post'+str(cc.campaign_id)+'_'+str(post.pd_id)+'.jpg'
				with open('./static/storeimg/'+filename, 'wb') as f:
					f.write(imgdata)
				post.file_name=filename
				db.session.commit()
				for inv in cc.influencers:
					inv.posts.append(post)
				db.session.commit()
				return jsonify(valid=True)
			return jsonify(valid=False,error="No Campaign Found")
		return jsonify(valid=False,error="No Brand Found")

@app.route("/create-ugc",methods=["GET","POST"])
def create_ugc():
	if request.method=="POST":
		data=request.json
		inff=Influencer_details.query.filter_by(c_tokken=data['c_tokken'])
		inv=Influencers_involved.query.filter_by(influencer_id=inff.influencer_id,campaign_id=data["campaign_id"]).first()
		cc=Campaign.query.filter_by(campaign_id=data["campaign_id"]).first()
		if cc:
			post=Posts_done(desc=data['desc'],verified=False)
			db.session.add(post)
			db.session.commit()
			imgdata=base64.b64decode(data["imageData"])
			filename = 'post'+str(cc.campaign_id)+'_'+str(post.pd_id)+'.jpg'
			with open('./static/storeimg/'+filename, 'wb') as f:
				f.write(imgdata)
			post.file_name=file_name
			db.session.commit()
			inv.posts.append(post)
			db.session.commit()
			return jsonify(valid=True)
		return jsonify(valid=False,error="No Campaign Found")

@app.route("/to-verify-ugc",methods=["GET","POST"])
def to_verify_ugc():
	if request.method=="POST":
		res=[]
		data=request.json
		cc=Campaign.query.filter_by(campaign_id=data["campaign_id"]).first()
		inff=cc.influencers
		if len(inff)>0:
			for inf in inff:
				post=inf.posts[0]
				if not post.verified:
					res.append({"file_name":post.file_name,"pd_id":post.pd_id})
			return jsonify(valid=True,res=res)
		return jsonify(valid=False,err="No Posts Found")

@app.route("/verify-ugc",methods=["GET","POST"])
def verify_ugc():
	if request.method=="POST":
		data=request.json
		p=Posts_done.query.filter_by(pd_id=data["pd_id"]).first()
		p.verified=True
		db.session.commit()
		return jsonify(valid=True)
	else:
		return jsonify(valid=False)



@app.route("/brandprofileimageupdate",methods=["GET","POST"])
def brandprofileimageupdate():
	if request.method=="POST":
		data=request.json
		inf=Brand_details.query.filter_by(c_tokken=data["tokken"]).first()
		if inf:
			imgdata=base64.b64decode(data["imageData"])
			filename = 'brandprofile'+str(inf.brand_id)+'.jpg'
			with open('./static/storeimg/'+filename, 'wb') as f:
				f.write(imgdata)
			inf.logo=filename
			db.session.commit()
			return jsonify(valid=True,uploaded=inf.logo)
		return jsonify(valid=False,uploaded='')


@app.route("/infprofileimageupdate",methods=["GET","POST"])
def infprofileimageupdate():
	if request.method=="POST":
		data=request.json
		inf=Influencer_details.query.filter_by(c_tokken=data["tokken"]).first()
		if inf:
			imgdata=base64.b64decode(data["imageData"])
			filename = 'profile'+str(inf.influencer_id)+'.jpg'
			with open('./static/storeimg/'+filename, 'wb') as f:
				f.write(imgdata)
			inf.profile_photo=filename
			db.session.commit()
			return jsonify(valid=True,uploaded=inf.profile_photo)
		return jsonify(valid=False,uploaded='')

@app.route("/insta-get-access-token")
def insta_get_access_token():
	# access_token=request.args
	return '''  <script type="text/javascript">
				var token = window.location.href.split("access_token=")[1]; 
				window.location = "/app_response_token/" + token;
			</script> '''
	# return access_token
@app.route('/app_response_token/<token>/', methods=['GET'])
def app_response_token(token):
	url='https://api.instagram.com/v1/users/self/?access_token='+token
	uResponse = requests.get(url)
	Jresponse = uResponse.text
	d = json.loads(Jresponse)
	insta_numeric_id=(d['data']['id'])
	followers=(d['data']['counts']['followed_by'])
	if followers>100:
		insta=Instagram(access_token=token,verified=True,profile_url=insta_numeric_id,follower_count=followers)
		db.session.add(insta)
		db.session.commit()
		user=Influencer_details.query.filter_by(c_tokken=session["username"]).first()
		user.insta_id.append(insta)
		user.use_instagram=True
		db.session.commit()
		return "Success"
	else:
		return "You Have Less Followers Than Required"


@app.route("/instagram-authentication/<string:tokken>",methods=["GET","POST"])
def instagram_authentication(tokken):
	session["username"]=tokken
	return redirect("https://api.instagram.com/oauth/authorize/?client_id=dummy_id&redirect_uri=https://www.xyz.com/insta-get-access-token&response_type=token")

@app.route("/get-campaign-details",methods=["GET","POST"])
def get_campaign_details():
	data=request.json
	campaign=Campaign.query.filter_by(campaign_id=data["campaign_id"]).first()
	campaign_schema=Campaign_S()
	post_files=[]
	output=campaign_schema.dump(campaign).data
	for p in campaign.posts:
		post_files.append(p.file_name)
	return jsonify(valid=True,campaign=output,posts=post_files)

@app.route("/check-inf-platform",methods=["GET","POST"])
def check_inf_platform():
	if request.method=="POST":
		data=request.json
		inf=Influencer_details.query.filter_by(c_tokken=data["tokken"]).first()
		return jsonify(valid=True,fbverified=inf.use_facebook,instaverified=inf.use_instagram,ytverified=inf.use_youtube,twitterverified=inf.use_twitter)

@app.route("/apply-for-campaign",methods=["GET","POST"])
def apply_for_campaign():
	if request.method=="POST":
		data=request.json
		inf=Influencer_details.query.filter_by(c_tokken=data["tokken"]).first()
		campaign=Campaign.query.filter_by(campaign_id=data["campaign_id"]).first()
		req_platform=campaign.platform
		followers=0
		if req_platform==1:
			fb=Facebook.query.filter_by(influencer_id=inf.influencer_id).first()
			followers=fb.follower_count
		elif req_platform==2:
			insta=Instagram.query.filter_by(influencer_id=inf.influencer_id).first()
			followers=insta.follower_count
		elif req_platform==3:
			tw=Twitter.query.filter_by(influencer_id=inf.influencer_id).first()
			followers=tw.follower_count
		elif req_platform==4:
			yt=Youtube.query.filter_by(influencer_id=inf.influencer_id).first()
			followers=yt.subscriber_count

		if followers>=100 and followers<=500:
			x=0
			req_inf=campaign.no_of_influencers1
		elif followers>500:
			x=1
			req_inf=campaign.no_of_influencers2

		inf_inv=Influencers_involved.query.filter_by(campaign_id=data["campaign_id"],range_type=x).all()
		already_inv=len(inf_inv)
		if already_inv<req_inf:
			involve=Influencers_involved(influencer_id=inf.influencer_id,campaign_id=campaign.campaign_id,range_type=x,accepted=True)
			db.session.add(involve)
			db.session.commit()
			campaign.influencers.append(involve)
			inf.involved_in.append(involve)
			db.session.commit()
			for p in campaign.posts:
				new_post=Posts_done(file_name=p.file_name)
				db.session.add(new_post)
				db.session.commit()
				inf_inv.posts.append(new_post)
			return jsonify(valid=True)
		elif already_inv<int(1.05*req_inf):
			involve=Influencers_involved(influencer_id=inf.influencer_id,campaign_id=campaign.campaign_id,range_type=x,accepted=False)
			db.session.add(involve)
			db.session.commit()
			campaign.influencers.append(involve)
			inf.involved_in.append(involve)
			db.session.commit()
			for p in campaign.posts:
				new_post=Posts_done(file_name=p.file_name)
				db.session.add(new_post)
				db.session.commit()
				inf_inv.posts.append(new_post)
			return jsonify(valid=True)
		else:
			return jsonify(valid=False)

@app.route("/check-applied",methods=["GET","POST"])
def check_applied():
	if request.method=="POST":
		data=request.json
		inf=Influencer_details.query.filter_by(c_tokken=data["tokken"]).first()
		campaign=Campaign.query.filter_by(campaign_id=data["campaign_id"]).first()
		involve=Influencers_involved.query.filter_by(influencer_id=inf.influencer_id,campaign_id=campaign.campaign_id).all()
		if len(involve)>0:
			involve=involve[0]
			return jsonify(valid=True,status="Pending" if not involve.accepted else "Accepted",color="orange" if not involve.accepted else "green",stateval=True)
		return jsonify(valid=True,status="Apply Now",color="red",stateval=False)


@app.route("/get-campaign",methods=["GET","POST"])
def campaign():
	data=request.json
	output=[]
	brand=Brand_details.query.filter_by(c_tokken=data["tokken"]).first()
	campaigns=brand.campaigns
	campaign_schema=Campaign_S()
	# return jsonify(valid=True,campaigns=output,tokken=data["tokken"])
	count=0
	for campaign in campaigns:
		if count>20:
			break
		count+=1
		if campaign.status==1:
			output.append(campaign_schema.dump(campaign).data)
	return jsonify(valid=True,campaigns=output)



@app.route("/get-campaign-some",methods=["GET","POST"])
def campaign_some():
	data=request.json
	output=[]
	brand=Brand_details.query.filter_by(c_tokken=data["tokken"]).first()
	campaigns=brand.campaigns
	campaign_schema=Campaign_S()
	# return jsonify(valid=True,campaigns=output,tokken=data["tokken"])
	count=0
	for campaign in campaigns:
		if count>4:
			break
		count+=1
		if campaign.status==1:
			output.append(campaign_schema.dump(campaign).data)
	return jsonify(valid=True,campaigns=output)

@app.route("/brandprofile",methods=["GET","POST"])
def brandprofile():
	data=request.json
	campaigns=[]
	output=[]
	brand=Brand_details.query.filter_by(c_tokken=data["tokken"]).first()
	campaigns=brand.campaigns
	campaign_schema=Campaign_S()
	if len(campaigns)==0:
		output=["not_available.jpg"]
	else:
		for campaign in campaigns:
			if campaign.status==1:
				output+=[campaign_schema.dump(campaign).data]
	return jsonify(valid=True,brand={"fname":brand.full_name,"brand_name":brand.brand_name,"email":brand.email,"campaign":output,"b_wallet":brand.b_wallet})


@app.route("/infprofile",methods=["GET","POST"])
def infprofile():
	data=request.json
	campaigns=[]
	output=[]
	inf=Influencer_details.query.filter_by(c_tokken=data["tokken"]).first()
	campaigns=Influencers_involved.query.filter_by(influencer_id=inf.influencer_id).all()
	campaign_schema=Campaign_S()
	found=True
	if len(campaigns)==0:
		found=False
	else:
		for campaign in campaigns:
			cc=Campaign.query.filter_by(campaign_id=campaign.campaign_id).first()
			if cc.status==1:
				output+=[campaign_schema.dump(cc).data]
	return jsonify(valid=True,found=found,inf={"name":inf.name,"contact":inf.mobile_no,"email":inf.email,"campaign":output,'profile_photo':inf.profile_photo})


@app.route("/infwallet",methods=["GET","POST"])
def infwallet():
	data=request.json
	trans=[]
	inf=Influencer_details.query.filter_by(c_tokken=data["tokken"]).first()
	for i in inf.payment:
		trans+=[{"purpose":i.purpose,"amount":i.amount,"date_time":i.date_time,"transaction_id":i.transaction_id,"status":i.status}]
	return jsonify(valid=True,transactions=trans,amount=inf.i_wallet)

@app.route("/infnotifications",methods=["GET","POST"])
def infnotifications():
	data=request.json
	trans=[]
	inf=Influencer_details.query.filter_by(c_tokken=data["tokken"]).first()
	n_sch=Notifications_S()
	for i in inf.notify:
		trans.append(n_sch.dump(i.for_influencer).data)
	return jsonify(valid=True,notif=trans)


@app.route("/submitinfdetails",methods=["GET","POST"])
def submitinfdetails():
	# try:
		if request.method=="POST":
			data=request.json
			if int(data["age"])<15 or int(data["age"])>35:
				return jsonify(valid=False,err="You Do Not fall Under Required Age Limit")
			inf=Influencer_details.query.filter_by(c_tokken=data["tokken"]).first()
			inf.name=data["full_name"]
			inf.age=data["age"]
			loc=Location.query.filter_by(location=data["loc"]).first()
			inf.location.append(loc)
			inf.email=data["email"]
			inf.gender=data["gender"][0]
			# int_details=Interest_details(user_type=1,name1=1 if 1 in data["interestselected"] else 0,name2=1 if 2 in data["interestselected"] else 0,name3=1 if 3 in data["interestselected"] else 0,name4=1 if 4 in data["interestselected"] else 0,name5=1 if 5 in data["interestselected"] else 0,name6=1 if 6 in data["interestselected"] else 0,name7=1 if 7 in data["interestselected"] else 0,name8=1 if 8 in data["interestselected"] else 0,name9=1 if 9 in data["interestselected"] else 0,name10=1 if 10 in data["interestselected"] else 0,name11=1 if 11 in data["interestselected"] else 0)
			# db.session.add(int_details)
			# inf.interests.append(int_details)
			inf.updated=True
			db.session.commit()
			return jsonify(valid=True,msg="Updated")
		else:
			return jsonify(valid=False,err="Method Not Allowed")
	# except:
	# 	return jsonify(valid=False,err=data["loc"])


@app.route("/brandnotification",methods=["GET","POST"])
def brandnotification():
	data=request.json
	brand=Brand_details.query.filter_by(c_tokken=data["tokken"]).first()
	notifications=brand.notify
	notification_schema=Notifications_S()
	out=[]
	if len(notifications)!=0:
		for n in notifications:
			out+=[notification_schema.dump(n.for_brand).data]
	return jsonify(valid=True,notifications=out)


@app.route("/brandlogout",methods=["GET","POST"])
def brandlogout():
	data=request.json
	brand=Brand_details.query.filter_by(c_tokken=data["tokken"]).first()
	brand.c_tokken=""
	db.session.commit()
	return jsonify(valid=True,msg="Logged Out")

@app.route("/inflogout",methods=["GET","POST"])
def inflogout():
	data=request.json
	inf=Influencer_details.query.filter_by(c_tokken=data["tokken"]).first()
	inf.c_tokken=""
	db.session.commit()
	return jsonify(valid=True,msg="Logged Out")


@app.route("/brand-payment/<string:tokken>/<string:amount>",methods=["GET","POST"])
def req_payment(tokken,amount):
		brand=Brand_details.query.filter_by(c_tokken=tokken).all()
		if len(brand)==0:
			return jsonify(valid=False,msg="You are logged Out")
		brand=brand[0]
		red_url,pay=Createpaypalpayment(item="Campaign",amount=amount,desc="Payment for campaign")
		payment=Payments(pay_type=0,mode="Paypal",amount=amount,date_time=datetime.now(),purpose="Payment For Campaign",transaction_id=pay["id"],links=red_url,payment_detail_data=str(pay),status=pay["state"])
		db.session.add(payment)
		db.session.commit()
		brand.payment.append(payment)
		db.session.commit()
		return redirect(red_url)


@app.route("/inf-payment-final",methods=["GET","POST"])
def req_payment():
	data=request.json
	tokken=data["tokken"]
	amount=data["amount"]
	number=data["number"]
	inf=Influencer_details.query.filter_by(c_tokken=tokken).first()
	order_id="Paytm_xyz_"+str(len(Payments.query.all())+1)
	res=ExecutePaytmPayment(str(amount),str(number),str(order_id))
	payment=Payments(pay_type=1,mode="Paytm",amount=amount,date_time=datetime.now(),purpose="Transfer To Paytm Wallet",transaction_id=str(order_id),payment_detail_data=str(res),status=res["statusMessage"])
	db.session.add(payment)
	db.session.commit()
	inf.payment.append(payment)
	db.session.commit()
	return res["statusMessage"]


@app.route("/")
@app.route("/bestinfluencers",methods=["GET","POST"])
def bestinfluencers():
	influencers=Influencer_details.query.limit(5).all()
	# influencers=[{"image":"bi.png"},{"image":"bi.png"},{"image":"bi.png"}]
	result=[]
	for i in influencers:
		if len(result)>4:
			break
		result.append({"name":i.name,"profile_photo":i.profile_photo,"age":i.age,"influencer_id":i.influencer_id})
	return jsonify(valid=True,bestinfluencers=result,err="some err")

@app.route("/influencers-all",methods=["GET","POST"])
def influencers_all():
	influencers=Influencer_details.query.limit(100).all()
	# out=[{"influencer_id":"influencer.influencer_id","image":"os.jpg","name":"influencer.name","city":"influencer.city","facebook_count":"influencer.facebook","instagram_count":"influencer.instagram","youtube_count":"influencer.youtube","twitter_count":"influencer.twitter"}]
	out=[]
	for influencer in influencers:
		if len(out)>15:
			break
		out+=[{"influencer_id":influencer.influencer_id,"image":influencer.profile_photo,"name":influencer.name,"gender":influencer.gender,"use_facebook":influencer.use_facebook,"use_instagram":influencer.use_instagram,"use_twitter":influencer.use_twitter,"use_youtube":influencer.use_youtube}]
	return jsonify(valid=True,influencers=out,err="some err")



@app.route("/xyzsuccess",methods=["GET","POST"])
def xyzsuccess():
	xyzsuccess=[{"image":"os.jpg"},{"image":"os.jpg"}]
	return jsonify(valid=True,oursuccess=xyzsuccess,err="some err")



@app.route("/get-image/<string:name>",methods=["GET","POST"])
def get_image(name):
	try:
		filename=name
		return send_file('./static/storeimg/'+filename, mimetype='image')
	except:
		return send_file('./static/storeimg/'+"defaultprof.jpg", mimetype='image')
@app.route("/get-image1/<int:cp_id>",methods=["GET","POST"])
def get_image1(cp_id):
	file=Campaign_posts.query.filter_by(cp_id=cp_id).first().file
	return send_file(base64.b64encode(file))

@app.route("/cal-camp-data")
def cal_camp_data():
	data=request.json
	r1,d1,b1=reach_duration_budget(data["fb1"],data["fb2"],data["fb3"],data["fb4"],data["fb5"],data["fb6"])
	r2,d2,b2=reach_duration_budget(data["insta1"],data["insta2"],data["insta3"],data["insta4"],data["insta5"],data["insta6"])
	r3,d3,b3=reach_duration_budget(data["yt1"],data["yt2"],data["yt3"],data["yt4"],data["yt5"],data["yt6"])
	r4,d4,b4=reach_duration_budget(data["twitter1"],data["twitter2"],data["twitter3"],data["twitter4"],data["twitter5"],data["twitter6"])
	return jsonify(valid=True,budget=b1+b2+b3+b4+b5+b6,duration=d1+d2+d3+d4+d5+d6,reach=r1+r2+r3+r4+r5+r6)

@app.route("/campaign-involvement-details",methods=["GET","POST"])
def campaign_involvement_details():
	if request.method=="POST":
		data=request.json
		fbr=Influencers_required(range1=data["fb1"],range2=data["fb2"],range3=data["fb3"],range4=data["fb4"],range5=data["fb5"],range6=data["fb6"],total=data["fbn"])
		instar=Influencers_required(range1=data["insta1"],range2=data["insta2"],range3=data["insta3"],range4=data["insta4"],range5=data["insta5"],range6=data["insta6"],total=data["instan"])
		ytr=Influencers_required(range1=data["yt1"],range2=data["yt2"],range3=data["yt3"],range4=data["yt4"],range5=data["yt5"],range6=data["yt6"],total=data["ytn"])
		twitterr=Influencers_required(range1=data["twitter1"],range2=data["twitter2"],range3=data["twitter3"],range4=data["twitter4"],range5=data["twitter5"],range6=data["twitter6"],total=data["twittern"])
		db.session.add(ytr)
		db.session.add(fbr)
		db.session.add(instar)
		db.session.add(twitterr)
		brand=Brand_details.query.filter_by(c_tokken=data["tokken"]).first()
		campaigns=data["camp_ids"]
		for c in campaigns:
			cc=Campaign.query.filter_by(campaign_id=c).first()
			if cc.brand_id==brand.brand_id:
				if cc.platform==0:
					cc.no_of_influencers.append(fbr)
					cc.est_budget,cc.est_duration,cc.est_reach=reach_duration_budget(data["fb1"],data["fb2"],data["fb3"],data["fb4"],data["fb5"],data["fb6"])
				elif cc.platform==1:
					cc.no_of_influencers.append(instar)
					cc.est_budget,cc.est_duration,cc.est_reach=reach_duration_budget(data["insta1"],data["insta2"],data["insta3"],data["insta4"],data["insta5"],data["insta6"])
				elif cc.platform==2:
					cc.no_of_influencers.append(ytr)
					cc.est_budget,cc.est_duration,cc.est_reach=reach_duration_budget(data["yt1"],data["yt2"],data["yt3"],data["yt4"],data["yt5"],data["yt6"])
				elif cc.platform==3:
					cc.no_of_influencers.append(twitterr)
					cc.est_budget,cc.est_duration,cc.est_reach=reach_duration_budget(data["twitter1"],data["twitter2"],data["twitter3"],data["twitter4"],data["twitter5"],data["twitter6"])
				db.session.commit()
			else:
				return jsonify(valid=False,err="Not Authorized")
		return jsonify(valid=True,camp_ids=data["camp_ids"])
	else:
		return jsonify(valid=False,err="Method Not Allowed")


if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0',port=5000)

@app.route("/inf-not-token",methods=["GET","POST"])
def inf_notif_token():
	data=request.json
	tokken=data["tokken"]
	inf=Influencer_details.query.filter_by(c_tokken=tokken).first()
	if inf.not_token:	
		return jsonify(valid=True)
	else:
		return jsonify(valid=False)



@app.route("/inf-gzid-wallet",methods=["GET","POST"])
def inf_gzid_wallet():
	data=request.json
	tokken=data["tokken"]
	inf=Influencer_details.query.filter_by(c_tokken=tokken).first()
	imgdata=base64.b64decode(data["imageData"])
	filename = 'infcard'+str(inf.influencer_id)+'.jpg'
	with open('./static/storeimg/'+filename, 'wb') as f:
		f.write(imgdata)
	return jsonify(valid=True,msg="http://xyz.com:81/get-image/"+filename)






@app.route("/fb-authenticate",methods=["GET","POST"])
def fb_authenticate():
	return """<html>
				<head></head>
				<body>
					<script>
					window.fbAsyncInit = function() {
					FB.init({
					appId      : 'dummy_app_id',
					xfbml      : true,
					version    : 'v4.0'
					});
					FB.AppEvents.logPageView();
					};

					(function(d, s, id){
					var js, fjs = d.getElementsByTagName(s)[0];
					if (d.getElementById(id)) {return;}
					js = d.createElement(s); js.id = id;
					js.src = "https://connect.facebook.net/en_US/sdk.js";
					fjs.parentNode.insertBefore(js, fjs);
					}(document, 'script', 'facebook-jssdk'));
				</script>
				</body>
			</html>"""




@app.route("/register/push-token",methods=["GET","POST"])
def register_push_token():
	data=request.json
	tokken=data["tokken"]
	push_tokken=data["push_tokken"]
	inf=Influencer_details.query.filter_by(c_tokken=tokken).first()
	if push_tokken is not inf.not_token:
		send_push_message(push_tokken,"Welcome "+str(inf.name.split(" ")[0])+"! You have been successfully registered with xyz. Your id card can be downloaded from your profile on to your device.")
	inf.not_token=push_tokken
	db.session.commit()
	return jsonify(valid=True)

@app.route("/send-push-notification-inf",methods=["GET","POST"])
def send_push_notification_inf():
	if request.method=="POST":
		passwd=request.form["passwd"]
		msg=request.form["msg"]
		if passwd=="welcome@xyz$360":
			inf_all=Influencer_details.query.filter_by(not_token is not None).all()
			for inf in inf_all:
				send_push_notif(inf,msg)
			return "Notifications Has been Sent!!!"
		else:
			return "Wrong Password"
	else:
		return "That Was A Good Fun"
@app.route("/send-notification-inf",methods=["GET","POST"])
def send_notification_inf():
	return render_template("notify.html")


@app.route("/get-image1/<string:name>",methods=["GET","POST"])
def get_image1(name):
# 	try:
		filename=name
		with open('./static/storeimg/'+filename, "rb") as image_file:
			encoded_string = base64.b64encode(image_file.read())
			base64_string = base64_bytes.decode(encoded_string)
			return jsonify(valid=True,inbase=base64_string)
# 	except:
# 		return jsonify(valid=False,err="Something Went Wrong!!!")



@app.route("/apply-for-campaign",methods=["GET","POST"])
def apply_for_campaign():
	# try:
		if request.method=="POST":
			data=request.json
			inf=Influencer_details.query.filter_by(c_tokken=data["tokken"]).first()
			campaign=Campaign.query.filter_by(campaign_id=data["campaign_id"]).first()
			infinv=Influencers_involved.query.filter_by(influencer_id=inf.influencer_id,campaign_id=campaign.campaign_id).all()
			if len(infinv)>0:
				return jsonify(valid=False,err=" You Have Already Applied ")
			req_platform=campaign.platform
			followers=0
			if req_platform==0:
				fb=Facebook.query.filter_by(influencer_id=inf.influencer_id).first()
				followers=fb.follower_count
			elif req_platform==1:
				insta=Instagram.query.filter_by(influencer_id=inf.influencer_id).first()
				followers=insta.follower_count
			elif req_platform==3:
				tw=Twitter.query.filter_by(influencer_id=inf.influencer_id).first()
				followers=tw.follower_count
			elif req_platform==2:
				yt=Youtube.query.filter_by(influencer_id=inf.influencer_id).first()
				followers=yt.subscriber_count

			if followers>=100 and followers<=500:
				x=0
				req_inf=campaign.no_of_influencers1
			elif followers>500:
				x=1
				req_inf=campaign.no_of_influencers2

			inf_inv=Influencers_involved.query.filter_by(campaign_id=data["campaign_id"],range_type=x).all()
			already_inv=len(inf_inv)
			if already_inv<req_inf:
				involve=Influencers_involved(influencer_id=inf.influencer_id,campaign_id=campaign.campaign_id,range_type=x,accepted=True)
				db.session.add(involve)
				db.session.commit()
				campaign.influencers.append(involve)
				inf.involved_in.append(involve)
				db.session.commit()
				if int(campaign.subtype)==4 or int(campaign.subtype)==6:
					send_push_notif(inf,"Your application has been accepted. Please Perform the Action As Soon As Possible.")
					return jsonify(valid=True)
				for p in campaign.posts:
					new_post=Posts_done(file_name=p.file_name)
					db.session.add(new_post)
					db.session.commit()
					involve.posts.append(new_post)
					db.session.commit()
				send_push_notif(inf,"Your application has been accepted. Please Perform the Action As Soon As Possible.")
				return jsonify(valid=True)
			elif already_inv<int(1.05*req_inf):
				involve=Influencers_involved(influencer_id=inf.influencer_id,campaign_id=campaign.campaign_id,range_type=x,accepted=False)
				db.session.add(involve)
				db.session.commit()
				campaign.influencers.append(involve)
				inf.involved_in.append(involve)
				db.session.commit()
				for p in campaign.posts:
					new_post=Posts_done(file_name=p.file_name)
					db.session.add(new_post)
					db.session.commit()
					involve.posts.append(new_post)
					db.session.commit()
					send_push_notif(inf,"Your application is pending.")
				return jsonify(valid=True)
			else:
				send_push_notif(inf,"Regret! Number of applications have reached the limit.")
				return jsonify(valid=False)
	# except:
	# 	return jsonify(valid=False,err="Something Went Wrong!!!")

@app.route('/check-inf-platform-facebook', methods=['GET'])
def app_response_token(token):
	data=request.json
	followers=200
	if followers>100:
		fb=Facebook(access_token=data['fbtoken'],verified=True,follower_count=followers)
		db.session.add(fb)
		db.session.commit()
		user=Influencer_details.query.filter_by(c_tokken=data['tokken']).first()
		user.fb_id.append(fb)
		user.use_facebook=True
		db.session.commit()
		return "Success"
	else:
		return "You Have Less Followers Than Required"


@app.route("/createnewcampaign",methods=["GET","POST"])
def createnewcampaign():
	try:
		if request.method=="POST":
			data=request.json
			ids=[]
			camp_type=data["selectedTypeval"]
			caption=data["caption"]
			app_token=data["uniquetoken"]
			link=data["link"]
			brand=Brand_details.query.filter_by(c_tokken=data["tokken"]).first()
			if data["fb"]:
				campaign=Campaign(name=data["name"],desc=data["description"],platform=0,creative_req=data["creativereq"],subtype=str(camp_type),linktoshare=link,caption=caption)
				db.session.add(campaign)
				brand.campaigns.append(campaign)
				db.session.commit()
				if int(camp_type) in [7,8]:
					loc=Location.query.filter_by(location_id=data["location"]).first()
					campaign.location.append(loc)
					db.session.commit()
				ids+=[campaign.campaign_id]
			if data["insta"]:
				campaign=Campaign(name=data["name"],desc=data["description"],platform=1,creative_req=data["creativereq"],subtype=str(camp_type),linktoshare=link,caption=caption)
				db.session.add(campaign)
				brand.campaigns.append(campaign)
				db.session.commit()
				if int(camp_type) in [7,8]:
					loc=Location.query.filter_by(location_id=data["location"]).first()
					campaign.location.append(loc)
					db.session.commit()
				ids+=[campaign.campaign_id]
			if data["yt"]:
				campaign=Campaign(name=data["name"],desc=data["description"],platform=2,creative_req=data["creativereq"],subtype=str(camp_type),linktoshare=link,caption=caption)
				db.session.add(campaign)
				brand.campaigns.append(campaign)
				db.session.commit()
				if int(camp_type) in [7,8]:
					loc=Location.query.filter_by(location_id=data["location"]).first()
					campaign.location.append(loc)
					db.session.commit()
				ids+=[campaign.campaign_id]
			if data["twitter"]:
				campaign=Campaign(name=data["name"],desc=data["description"],platform=3,creative_req=data["creativereq"],subtype=str(camp_type),linktoshare=link,caption=caption)
				db.session.add(campaign)
				brand.campaigns.append(campaign)
				db.session.commit()
				if int(camp_type) in [7,8]:
					loc=Location.query.filter_by(location_id=data["location"]).first()
					campaign.location.append(loc)
					db.session.commit()
				ids+=[campaign.campaign_id]
			if len(ids)==0:
				return jsonify(valid=False,err="No Platform Selected")
			db.session.commit()
			return jsonify(valid=True,msg="Campaign Created",campaign_ids=ids)
	except:
		return jsonify(valid=False,err="Something Went Wrong!!!")





@app.route("/inflivecampaign",methods=["GET","POST"])
def inflivecampaign():
	try:
		if request.method=="POST":
			data=request.json
			tokken=data["tokken"]
			inf=Influencer_details.query.filter_by(c_tokken=tokken).first()
			camp=Campaign.query.all()
			campaign_schema=Campaign_S()
			result=[]
			for i in camp:
				if i.status==1:
				# if inf.location[0] in i.location and inf.interests in i.business_interest:
					if i.platform==0 and inf.use_facebook:
						result.append(campaign_schema.dump(i).data)
					elif i.platform==1 and inf.use_instagram:
						result.append(campaign_schema.dump(i).data)
					elif i.platform==3 and inf.use_twitter:
						result.append(campaign_schema.dump(i).data)
					elif i.platform==2 and inf.use_youtube:
						result.append(campaign_schema.dump(i).data)
					elif i.platform==10:
						result.append(campaign_schema.dump(i).data)
			return jsonify(valid=True,campaigns=result)
	except:
		return jsonify(valid=False,err="Some Thing Went Wrong!!!")


def heapPermutation(a, size, n):
	if (size == 1):
		yield a
	for i in range(size):
		heapPermutation(a,size-1,n)
		if size&1: 
			a[0], a[size-1] = a[size-1],a[0] 
		else: 
			a[i], a[size-1] = a[size-1],a[i]
def good_triplets (arr, n):
	# Write your code here
	count=0
	for val in heapPermutation(arr,len(arr),3):
		sumv=sum(val)
		divi=0
		if sumv%val[0]==0:
			divi+=1
		if sumv%val[1]==0:
			divi+=1
		if sumv%val[2]==0:
			divi+=1
		if divi==1:
			count+=1
	return count
	
	
n = int(input())
arr = []
for i in range(n) : 
	x = int(input())
	arr.append(x)

out_ = good_triplets(arr, n)
print (out_)

@app.route("/infurl/<string:m>-<string:cid>",methods=["GET","POST"] )
def infurl(m,cid):
	mob=m[2:12]
	inff=Influencer_details.query.filter_by(mobile_no=mob).first()
	infinv=Influencers_involved.query.filter_by(influencer_id=inff.influencer_id,campaign_id=int(cid)).first()
	if infinv.click_count==None:
		infinv.click_count=1
	else:
		infinv.click_count=infinv.click_count+1
	db.session.commit()
	return redirect('https://www.sourcewebsite.com')


@app.route("/get-posts-details",methods=["GET","POST"])
def get_posts_details():
	try:
		data=request.json
		post=Campaign.query.filter_by(campaign_id=data["campaign_id"]).first().posts[0]
		post_schema=Campaign_posts_S()
		output=post_schema.dump(post).data
		return jsonify(valid=True,data=output)
	except:
		return jsonify(valid=False,err="Something Went Wrong!!!")


def send_push_notif_brand(brand,msg):
	try:
		if brand.not_token:
			send_push_message(brand.not_token,msg)
			nn=Notifications(message=msg)
			db.session.add(nn)
			rr=Rel_brand_notification()
			db.session.add(rr)
			brand.notify.append(rr)
			nn.notifications_for_brand.append(rr)
			db.session.commit()
		else:
			pass
	except:
		pass



@app.route("/apply-for-campaign",methods=["GET","POST"])
def apply_for_campaign():
	# try:
		if request.method=="POST":
			data=request.json
			inf=Influencer_details.query.filter_by(c_tokken=data["tokken"]).first()
			campaign=Campaign.query.filter_by(campaign_id=data["campaign_id"]).first()
			infinv=Influencers_involved.query.filter_by(influencer_id=inf.influencer_id,campaign_id=campaign.campaign_id).all()
			if len(infinv)>0:
				return jsonify(valid=False,err=" You Have Already Applied ")
			req_platform=campaign.platform
			followers=0
			if req_platform==0:
				fb=Facebook.query.filter_by(influencer_id=inf.influencer_id).first()
				followers=fb.follower_count
			elif req_platform==1:
				insta=Instagram.query.filter_by(influencer_id=inf.influencer_id).first()
				followers=insta.follower_count
			elif req_platform==3:
				tw=Twitter.query.filter_by(influencer_id=inf.influencer_id).first()
				followers=tw.follower_count
			elif req_platform==2:
				yt=Youtube.query.filter_by(influencer_id=inf.influencer_id).first()
				followers=yt.subscriber_count

			if followers>=100 and followers<=500:
				x=0
				req_inf=campaign.no_of_influencers1
			elif followers>500:
				x=1
				req_inf=campaign.no_of_influencers2

			inf_inv=Influencers_involved.query.filter_by(campaign_id=data["campaign_id"],range_type=x).all()
			already_inv=len(inf_inv)
# 			un_link=click_url_generator(inf.mobile_no,campaign.campaign_id)
			if already_inv<req_inf:
				involve=Influencers_involved(influencer_id=inf.influencer_id,campaign_id=campaign.campaign_id,range_type=x,accepted=True)
				db.session.add(involve)
				db.session.commit()
				campaign.influencers.append(involve)
				inf.involved_in.append(involve)
				db.session.commit()
				if int(campaign.subtype)==4 or int(campaign.subtype)==6:
					send_push_notif(inf,"Your application has been accepted. Please Perform the Action As Soon As Possible.")
					return jsonify(valid=True)
				for p in campaign.posts:
					new_post=Posts_done(file_name=p.file_name,rules=p.rules,desc=p.desc,verified=True)
					db.session.add(new_post)
					db.session.commit()
					involve.posts.append(new_post)
					db.session.commit()
				send_push_notif(inf,"Your application has been accepted. Please Perform the Action As Soon As Possible.")
				return jsonify(valid=True)
			elif already_inv<int(1.05*req_inf):
				involve=Influencers_involved(influencer_id=inf.influencer_id,campaign_id=campaign.campaign_id,range_type=x,accepted=False)
				db.session.add(involve)
				db.session.commit()
				campaign.influencers.append(involve)
				inf.involved_in.append(involve)
				db.session.commit()
				if int(campaign.subtype)==4 or int(campaign.subtype)==6:
					send_push_notif(inf,"Your application is pending.")
					return jsonify(valid=True)
				for p in campaign.posts:
					new_post=Posts_done(file_name=p.file_name,rules=p.rules,desc=p.desc)
					db.session.add(new_post)
					db.session.commit()
					involve.posts.append(new_post)
					db.session.commit()
				send_push_notif(inf,"Your application is pending.")
				return jsonify(valid=True)
			else:
				send_push_notif(inf,"Regret! Number of applications have reached the limit.")
				return jsonify(valid=False,err="Sorry!!! Campaign Full Please Try In Some Other Campaign")
	# except:
	# 	return jsonify(valid=False,err="Something Went Wrong!!!")

@app.route("/inf-daily-task",methods=["GET","POST"])
def inf_daily_task():
	try:
		if request.method=="POST":
			data=request.json
			tokken=data["tokken"]
			inf=Influencer_details.query.filter_by(c_tokken=tokken).first()
			involve=inf.involved_in
			result=[]
			post_sch=Posts_done_S()
			for i in involve:
				if i.registered_campaigns.status==2:
					for j in i.posts:
						if not j.done and j.verified:
							result.append(post_sch.dump(j).data)
			return jsonify(valid=True,dailytask=result)
	except:
		return jsonify(valid=False,err="Some Thing Went Wrong!!!")

