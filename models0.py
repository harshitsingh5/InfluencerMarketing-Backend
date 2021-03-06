from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Brand_details(db.Model):
    __tablename__="brand_details"
    brand_id=db.Column(db.Integer,primary_key=True)
    full_name=db.Column(db.String(50),nullable=False)
    brand_name=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(50),nullable=False)
    password=db.Column(db.String(200),nullable=False)
    verified=db.Column(db.Boolean)      #verified=1  unverified=0
    company_type=db.Column(db.String(40))
    company_turnover=db.Column(db.String(10))
    company_size=db.Column(db.Integer)
    headquarter=db.Column(db.String(50))
    website_url=db.Column(db.String(100))
    b_wallet=db.Column(db.Integer)
    c_tokken=db.Column(db.String(200))
    not_token=db.Column(db.String(200))
    logo=db.Column(db.LargeBinary)
    spoc=db.relationship("Spoc_details", cascade="all,delete",backref=db.backref("brand"))    #uselist=false  makes it one-one
    payment=db.relationship("Payments", cascade="all,delete",backref=db.backref("by_brand"))     #one-many
    interests=db.relationship("Interest_details", cascade="all,delete",backref=db.backref("of_brand"))   #many-many
    notify=db.relationship("Rel_brand_notification", cascade="all,delete",backref=db.backref("notify_to_brand"))   #many-many with notifications
    campaigns=db.relationship("Campaign", cascade="all,delete",backref=db.backref("of_brand"))      #many many with campaign
    location=db.relationship("Location", cascade="all,delete",backref=db.backref("of_brand"))    #one one

class Spoc_details(db.Model):
    __tablename__="spoc_details"
    spoc_id=db.Column(db.Integer,primary_key=True)
    brand_id=db.Column(db.Integer,db.ForeignKey("brand_details.brand_id"))
    name=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(50),nullable=False)
    contact_no=db.Column(db.String(12),nullable=False)


class Location(db.Model):
    __tablename__="location"
    location_id=db.Column(db.Integer,primary_key=True)
    location=db.Column(db.String(50))
    brand_id=db.Column(db.Integer,db.ForeignKey("brand_details.brand_id"))
    inf_id=db.Column(db.Integer,db.ForeignKey("influencer_details.influencer_id"))
    campaign=db.Column(db.Integer,db.ForeignKey("campaign.campaign_id"))


class Influencer_details(db.Model):
    __tablename__="influencer_details"
    influencer_id=db.Column(db.Integer,primary_key=True)
    mobile_no=db.Column(db.String(15),nullable=False)
    name=db.Column(db.String(50))
    email=db.Column(db.String(50))
    profile_photo=db.Column(db.String(50),default="defaultprof.jpg")
    dob=db.Column(db.DateTime)
    age=db.Column(db.Integer)
    updated=db.Column(db.Boolean,default=False)      #verified=1  unverified=0
    gender=db.Column(db.String(1))
    location=db.relationship("Location", cascade="all,delete",backref=db.backref("of_influencer"))    #one one
    i_wallet=db.Column(db.Integer)
    use_facebook=db.Column(db.Boolean)
    use_instagram=db.Column(db.Boolean)
    use_twitter=db.Column(db.Boolean)
    use_youtube=db.Column(db.Boolean)
    fb_id=db.Column(db.Integer,db.ForeignKey("facebook.fb_id"),nullable=True)
    insta_id=db.Column(db.Integer,db.ForeignKey("instagram.insta_id"),nullable=True)
    tw_id=db.Column(db.Integer,db.ForeignKey("twitter.tw_id"),nullable=True)
    yt_id=db.Column(db.Integer,db.ForeignKey("youtube.yt_id"),nullable=True)
    c_tokken=db.Column(db.String(200))
    not_token=db.Column(db.String(200))
    payment=db.relationship("Payments", cascade="all,delete",backref=db.backref("by_influencer"))     #one-many
    notify=db.relationship("Rel_influencer_notification", cascade="all,delete",backref=db.backref("notify_to_inf"))   #many-many with notifications
    interests=db.relationship("Interest_details", cascade="all,delete",backref=db.backref("of_influencer"))   #many-many
    involved_in=db.relationship("Influencers_involved", cascade="all,delete",backref=db.backref("influencer"))
    coupon=db.relationship("Coupons", cascade="all,delete",backref=db.backref("for_influencer"))   #many-many

class Facebook(db.Model):
    __tablename__="facebook"
    fb_id=db.Column(db.Integer,primary_key=True)
    influencer_id=db.Column(db.Integer,db.ForeignKey("influencer_details.influencer_id"))
    profile_url=db.Column(db.String(100))
    follower_count=db.Column(db.Integer)
    verified=db.Column(db.Boolean)
    access_token=db.Column(db.String(100))

class Instagram(db.Model):
    __tablename__="instagram"
    insta_id=db.Column(db.Integer,primary_key=True)
    influencer_id=db.Column(db.Integer,db.ForeignKey("Influencer_details.influencer_id"))
    #profile_url=db.Column(db.String(100))
    follower_count=db.Column(db.Integer)
    verified=db.Column(db.Boolean)
    access_token=db.Column(db.String(100))
    insta_numeric_id=db.Column(db.String(100))

class Twitter(db.Model):
    __tablename__="twitter"
    tw_id=db.Column(db.Integer,primary_key=True)
    influencer_id=db.Column(db.Integer,db.ForeignKey("influencer_details.influencer_id"))
    profile_url=db.Column(db.String(100))
    follower_count=db.Column(db.Integer)
    verified=db.Column(db.Boolean)
    access_token=db.Column(db.String(100))

class Youtube(db.Model):
    __tablename__="youtube"
    yt_id=db.Column(db.Integer,primary_key=True)
    influencer_id=db.Column(db.Integer,db.ForeignKey("Influencer_details.influencer_id"))
    channel_link=db.Column(db.String(100))
    subscriber_count=db.Column(db.Integer)
    verified=db.Column(db.Boolean)

class Interest_details(db.Model):
    __tablename__="interest_details"
    interest_id=db.Column(db.Integer,primary_key=True)
    user_type=db.Column(db.Integer)   #0-brand, 1-influencer
    brand_id=db.Column(db.Integer,db.ForeignKey("brand_details.brand_id"), nullable=True)
    influencer_id=db.Column(db.Integer, db.ForeignKey("influencer_details.influencer_id"),nullable=True)
    campaign=db.Column(db.Integer,db.ForeignKey("campaign.campaign_id"))
    name1=db.Column(db.Boolean)
    name2=db.Column(db.Boolean)
    name3=db.Column(db.Boolean)
    name4=db.Column(db.Boolean)
    name5=db.Column(db.Boolean)
    name6=db.Column(db.Boolean)
    name7=db.Column(db.Boolean)
    name8=db.Column(db.Boolean)
    name9=db.Column(db.Boolean)
    name10=db.Column(db.Boolean)
    name11=db.Column(db.Boolean)

class Otp_details(db.Model):
    __tablename__="otp_details"
    otp_id=db.Column(db.Integer,primary_key=True)
    otp_for=db.Column(db.Integer)   #0-brand, 1-influencer
    brand_id=db.Column(db.Integer,db.ForeignKey("brand_details.brand_id"), nullable=True)
    influencer_id=db.Column(db.Integer,db.ForeignKey("influencer_details.influencer_id"),nullable=True)
    otp_no=db.Column(db.Integer,nullable=False)
    purpose=db.Column(db.Boolean)           #password change=0   verification=1
    valid_till=db.Column(db.DateTime)     #store time and date upto which otp is valid_till

class Influencers_required(db.Model):
    __tablename__="influencers_required"
    inf_req_id=db.Column(db.Integer,primary_key=True)
    campaign_id=db.Column(db.Integer, db.ForeignKey("campaign.campaign_id"))
    range1=db.Column(db.Integer)
    range2=db.Column(db.Integer)
    range3=db.Column(db.Integer)
    range4=db.Column(db.Integer)
    range5=db.Column(db.Integer)
    range6=db.Column(db.Integer)
    total=db.Column(db.Integer)

class Influencers_involved(db.Model):
    __tablename__="influencers_involved"
    inf_inv_id=db.Column(db.Integer,primary_key=True)
    campaign_id=db.Column(db.Integer, db.ForeignKey("campaign.campaign_id"))
    influencer_id=db.Column(db.Integer, db.ForeignKey("influencer_details.influencer_id"))
    accepted=db.Column(db.Boolean,default=False)
    active_status=db.Column(db.Integer)
    amount_to_be_paid=db.Column(db.Integer,default=0)
    posts=db.relationship("Posts_done", cascade="all,delete",backref=db.backref("by_influencer"))   #one-many with posts table
    created=db.relationship("Created_table", cascade="all,delete",backref=db.backref("by_influencer"))   #one-many

class Posts_done(db.Model):
    __tablename__="posts_done"
    pd_id=db.Column(db.Integer,primary_key=True)
    inf_inv_id=db.Column(db.Integer,db.ForeignKey("influencers_involved.inf_inv_id"))
    platform=db.Column(db.Integer)  #1-facebook, 2-insta, 3-twitter, 4-youtube
    post_url=db.Column(db.String(100))
    likes=db.Column(db.Integer)
    views=db.Column(db.Integer)
    file_name=db.Column(db.String(50))
    date_posted=db.Column(db.DateTime)
    verified=db.Column(db.Boolean)
    post_data=db.Column(db.String(200))
    rules=db.Column(db.String(200))
    description=db.Column(db.String(200))

class Created_table(db.Model):
    __tablename__="created_table"
    ct_id=db.Column(db.Integer,primary_key=True)
    inf_inv_id=db.Column(db.Integer,db.ForeignKey("influencers_involved.inf_inv_id"))
    image=db.Column(db.LargeBinary)
    blog=db.Column(db.String(1000))
    video=db.Column(db.String(50))
    verified=db.Column(db.Boolean)
    status=db.Column(db.Integer)

class Campaign(db.Model):
    __tablename__="campaign"
    campaign_id=db.Column(db.Integer, primary_key=True)
    brand_id=db.Column(db.Integer,db.ForeignKey("brand_details.brand_id"))
    image=db.Column(db.String(30),default="campdef.jpg")
    subtype=db.Column(db.String(30),nullable=True)
    name=db.Column(db.String(200))
    desc=db.Column(db.String(4000))
    status=db.Column(db.Integer)    #0=closed, 1=active, 2=upcoming
    age_req=db.Column(db.Integer)
    platform=db.Column(db.String(10))   #eg. 1,2,3,4    fb,insta,tw,yt
    location=db.relationship("Location", cascade="all,delete",backref=db.backref("campaigns"))      #many-many with Location
    payment=db.Column(db.Integer,db.ForeignKey("payments.payment_id"))
    no_of_influencers=db.relationship("Influencers_required", cascade="all,delete",backref=db.backref("i_for_campaign"), uselist=False)     #one-one with Influencers_available
    business_interest=db.relationship("Interest_details", cascade="all,delete",backref=db.backref("interested_campaigns"))   #many to many with interest
    influencers=db.relationship("Influencers_involved", cascade="all,delete",backref=db.backref("registered_campaigns"))   #many-many with influencers_involved
    posts=db.relationship("Campaign_posts", cascade="all,delete",backref=db.backref("from_campaign"))
    c_type=db.relationship("Campaign_type", cascade="all,delete",backref=db.backref("from_campaign"))
    pricing=db.relationship("Pricing_details", cascade="all,delete",backref=db.backref("for_campaign"), uselist=False)     #one-one

class Campaign_posts(db.Model):
    __tablename__="campaign_posts"
    cp_id=db.Column(db.Integer,primary_key=True)
    file_name=db.Column(db.String(50))
    campaign_id=db.Column(db.Integer,db.ForeignKey("campaign.campaign_id"))
    file_location=db.Column(db.String(100))
    approved=db.Column(db.Boolean)

class Campaign_type(db.Model):
    __tablename__="campaign_type"
    ca_id=db.Column(db.Integer,primary_key=True)
    reach=db.Column(db.Integer)
    cost_to_brand=db.Column(db.Integer)
    payout_to_influencers=db.Column(db.Integer)
    campaign_id=db.Column(db.Integer,db.ForeignKey("campaign.campaign_id"))

'''
class Rel_campaign_interest(db.Model):
    __tablename__="rel_campaign_interest"
    ci_id=db.Column(db.Integer,primary_key=True)
    campaign_id=db.Column(db.Integer,db.ForeignKey("campaign.campaign_id"))
    interest_id=db.Column(db.Integer,db.ForeignKey("interest_details.interest_id"))
    interest=db.relationship("Interest_details", cascade="all,delete",backref=db.backref("used_in_campaigns"))

class Rel_campaign_influencer_inv(db.Model):
    __tablename__="rel_campaign_influencer_inv"
    ci_id=db.Column(db.Integer,primary_key=True)
    campaign_id=db.Column(db.Integer,db.ForeignKey("campaign.campaign_id"))
    inf_inv_id=db.Column(db.Integer,db.ForeignKey("influencers_involved.inf_inv_id"))
    influencers_inv=db.relationship("Influencers_involved", cascade="all,delete",backref=db.backref("inv_in_campaign"))

class Platform(db.Model):
    __tablename__="platform"
    platform_id=db.Column(db.Integer,primary_key=True)
    campaign_id=db.Column(db.Integer,db.ForeignKey("campaign.campaign_id"))
    facebook=db.Column(db.Boolean)
    instagram=db.Column(db.Boolean)
    twitter=db.Column(db.Boolean)
    youtube=db.Column(db.Boolean)
'''

class Pricing_details(db.Model):
    __tablename__="pricing_details"
    pricing_id=db.Column(db.Integer,primary_key=True)
    follower_lower_range=db.Column(db.Integer)
    follower_upper_range=db.Column(db.Integer)
    est_impression=db.Column(db.Integer)
    est_engagement=db.Column(db.Integer)
    est_videoviews=db.Column(db.Integer)
    payout_to_influencers=db.Column(db.Integer)
    price_to_brand=db.Column(db.Integer)
    est_duration=db.Column(db.Integer)
    campaign=db.Column(db.Integer,db.ForeignKey("campaign.campaign_id"))

class Payments(db.Model):
    __tablename__="payments"
    payment_id=db.Column(db.Integer,primary_key=True)
    pay_type=db.Column(db.Integer)   #0-brand, 1-influencer
    brand_id=db.Column(db.Integer,db.ForeignKey("brand_details.brand_id"), nullable=True)
    influencer_id=db.Column(db.Integer, db.ForeignKey("influencer_details.influencer_id"),nullable=True)
    mode=db.Column(db.Integer)     #0-   ,1-   ,....
    amount=db.Column(db.Float)
    date_time=db.Column(db.DateTime)
    purpose=db.Column(db.String(20))
    transaction_id=db.Column(db.String(50))
    hashv=db.Column(db.String(50))
    links=db.Column(db.String(100))
    payment_detail_data=db.Column(db.String(50))
    status=db.Column(db.String(10))
    order_id=db.Column(db.String(20))

class Notifications(db.Model):
    __tablename__="notifications"
    not_id=db.Column(db.Integer,primary_key=True)
    subject=db.Column(db.String(50))
    message=db.Column(db.String(200))

class Coupons(db.Model):
    __tablename__="coupons"
    c_id=db.Column(db.Integer,primary_key=True)
    coupon_name=db.Column(db.String(50))
    coupon_code=db.Column(db.String(5000))
    cost=db.Column(db.Integer)
    desciption=db.Column(db.String(500))

class Rel_influencer_coupons(db.Model):
    __tablename__="rel_influencer_coupons"
    ic_id=db.Column(db.Integer,primary_key=True)
    influencer_id=db.Column(db.Integer,db.ForeignKey("influencer_details.influencer_id"))
    c_id=db.Column(db.Integer,primary_key=True)
    coupon_code=db.Column(db.String(50))

class Rel_influencer_notification(db.Model):
    __tablename__="rel_influencer_notification"
    in_id=db.Column(db.Integer,primary_key=True)
    influencer_id=db.Column(db.Integer,db.ForeignKey("influencer_details.influencer_id"))
    not_id=db.Column(db.Integer,db.ForeignKey("notifications.not_id"))
    for_influencer=db.relationship("Notifications", cascade="all,delete",backref=db.backref("notifications_for_inf"))

class Rel_brand_notification(db.Model):
    __tablename__="rel_brand_notification"
    in_id=db.Column(db.Integer,primary_key=True)
    brand_id=db.Column(db.Integer,db.ForeignKey("brand_details.brand_id"))
    not_id=db.Column(db.Integer,db.ForeignKey("notifications.not_id"))
    for_brand=db.relationship("Notifications", cascade="all,delete",backref=db.backref("notifications_for_brand"))

rel_brand_interest = db.Table('rel_brand_interest',
    db.Column('brand_id', db.Integer, db.ForeignKey('brand_details.brand_id')),
    db.Column('interest_id', db.Integer, db.ForeignKey('interest_details.interest_id'))
)
rel_influencer_interest = db.Table('rel_influencer_interest',
    db.Column('influencer_id', db.Integer, db.ForeignKey('influencer_details.influencer_id')),
    db.Column('interest_id', db.Integer, db.ForeignKey('interest_details.interest_id'))
)
rel_campaign_interest = db.Table('rel_campaign_interest',
    db.Column('campaign_id', db.Integer, db.ForeignKey('campaign.campaign_id')),
    db.Column('interest_id', db.Integer, db.ForeignKey('interest_details.interest_id'))
)
rel_campaign_influencer_inv = db.Table('rel_campaign_influencer_inv',
    db.Column('campaign_id', db.Integer, db.ForeignKey('campaign.campaign_id')),
    db.Column('inf_inv_id', db.Integer, db.ForeignKey('influencers_involved.inf_inv_id'))
)
