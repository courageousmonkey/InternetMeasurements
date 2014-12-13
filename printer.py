from filters import *
import random

def print_user_sessions(session_stats,user,filter_func=yes_man):
    session_stats = chrono_sessions(session_stats)
    if len(session_stats) > 0:
        keys = session_stats[0].keys()
    for session in session_stats:
        if (session["user"] == user) and filter_func(session):
            print("-----------")
            for key in keys:
                print("{0}: {1}".format(key,session[key]))
                
def chrono_sessions(session_stats):
    return sorted(session_stats,key=lambda session:session["time_of_day_first"])
    
def get_random(indexable):
    r = random.randint(0,len(indexable)-1)
    return indexable[r]
    
days_of_week = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]