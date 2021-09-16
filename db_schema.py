from flask_marshmallow import Marshmallow
import xyz_db

class Brand_details_S(ma.ModelSchema):
    class Meta:
        model = Brand_details

class Spoc_details_S(ma.ModelSchema):
    class Meta:
        model = Spoc_details

class Influencer_details_S(ma.ModelSchema):
    class Meta:
        model = Influencer_details

class Facebook_S(ma.ModelSchema):
    class Meta:
        model = Facebook

class Instagram_S(ma.ModelSchema):
    class Meta:
        model = Instagram

class Twitter_S(ma.ModelSchema):
    class Meta:
        model = Twitter

class Youtube_S(ma.ModelSchema):
    class Meta:
        model = Youtube

class Otp_details_S(ma.ModelSchema):
    class Meta:
        model = Otp_details

class Interest_details_S(ma.ModelSchema):
    class Meta:
        model = Interest_details

class Influencers_required_S(ma.ModelSchema):
    class Meta:
        model = Influencers_required

class Influencers_involved_S(ma.ModelSchema):
    class Meta:
        model = Influencers_involved

class Posts_done_S(ma.ModelSchema):
    class Meta:
        model = Posts_done

class Campaign_S(ma.ModelSchema):
    class Meta:
        model = Campaign

class Rel_campaign_interest_S(ma.ModelSchema):
    class Meta:
        model = Rel_campaign_interest

class Rel_campaign_influencer_inv_S(ma.ModelSchema):
    class Meta:
        model = Rel_campaign_influencer_inv

class Rel_influencer_interest_S(ma.ModelSchema):
    class Meta:
        model = Rel_influencer_interest

class Platform_S(ma.ModelSchema):
    class Meta:
        model = Platform

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
