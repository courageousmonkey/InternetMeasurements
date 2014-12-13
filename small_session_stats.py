import os
import fake
import filters
from filters import *
import numpy as np
import matplotlib.pyplot as plt
import datetime
import time

def pretty_sessions(n=1):
    count = 0
    for key in sessions:
        session_list = sessions[key]
        print("-------url {0} start --------".format(count+1))
        for session in session_list:

            print("---------- session start ---------")
            for response in session:
                print(response)
            print("----------session end --------")
        print("-------url {0} end --------".format(count+1))
        count = count + 1
        if count >= n:
            break

def session_interval_split(sorted_responses,interval):
    
    if len(sorted_responses) == 0:
        return [[]]
    elif len(sorted_responses) == 1:
        return [sorted_responses]
    else:
        sessions = []
        session = [sorted_responses[0]]
        for i in range(len(sorted_responses)-1):
            current_interval = sorted_responses[i+1]["time_of_day"] - sorted_responses[i]["time_of_day"]
            if current_interval <= interval:
                session.append(sorted_responses[i+1])
            else:
                sessions.append(session)
                session = [sorted_responses[i+1]]
        sessions.append(session)
        return sessions

def get_session_info(users_path,is_fake = True):
    
    sessions = mydict()
    
    iterable = range(0,2) if is_fake else os.listdir(users_path)
        
    for filename in iterable:
        context = fake.fake_context() if is_fake else open(users_path + filename, 'r')
        
        with context as f:
            response_dicts = f.user_responses if is_fake else eval(f.read())
            
            
            urls = set()
            user_sessions = {}
            new_responses = []
            for response in response_dicts:
                response = mydict(response)
                url = response["url"]
                response["time_of_day"] = int(response["time_of_day"])

                time_sending = int(response["time_sending"])
                if time_sending == 0:
                    continue

                new_responses.append(response)
                '''
                if url:
                    if url not in user_sessions:
                        user_sessions[url] = [response]
                    else:
                        user_sessions[url].append(response)
                        '''
            
           
            
            new_responses.sort(key=lambda d:d["time_of_day"])
            if len(new_responses) != 0:
                user_sessions[new_responses[0]["url"]] = new_responses
            
            
            for url in user_sessions:
                responses = user_sessions[url]
                responses.sort(key=lambda d:d["time_of_day"])
                if url in sessions:
                    sessions[url].extend(session_interval_split(responses,session_interval))
                else:
                    sessions[url] = []
                    sessions[url].extend(session_interval_split(responses,session_interval))
                    
    return sessions

def get_session_length(session):
    return session[len(session)-1]["time_of_day"] - session[0]["time_of_day"]

def is_valid_file_size(file_size):
    return not(file_size == "-" or file_size == "NIL" or file_size == None or file_size == "0")

def get_session_stats(sessions):
    session_stats = []
    for url in sessions:
        for session in sessions[url]:
            session_stat = {}
            STATS = ["time_of_day_first","content_type","user","length","bytes_sent","file_size","device","os","url","speed","days_of_week","percent_buffered", "requests","requests_with_valid_file_size","customer_id","server_id","time_series"]
            
            user = session[0]["user"]
            time_of_day_first = session[0]["time_of_day"]
            content_type = session[0]["content_type"]
            
            bytes_sent = 0.0
            total_file_size = 0.0
            requests = len(session)
            days_of_week = []
            time_series = {}
            first_times = []
            
            requests_with_valid_file_size = 0
            
            for response in session:
                time_sending = float(response["time_sending"])/1000
                first_times.append(response["time_of_day"] - time_sending)
                day_of_week = datetime.datetime.fromtimestamp(response["time_of_day"]).strftime("%A")
                hour = time.strftime('%H', time.localtime(response["time_of_day"]))
                key = "{0}_hour_{1}".format(day_of_week,hour)
                
                
                response_bytes = float(response["bytes_sent"])
                response_file_size = response["file_size"]
                
                if is_valid_file_size(response_file_size):
                    requests_with_valid_file_size += 1
                    
                    if day_of_week not in days_of_week:
                        days_of_week.append(day_of_week)
                    
                    if key not in time_series:
                        time_series[key] = response_bytes
                    else:
                        time_series[key] = time_series[key] + response_bytes
                        
                    bytes_sent += response_bytes
                    total_file_size += float(response_file_size)
                    
            if requests_with_valid_file_size == 0:
                file_size = None
            else:
                file_size = total_file_size/requests_with_valid_file_size
            
            first_times.sort()
            length = session[len(session)-1]["time_of_day"] - first_times[0] #  get_session_length(session) #
            
            os = session[0]["user_agent_os"]
            device = session[0]["user_agent_device"]
            
            if length == 0.0:
                length = None
                speed = None
            else:
                speed = bytes_sent/length
            
            if file_size == None:
                percent_buffered = None
            else:
                percent_buffered = bytes_sent/file_size
            
            customer_id = session[0]["customer_id"]
            server_id = session[0]["server_id"]
            
            
            for stat in STATS:
                session_stat[stat] = locals()[stat]
            session_stats.append(session_stat)
    return session_stats


        
class mydict(dict):
    #if "NIL" is set as a value, returns None
    def __getitem__(self,key):
        value = super(mydict,self).__getitem__(key)
        if value == "NIL":
            return None
        else:
            return value
            

def get_small_session_stats():
    

    users_path = r"C:\Users\NormanVIII\Downloads\Users\Users\\"
    sessions = get_session_info(users_path,is_fake = False)
    session_stats = get_session_stats(sessions)
    return session_stats


session_interval = 600

    

    



