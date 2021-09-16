interests={
1:'Automotive ',
2:'Banking ',
3:'Lifestyle & Interiors  ',
4:'Education ',
5:'Ed Tech ',
6: 'Engineering ',
7: 'Entertainment  ',
8: 'Energy  ',
9: ' Fast-moving consumer goods (FMCG) ',
10: 'Fashion  ',
11: ' Financial (Finance)  ',
12: ' Fin Tech  ',
13: ' Food & beverage  ',
14: 'Government & PSU  ',
15: ' Healthcare ',
16: 'Insurance  ',
17: 'Jewellery ',
18: 'Legal ',
19: 'Manufacturing ',
20: 'Media  ',
21: 'Online Aggregator ',
22: ' Real estate',
23: 'Retail ',
24: 'Sports  ',
25: 'Technology  ',
26: 'Telecom  ',
27: ' Travel & Hospitality   ',
28: 'Electronics ',
29: ' Not-for-profit ',
}


def Send_msg(mob,text):
	url="http://www.smsalert.co.in/api/push.json?apikey=dummy_key&sender=PUNNON&mobileno="+mob+"&text="+text
	

def reach_duration_budget(r1,r2,r3,r4,r5,r6):
	r1,r2,r3,r4,r5,r6=int(r1),int(r2),int(r3),int(r4),int(r5),int(r6)
	reach=(40*r1)+(80.2*r2)+(150.2*r3)+(200.2*r4)+(400.2*r5)+(1000.2*r6)
	duration=(r1+r2+r3+r4+r5+r6)*0.022
	budget=(30*r1)+(60*r2)+(90*r3)+(120*r4)+(150*r5)+(180*r6)
	return budget,duration,reach
