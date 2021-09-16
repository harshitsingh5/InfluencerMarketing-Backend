#CONTAINS ONLY APIs

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import xyz_db
import db_schema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/xyz'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
ma = Marshmallow(app)

@app.route("/signup")
def signup():
	try:
		if request.method=="POST":
			data = request.get_json()
			user=User_details.query.filter_by(email=data['email']).all()
			if len(user)==0:
				new_brand=Brand_details(full_name=data['full_name'],brand_name=data['brand_name'],email=data['email'],password=data['password'],verified=0,company_type=data['company_type'],company_size=data['company_size'],headquarter=data['headquarter'],website_url=data['website_url'],b_wallet=0)
				db.session.add(new_user)
				msg=Message('From xyz',sender='smtp.gmail.com',recipients=[new_brand.email])
				otp=randint(100000,999999)
				msg.body="Your otp for signup: "+str(otp)
				mail.send(msg)
				otp_obj=Otp_details(otp_for=0,brand_id=new_brand.brand_id,otp_no=otp,purpose=1,valid_till=(datetime.now()+timedelta(hours=1)))
				db.session.commit()
				return jsonify(created=True,otp_id=otp_obj.otp_no)
			else:
				return "Account already exist"
		else:
			return
	except:
		return


@app.route("/login")
def login():
	try:
		if request.method=="POST":
			data = request.get_json()
			user=Brand_details.query.filter_by(email=data['email']).first()
			if len(user)==0:
				return "No such account exists"
			if sha256_crypt.verify(data['password'],user.password):
				session['logged_in']=True
				brand_schema = Brand_details_S()	#brand schema
				output = brand_schema.dump(user).data
				return jsonify({'brand' : output})
			else:
				return "Wrong Password"
	except:
		return


#
