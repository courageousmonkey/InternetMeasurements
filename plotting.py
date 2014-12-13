
from filters import *
import numpy as np
import matplotlib.pyplot as plt


def collect_stats_for_sessions(session_stats,attr,filter_func,num_bins=300,cdf=True,percent=True,min_limit=-float("inf"),max_limit=float("inf"),conversion_factor=1):
    session_vals = []
    num_sessions = 0
    for session in session_stats:
        if filter_func(session) and not(session[attr] == None):
            converted_val = session[attr]*conversion_factor
            if (min_limit <= converted_val) and (converted_val <= max_limit):
                session_vals.append(converted_val)
                num_sessions +=1
    
    if num_sessions == 0:
        return ([],[])
        
    min_bin = min(session_vals)
    max_bin = max(session_vals)
    
    step = float(max_bin-min_bin)/num_bins
    if step == 0.0:
        return ([],[])
    
    
    val_freq = {}
    for val in session_vals:
        index = int((val-min_bin)/step)
        
        #taking care of max case
        if index == num_bins:
            index = num_bins -1
            
        if index in val_freq:
            val_freq[index] = val_freq[index] + 1
        else:
            val_freq[index] = 1
            
    attr_xs = []
    attr_ys = []
    running_sum = 0.0
    for i in range(0,num_bins):
        
        attr_xs.append((i+1)*step)
        if i not in val_freq:
            if cdf:
                attr_ys.append(running_sum)
            else:
                attr_ys.append(0.0)
        else:
            if percent:
                value = float(val_freq[i])/num_sessions
            else:
                value = float(val_freq[i])
                
            if cdf:
                running_sum += value
                attr_ys.append(running_sum)
            else:
                attr_ys.append(value)
    return (attr_xs,attr_ys)

def batch_stats(session_stats,attr,ids,filter_funcs,num_bins,cdf=True,percent=True,min_limit=-float("inf"),max_limit=float("inf"),conversion_factor=1):
    points = {}
    for i in range(len(ids)):
        attr_info = {}
        attr_xs,attr_ys = collect_stats_for_sessions(session_stats,attr,filter_funcs[i],num_bins,cdf,percent,min_limit,max_limit,conversion_factor)
        attr_info["xs"] = attr_xs
        attr_info["ys"] = attr_ys
        points[ids[i]] = attr_info
        
    return points

def batch_plot(session_stats,attr,ids,filter_funcs,num_bins=100000,cdf=True,percent=True,min_limit=-float("inf"),max_limit=float("inf"),conversion_factor=1,xlabel="xlabel",ylabel="ylabel"):
    batch_info = batch_stats(session_stats,attr,ids,filter_funcs,num_bins,cdf,percent,min_limit,max_limit,conversion_factor)
    fig = plt.figure()
    fig.suptitle(attr)
    for i in ids:
        plt.plot(map(lambda x:float(x),batch_info[i]["xs"]),batch_info[i]["ys"],label=i)
        
    plt.axis("tight")
    plt.xlabel("xlabel")
    plt.ylabel("ylabel")
    plt.legend(loc=4)
    return fig


def bar_plot(session_stats,label_func,top=-1,ylabel="ylabel",title="title",plot=True,can_be_none=False):
    bar_info = {}
    
    for session in session_stats:
        label = label_func(session)
        if (label == None):
            if can_be_none:
                label = "NIL"
            else:
                continue
        if label not in bar_info:
            bar_info[label] = 1
        else:
            bar_info[label] = bar_info[label] + 1
            
    if plot:
        bar_info_list = list(bar_info.items())
        
        bar_info_list.sort(key=(lambda x:x[1]))
        if top > 0:
            bar_info_list = bar_info_list[len(bar_info)-top:]
        
        labels,freqs = zip(*bar_info_list)
        
        N = len(labels)
    
        ## necessary variables
        ind = np.arange(N)                # the x locations for the groups
        width = 0.35                      # the width of the bars
        
        p1 = plt.bar(ind, freqs,width, color='r')
        
        
        plt.ylabel(ylabel)
        plt.title(title)
        plt.xticks(ind+width/2., labels,rotation="vertical" )
    return bar_info
    
def bar_customer_ids(session_stats):
    bar_info = {}
    for session in session_stats:
        customer_id = session["customer_id"]
        if customer_id not in bar_info:
            bar_info[customer_id] = 1
        else:
            bar_info[customer_id] = bar_info[customer_id] + 1
    bar_info = list(bar_info.items())
    
    bar_info.sort(key=(lambda x:x[1]))
    bar_info = bar_info[len(bar_info)-15:]
    
    labels,freqs = zip(*bar_info)
    
    N = len(labels)

    ## necessary variables
    ind = np.arange(N)                # the x locations for the groups
    width = 0.35                      # the width of the bars
    
    p1 = plt.bar(ind, freqs,width, color='r')
    
    
    plt.ylabel('Scores')
    plt.title('Scores by group and gender')
    plt.xticks(ind+width/2., labels )
    
def average_bar_plot(session_stats,label_func,top=-1,ylabel="ylabel",title="title",plot=True,can_be_none=False):
    bar_info = {}
    
    for session in session_stats:
        label = label_func(session)
        if (label == None):
            if can_be_none:
                label = "NIL"
            else:
                continue
        if label not in bar_info:
            bar_info[label] = 1
        else:
            bar_info[label] = bar_info[label] + 1
            
    if plot:
        bar_info_list = list(bar_info.items())
        
        bar_info_list.sort(key=(lambda x:x[1]))
        if top > 0:
            bar_info_list = bar_info_list[len(bar_info)-top:]
        
        labels,freqs = zip(*bar_info_list)
        
        N = len(labels)
    
        ## necessary variables
        ind = np.arange(N)                # the x locations for the groups
        width = 0.35                      # the width of the bars
        
        p1 = plt.bar(ind, freqs,width, color='r')
        
        
        plt.ylabel(ylabel)
        plt.title(title)
        plt.xticks(ind+width/2., labels,rotation="vertical" )
    return bar_info
    
def average(session_stats,attr,filter_func=yes_man):
    num_sessions = 0
    total = 0
    
    for session in session_stats:
        if filter_func(session) and session[attr] != None:
            total += session[attr]
            num_sessions += 1
            
    if num_sessions == 0:
        return None
    else:
        return float(total)/num_sessions

def utc_adjust_atlanta(time_series):
    new_time_series = {}
    for i in range(len(days_of_week)):
        day = days_of_week[i]
        for hour in range(0,24):
            new_hour = (hour - 5)%24
            if hour < 5:
                new_day = days_of_week[(i-1)%7]
            else:
                new_day = day
                
            if hour < 10:
                buff = "0"
            else:
                buff = ""
                
            key = "{0}_hour_{1}{2}".format(day,buff,hour)
            
            if new_hour < 10:
                new_buff = "0"
            else:
                new_buff = ""
            
            new_key = "{0}_hour_{1}{2}".format(new_day,new_buff,new_hour)
            if key in time_series:
                new_time_series[new_key] = time_series[key]
    return new_time_series

        
def day_time_series(session_stats,day="Monday",plot=True,utc_adjust=False):
    bytes_sent = [0]*24
    num_sessions = [0]*24
    for session in session_stats:
        if day in session["days_of_week"]:
            
            if utc_adjust:
                time_series = utc_adjust_atlanta(session["time_series"])
            else:
                time_series = session["time_series"]
                
            for hour in range(0,24):
                if hour < 10:
                    buff = "0"
                else:
                    buff = ""
                    
                key = "{0}_hour_{1}{2}".format(day,buff,hour)
                if key in time_series:
                    bytes_sent[hour] = bytes_sent[hour] + time_series[key]
                    num_sessions[hour] = num_sessions[hour] + 1
    xs = list(range(1,25))

        
    total_bytes_sent = sum(bytes_sent)
    total_sessions = sum(num_sessions)
    percent_bytes_sent = map(lambda x: float(x)/total_bytes_sent,bytes_sent)
    percent_num_sessions = map(lambda x:float(x)/total_sessions,num_sessions)
    
    if plot:
        plt.plot(xs,bytes_sent)
    return (percent_bytes_sent,percent_num_sessions)

def week_time_series(session_stats,plot=True):
    bytes_sent = [0]*(24*7)
    number_sessions = [0]*(24*7)
    for session in session_stats:
        for i in range(len(days_of_week)):
            day = days_of_week[i]
            if day in session["days_of_week"]:
                time_series = session["time_series"]
                for hour in range(0,24):
                    if hour < 10:
                        buff = "0"
                    else:
                        buff = ""
                    key = "{0}_hour_{1}{2}".format(day,buff,hour)
                    if key in time_series:
                        bytes_sent[i*24 + hour] = bytes_sent[i*24 + hour] + time_series[key]
                        number_sessions[i*24 + hour] = number_sessions[i*24 + hour] + 1
    xs = list(range(1, 24*7 + 1))
    total_bytes = sum(bytes_sent)
    total_sessions = sum(number_sessions)
    if plot:
        
        N = 24*7
        ind = np.arange(N)                # the x locations for the groups
        width = 0.35                      # the width of the bars
        p1 = plt.bar(ind, map(lambda x:float(x)/total_bytes,bytes_sent), color='r')
        
        labels = []
        for x in range(0,7):
            
            labels =labels +  [str(x if x == 0 else "noon") if (x == 0) or (x == 12) else "" for x in range(0,13)] + [ "" for x in range(1,12)]
        
        plt.ylabel("normalized bytes sent")
        plt.title("adult weekly volumes")
        plt.xticks(np.arange(24*7) + width, labels )
        plt.axis("tight")

    return bytes_sent

def sum_arrays(A,B):
    C=[]
    for i in range(len(A)):
        C.append(A[i] + B[i])
    return C
    
def divide_arrays(A,B):
    C = []
    for i in range(len(A)):
        C.append(A[i]/B[i])
    return C
    
def average_day_time_series(session_stats):
    average_bytes_sent = [0]*24
    average_num_sessions = [0]*24
    for day in days_of_week:
        bytes_sent_per_day,sessions_per_day = day_time_series(session_stats,day=day,plot=False)
        average_bytes_sent = sum_arrays(average_bytes_sent,bytes_sent_per_day)
        average_num_sessions = sum_arrays(average_num_sessions,sessions_per_day)
    xs = list(range(1,25))
    average_bytes_sent = map(lambda x: float(x)/7,average_bytes_sent)
    average_num_sessions = map(lambda x: float(x)/7,average_num_sessions)
    
    N = 24
    ind = np.arange(N)                # the x locations for the groups
    width = 0.35                      # the width of the bars
    p1 = plt.bar(ind, average_bytes_sent, color='r')
    
    labels = [str(x) if (x%3) == 0 else "" for x in range(0,13)] + [str(x) if (x%3)==0 else "" for x in range(1,13)]
    
    plt.ylabel("normalized bytes sent")
    plt.title("non adult daily volume")
    plt.xticks(np.arange(24) + width, labels )
    plt.axis("tight")

    
    '''
    plt.plot(xs,average_bytes_sent)
    plt.legend()
    plt.axis("tight")
    '''
    return average_bytes_sent
    

                
days_of_week = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]