import os
from filters import *
from printer import *
from small_session_stats import get_small_session_stats
import numpy as np
import matplotlib.pyplot as plt
import imp

from plotting import *
        
class mydict(dict):
    #if "NIL" is set as a value, returns None
    def __getitem__(self,key):
        value = super(mydict,self).__getitem__(key)
        if value == "NIL":
            return None
        else:
            return value
            
def get_session_stats(session_stats_path):
    with open(session_stats_path,'r') as fin:
        session_stats = []
        for line in fin:
            #session_stats.extend(eval(line))
            line = eval(line)
            for session_stat in line:
                if session_stat != None:
                    session_stats.append(session_stat)
        return session_stats

def toggle():
    global session_stats
    global flag
    if flag:
        session_stats = session_stats_big
        current = "big"
        flag = False
    else:
        session_stats = session_stats_small
        current = "small"
        flag = True
#threshold to be considered a different session
flag = True
current = "big"

#session_stats_path = r"C:\Users\NormanVIII\Downloads\Users\sessions.txt"
#session_stats_path = "/Users/macdaddy/Documents/InternetMeasurement/internetMeasurement/data/sessions_no_interval_not_clumped_weird.txt"
session_stats_path = "/Users/macdaddy/Documents/InternetMeasurement/internetMeasurement/data/sessions_interval_not_clumped_weird.txt"

session_stats_big = get_session_stats(session_stats_path)
#session_stats_small = get_small_session_stats()

session_stats=session_stats_big

urls = {}
cur_url_id = 1
for session in session_stats:
    url = session["url"]
    if url in urls:
        session["url_id"] = urls[url]
    else:
        urls[url] = cur_url_id
        cur_url_id += 1
        session["url_id"] = urls[url]

#STATS = 
#time_series key = "{0}_hour_{1}".format(day_of_week,hour)

ids = ["all videos","redtube","not redtube","daily motion","not daily motion"]
filter_funcs = [yes_man,redtube,negate(redtube), dailymotion,negate(dailymotion)]

break_ids = ["all videos","mobile break","not mobile - break", "mobile - redtube", "not mobile - redtube"]
break_filter_funcs = [yes_man,mobile_and(break_web), and_func(negate(mobile),break_web),mobile_and(redtube),and_func(negate(mobile),redtube)]

mobile_ids = [ "mobile","not mobile","mobile - redtube", "mobile - daily", "mobile - not redtube", "mobile -not daily","not mobile - redtube","not mobile - daily"]
mobile_filter_funcs = [mobile,negate(mobile),mobile_and(redtube),mobile_and(dailymotion),negate(mobile_and(redtube)),negate(mobile_and(dailymotion)),and_func(negate(mobile),redtube),and_func(negate(mobile),dailymotion)]

mobile_2_ids = ["mobile - redtube", "mobile - daily", "mobile - not redtube", "mobile -not daily","not mobile - redtube","not mobile - daily"]
mobile_2_filter_funcs = [mobile_and(redtube),mobile_and(dailymotion),negate(mobile_and(redtube)),negate(mobile_and(dailymotion)),and_func(negate(mobile),redtube),and_func(negate(mobile),dailymotion)]

computer_ids = ["all computer", "computer - redtube","computer - daily"]
computer_filter_funcs = [computer,and_func(computer,redtube),and_func(computer,dailymotion)]

daily_ids = ["mobile - daily"]
daily_filter_funcs = [mobile_and(dailymotion)]


max_wants_ids = ["video sharing sites", "episode viewing sites", "adult sites"]
max_wants_filter_funcs = [youtube_like,hulu_like,adult]

new_ids = ["weird1","weird2","weird3"]
new_filter_funcs = [indieclicktv,weird2,weird3]
new_filter_funcs = map(computer_and,new_filter_funcs)

num_bins = 1000000

attr = "file_size"



#limit
#limit = 4

us_red_sessions = filter(america_and(redtube),session_stats)
user_urls= {}
for session in us_red_sessions:
    user = session["user"]
    url = session["url"]
    if user in user_urls:
        user_urls[user].add(url)
    else:
        user_urls[user] = set()
        user_urls[user].add(url)
        


#batch_plot(session_stats,break_ids,attr,break_filter_funcs,num_bins,cdf=True,percent=False)
batch_plot(session_stats,attr,ids,filter_funcs,num_bins,cdf=True,percent=True,conversion_factor=1.0/1e6)
#batch_plot(session_stats,attr,computer_ids,computer_filter_funcs,num_bins,cdf=True,percent=True)
#batch_plot(session_stats,mobile_ids,attr,mobile_filter_funcs,num_bins,cdf=True,percent=True)
#batch_plot(session_stats,mobile_2_ids,attr,mobile_2_filter_funcs,num_bins,cdf=True,percent=True)
#batch_plot(session_stats,daily_ids,attr,daily_filter_funcs,num_bins,cdf=True)
#batch_plot(session_stats,attr,max_wants_ids,max_wants_filter_funcs,num_bins,cdf=True,percent=True)
#batch_plot(session_stats,attr,new_ids,new_filter_funcs,num_bins,cdf=True,percent=True)

plt.show()


'''
types = ["console","computer","mobile","nil"]
nil_count = 0
console_count = 0
computer_count = 0
mobile_count = 0
for session in session_stats:
    device = session["device"]
    if device == None:
        nil_count += 1
    else:
        locals()[device+"_count"] += 1


freqs = [locals()[x+"_count"] for x in types]
## the data
N = len(types)

## necessary variables
ind = np.arange(N)                # the x locations for the groups
width = 0.35                      # the width of the bars

p1 = plt.bar(ind, freqs,width, color='r')


plt.ylabel('Scores')
plt.title('Scores by group and gender')
plt.xticks(ind+width/2., types )
#plt.yticks(np.arange(0,81,10))
'''