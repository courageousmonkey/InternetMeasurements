import os
import datetime
import time
import multiprocessing
import itertools
import glob


def session_interval_split(sorted_responses,interval):
    
    if len(sorted_responses) == 0:
        return [[]]
    elif len(sorted_responses) == 1:
        return [sorted_responses]
    else:
        sessions = []
        session = [sorted_responses[0]]
        for i in range(len(sorted_responses)-1):
            current_interval = sorted_responses[i+1]["time_of_day_modified"] - sorted_responses[i]["time_of_day_modified"]
            if current_interval <= interval:
                session.append(sorted_responses[i+1])
            else:
                sessions.append(session)
                session = [sorted_responses[i+1]]
        sessions.append(session)
        return sessions

def process_files(file_path):
    #20 minutes
    session_interval = 1200
    no_weird = False
    with open(file_path, 'r') as f:
        response_dicts = eval(f.read())
        
        
        urls = set()
        user_sessions = {}
        new_responses = []
        for response in response_dicts:
            response = mydict(response)
            url = response["url"]
            response["time_of_day"] = int(response["time_of_day"])
            time_sending = int(response["time_sending"])
            response["time_of_day_modified"] = response["time_of_day"] - float(time_sending)/1000
            if time_sending == 0 and no_weird:
                continue
            
            #new_responses.append(response)

            if url:
                if url not in user_sessions:
                    user_sessions[url] = [response]
                else:
                    user_sessions[url].append(response)

        '''
        if len(new_responses) == 0:
            return []
        session_stats = []
        new_responses.sort(key=lambda d:d["time_of_day"])
        session_stats.extend(output_session_stats([new_responses]))
        '''

        session_stats = []
        for url in user_sessions:
            responses = user_sessions[url]
            responses.sort(key=lambda d:d["time_of_day_modified"])
            #session_stats.extend(output_session_stats(False,[responses]))
            session_stats.extend(output_session_stats(False,session_interval_split(responses,session_interval)))

    return session_stats
            
def output_session_info(users_path,session_interval):
    print("output_session_info")
    p = multiprocessing.Pool(4)
    files = os.listdir(users_path)
    iterable = ((users_path + filename,session_interval) for filename in files)
    p.map(process_files,iterable)
                
def is_valid_file_size(file_size):
    return not(file_size == "-" or file_size == "NIL" or file_size == None or file_size == "0")
                        
def output_session_stats(ignore_strange,url_sessions):
    session_stats = []
    for session in url_sessions:
        session_stat = {}
        STATS = ["time_of_day_first","time_of_day_last","content_type","user","length","bytes_sent","file_size","device","os","url","speed","days_of_week","percent_buffered", "requests","customer_id","server_id","time_series"]

        min_length = 5
        max_length = 14400

        min_percent_buffered = 0
        max_percent_buffered = 5


        url = session[0]["url"]
        
        user = session[0]["user"]
        time_of_day_first = session[0]["time_of_day_modified"]
        content_type = session[0]["content_type"]
        
        
        bytes_sent = 0.0
        total_file_size = 0.0
        requests = len(session)
        days_of_week = []
        time_series = {}
        #don't need first_times anymore?
        first_times = []
        
        requests_with_valid_file_size = 0
        for response in session:
            time_sending = float(response["time_sending"])/1000
            first_times.append(response["time_of_day_modified"])
            
            day_of_week = datetime.datetime.fromtimestamp(response["time_of_day_modified"]).strftime("%A")
            hour = time.strftime('%H', time.localtime(response["time_of_day_modified"]))
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
        time_of_day_last = session[len(session)-1]["time_of_day"]
        length = time_of_day_last - first_times[0] #  get_session_length(session) #
        
        os = session[0]["user_agent_os"]
        device = session[0]["user_agent_device"]
        
        if (not (min_length <= length and length <= max_length)) and ignore_strange:
            session_stats.append(None)
            continue

        if length == 0:
            length = None
            speed = None
        else:
            speed = bytes_sent/length


        if file_size == None:
            if ignore_strange:
                session_stats.append(None)
                continue
            else:
                percent_buffered = None
        else:
            percent_buffered = bytes_sent/file_size

        if (not(min_percent_buffered <= percent_buffered and percent_buffered <= max_percent_buffered)) and ignore_strange:
            session_stats.append(None)
            continue
        
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
            
if __name__ == "__main__":
    #threshold to be considered a different session
    start = time.time()
    users_path = "/Users/macdaddy/Downloads/Users/*.json"
    #users_path = "C:\Users\NormanVIII\Downloads\Users\Users\*.json"
    
    out_path = "/Users/macdaddy/Documents/InternetMeasurement/internetMeasurement/data/sessions_interval_not_clumped_weird.txt"
    p = multiprocessing.Pool(8)
    files = glob.iglob(users_path)
    count = 0
    step = 50000
    while True:
        print("count: " + str(count))
        '''
        lists_of_session_stats = []
        for file_path in itertools.islice(files,0,step):
            lists_of_session_stats.append(process_files(file_path))
            '''
            
        lists_of_session_stats = p.map(process_files,itertools.islice(files,0,step))
        
        if len(lists_of_session_stats) == 0:
            break
        with open(out_path,'a') as fout:
            for group in lists_of_session_stats:
                fout.write(str(group) + "\n")
        count += step
    
    end = time.time()    
