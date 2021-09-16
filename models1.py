from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Rel_campaign_campposts(db.Model):
    __tablename__="rel_campaign_interest"
    ci_id=db.Column(db.Integer,primary_key=True)
    campaign_id=db.Column(db.Integer,db.ForeignKey("campaign.campaign_id"))
    campposts_id=db.Column(db.Integer,db.ForeignKey("campaign_posts.cp_id"))
    campposts=db.relationship("Campaign_posts", cascade="all,delete",backref=db.backref("creative_in_campaigns"))



class Brand_details(db.Model):
    __tablename__="brand_details"
    brand_id=db.Column(db.Integer,primary_key=True)
    full_name=db.Column(db.String(50),nullable=False)
    brand_name=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(50),nullable=False)
    contact_no=db.Column(db.String(15))
    password=db.Column(db.String(200),nullable=False)
    verified=db.Column(db.Boolean)      #verified=1  unverified=0
    spoc=db.relationship("Spoc_details", cascade="all,delete",backref=db.backref("brand"))    #uselist=false  makes it one-one
    campaigns=db.relationship("Campaign", cascade="all,delete",backref=db.backref("of_brand"))
    notify=db.relationship("Rel_brand_notification", cascade="all,delete",backref=db.backref("notify_to_brand"))   #many-many with notifications
    company_type=db.Column(db.String(40))
    company_turnover=db.Column(db.String(10))
    company_size=db.Column(db.Integer)
    headquarter=db.Column(db.String(50))
    website_url=db.Column(db.String(100))
    gst_no=db.Column(db.String(20))
    b_wallet=db.Column(db.Integer)
    c_tokken=db.Column(db.String(200))
    logo=db.Column(db.LargeBinary)

class Spoc_details(db.Model):
    __tablename__="spoc_details"
    spoc_id=db.Column(db.Integer,primary_key=True)
    brand_id=db.Column(db.Integer,db.ForeignKey("brand_details.brand_id"))
    name=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(50),nullable=False)
    designation=db.Column(db.String(10))
    contact_no=db.Column(db.String(12),nullable=False)

class Influencer_details(db.Model):
    __tablename__="influencer_details"
    influencer_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))
    email=db.Column(db.String(50))
    password=db.Column(db.String(200))
    mobile_no=db.Column(db.String(15),nullable=False)
    profile_photo=db.Column(db.String(100))
    age=db.Column(db.Integer)
    verified=db.Column(db.Boolean)      #verified=1  unverified=0
    gender=db.Column(db.String(1))
    location=db.Column(db.String(20))
    interest_areas=db.Column(db.String(200))
    notify=db.relationship("Rel_influencer_notification", cascade="all,delete",backref=db.backref("notify_to_inf"))   #many-many with notifications
    i_wallet=db.Column(db.Integer)
    facebook_id=db.Column(db.String(100))
    facebook_follower_count=db.Column(db.Integer)
    instagram_id=db.Column(db.String(100))
    instagram_follower_count=db.Column(db.Integer)
    twitter_id=db.Column(db.String(100))
    twitter_follower_count=db.Column(db.Integer)
    youtube_id=db.Column(db.String(100))
    youtube_follower_count=db.Column(db.Integer)
    c_tokken=db.Column(db.String(200))
    logo=db.Column(db.LargeBinary)

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
    accepted=db.Column(db.Boolean)
    active_status=db.Column(db.Integer)
    amount_to_be_paid=db.Column(db.Integer)
    posts=db.relationship("Posts_done", cascade="all,delete",backref=db.backref("by_influencer"))   #one-many with posts table

class Posts_done(db.Model):
    __tablename__="posts_done"
    pd_id=db.Column(db.Integer,primary_key=True)
    file_name=db.Column(db.String(50))
    inf_inv_id=db.Column(db.Integer,db.ForeignKey("influencers_involved.inf_inv_id"))
    date_posted=db.Column(db.DateTime)
    post_unique_id=db.Column(db.String(100))
    verified=db.Column(db.Boolean)
    post_data=db.Column(db.String(200))
    platform=db.Column(db.Integer)  #1-facebook, 2-insta, 3-twitter, 4-youtube


class Campaign(db.Model):
    __tablename__="campaign"
    campaign_id=db.Column(db.Integer, primary_key=True)
    brand_id=db.Column(db.Integer,db.ForeignKey("brand_details.brand_id"))
    name=db.Column(db.String(50))
    desc=db.Column(db.String(400))
    typeC=db.Column(db.String(30))
    subtype=db.Column(db.String(30),nullable=True)
    posts=db.relationship("Rel_campaign_campposts", cascade="all,delete",backref=db.backref("from_campaign"))
    status=db.Column(db.Integer)    #0=closed, 1=active, 2=upcoming
    business_interest=db.Column(db.String(200)) #many to many with interest
    no_of_influencers=db.relationship("Influencers_required", cascade="all,delete",backref=db.backref("i_for_campaign"))     #one-one with Influencers_available
    platform=db.Column(db.Integer)
    creative_req=db.Column(db.Boolean)
    est_duration=db.Column(db.String(10))
    est_budget=db.Column(db.String(10))
    est_reach=db.Column(db.String(10))
    location=db.Column(db.String(200))
    influencers=db.relationship("Rel_campaign_influencer_inv", cascade="all,delete",backref=db.backref("registered_campaigns"))   #many-many with influencers_involved


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

class Campaign_posts(db.Model):
    __tablename__="campaign_posts"
    cp_id=db.Column(db.Integer,primary_key=True)
    file_name=db.Column(db.String(50))
    file=db.Column(db.LargeBinary)
    approved=db.Column(db.Boolean)

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

class Payments(db.Model):
    __tablename__="payments"
    payment_id=db.Column(db.Integer,primary_key=True)
    paid_by=db.Column(db.Integer)   #0-brand, 1-influencer
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
    create_date=db.Column(db.DateTime)
    expiry_date=db.Column(db.DateTime)
    is_reminder=db.Column(db.Boolean)
    next_reminder=db.Column(db.DateTime)

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

