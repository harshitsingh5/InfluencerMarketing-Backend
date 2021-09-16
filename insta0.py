import urllib
import json
import requests



access_token='dummy_token'

def store_insta_account_data(c_tokken,access_token):
    url='https://api.instagram.com/v1/users/self/?access_token='+access_token
    uResponse = requests.get(url)
    Jresponse = uResponse.text
    d = json.loads(Jresponse)
    insta_numeric_id=(d['data']['id'])
    followers=(d['data']['counts']['followed_by'])
    if followers>150:
        user=Influencer_details.query.filter_by(c_tokken=c_tokken).first()
        insta_user=Instagram(influencer_id=user.influencer_id,follower_count=followers,verified=True,access_token=access_token,insta_numeric_id=insta_numeric_id)
        db.session.add(insta_user)
        db.session.commit()
        return True
    else:
        return False

def getinstadata(url,insta_numeric_id,access_token):
    alphabet ={'-':62,'1':53,'0':52,'3':55,'2':54,'5':57,'4':56, '7':59, '6':58,'8':60,'9':61,'A':0,'C':2,'B':1,'E':4,'D':3,'G':6,'F':5,'I':8,'H':7,'K':10,'J':9,'M':12,'L':11,'O':14,'N':13,'Q':16,'P':15,'S':18,'R':17,'U':20,'T':19,'W':22,'V':21,'Y':24,'X':23,'Z':25,'_':63,'a':26,'c':28,'b':27,'e':30,'d':29,'g':32,'f':31,'i':34,'h':33,'k':36,'j':35,'m':38,'l':37,'o':40,'n':39,'q':42,'p':41,'s':44,'r':43,'u':46,'t':45,'w':48,'v':47,'y':50,'x':49,'z':51}
    n=0
    su=url.split('/')
    code=su[-2]
    for i in range(len(code)):
        c=code[i]
        n=n*64+alphabet[c]
    media_id=str(n)+'_'+insta_numeric_id
    url='https://api.instagram.com/v1/media/'+media_id+'?access_token='+access_token
    uResponse = requests.get(url)
    Jresponse = uResponse.text
    d = json.loads(Jresponse)
    likes_count=(d['data']['likes']['count'])
    comments_count=(d['data']['comments']['count'])
    user=Influencer_details.query.filter_by(c_tokken=c_tokken).first()
    insta_post=Posts_done(inf_inv_id=user.influencer_id,platform=2,post_url=url,likes=likes_count)
    db.session.add(insta_post)
    db.session.commit()
