#filters module
#devices - computer,mobile,console,NIL
#os - android, iphone, ipod, ubuntu, windows xp, xbox, playstation, ...

''' start customer ids '''
def pornflixer(session):
    return session["customer_id"] == "27095"
    
def sugardaddy(session):
    return session["customer_id"] == "15068"
    
def hustler(session):
    return session["customer_id"] == "17587"
    
def eurorevenue(session):
    return session["customer_id"] == "33803"
    
def indieclicktv(session):
    return session["customer_id"] == "8376"

def weird2(session):
    return session["customer_id"] == "25382"
    
def weird3(session):
    return session["customer_id"] == "9194"
    
def world_television(session):
    #max says this is a bust
    return session["customer_id"] == "4540"
    
def viki(session):
    return session["customer_id"] == "13642"
    
def deviantclips(session):
    return session["customer_id"] == "10872"
    
def yupptv(session):
    return session["customer_id"] == "20313"
    
def hulu(session):
    return session["customer_id"] == "20653"
    
def shufuni(session):
    return session["customer_id"] == "10832"

def dailymotion(session):
    return session["customer_id"] == "16234"
    
def break_web(session):
    return session["customer_id"] == "3774"
    
def redtube(session):
    return session["customer_id"] == "9055"
    
''' end customer ids '''

def flash(session):
    content_type = session["content_type"]
    return content_type == "flv" or content_type == "x-flv"

''' start label funcs '''
def user_label(session):
    user = session["user"]
    return user
    
def content_type_label(session):
    content_type = session["content_type"]
    return content_type
    
def device_label(session):
    device = session["device"]
    return device
    
def max_wants_label(session):
    if adult(session):
        return "adult sites"
    elif youtube_like(session):
        return "video sharing sites"
    elif hulu_like(session):
        return "episode streaming sites"
    else:
        return None
        
def customer_id_label(session):
    customer_id = session["customer_id"]
    return customer_id
    
def special_customer_id_label(session):
    if computer(session) and not ios(session):
        return customer_id_label(session)
        
def find_out_how_much_non_adult_flash_label(session):
    if(computer_and(redtube)(session)):
        return "redtube computer"
    elif(redtube(session)):
        return "redtube other"
    elif(flash_and(and_func(negate(adult),negate(hulu)))(session)):
        return "not redtube non_adult flash"
    else:
        return None
        
def non_adult_flash_customer_id_label(session):
    if(computer_and(redtube)(session)):
        return None
    elif(redtube(session)):
        return None
    elif(flash_and(and_func(negate(adult),negate(hulu)))(session)):
        return customer_id_label(session)
    else:
        return None
    
''' end label funcs '''

def weird_ios(session):
    return computer(session) and ios(session)
    
def adult(session):
    adult_list=[deviantclips,shufuni,redtube,eurorevenue,pornflixer,sugardaddy,hustler]
    return any_2(session,adult_list)
    
def non_adult(session):
    non_adult_list = [youtube_like,hulu_like]
    return any_2(session,non_adult_list)
    
def youtube_like(session):
    youtube_like_list = [dailymotion,break_web]
    return any_2(session,youtube_like_list)
    
def hulu_like(session):
    hulu_like_list = [hulu,viki]
    return any_2(session,hulu_like_list)
    
def mobile(session):
    device = session["device"]
    if device == None:
        return False
    else:
        return device == "mobile"
        
def computer(session):
    device = session["device"]
    if device == None:
        return False
    else:
        return device == "computer"

def ios(session):
    os = session["os"]
    if os == None:
        return False
    else:
        return "ios" == os.lower()
        
def windows(session):
    os = session["os"]
    if os == None:
        return False
    else:
        return "windows" in os.lower()
    
def mac(session):
    os = session["os"]
    if os == None:
        return False
    else:
        return "mac" in os.lower()
    
def yes_man(session):
    return True
    
def europe(session):
    server_location = session["server_id"]
    if server_location == None:
        return False
    else:
        return server_location == "ams"
        
def america(session):
    server_location = session["server_id"]
    if server_location == None:
        return False
    else:
        return server_location == "atl"

''' start higher order '''
def negate(func):
    return lambda x: not func(x)
    
def and_func(func1,func2):
    return lambda x: func1(x) and func2(x)
    
def mobile_and(func):
    return and_func(mobile,func)
    
def america_and(func):
    return and_func(america,func)

def europe_and(func):
    return and_func(europe,func)
    
def any_func(list_of_filter_funcs):
    return lambda x : any_2(x,list_of_filter_funcs)
    
def every_func(list_of_filter_funcs):
    return lambda x : every_2(x, list_of_filter_funcs)
    
def any_2(session,list_of_filter_funcs):
    at_least_one = False
    for filter_func in list_of_filter_funcs:
        at_least_one = at_least_one or filter_func(session)
    return at_least_one

def every_2(session, list_of_filter_funcs):
    every_one = True
    for filter_func in list_of_filter_funcs:
        every_one = every_one and filter_func(session)
    return every_one
    
def computer_and(func):
    return lambda x: computer(x) and func(x)
    
def flash_and(func):
    return lambda x: flash(x) and func(x)
''' end higher order '''

