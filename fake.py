import time
import random

class fake_context():
    user_id = 0
    
    def __init__(self,n=10):
        self.salt = random.randint(0,4)
        self.user_responses = self.fake(n + self.salt, "user" + str(fake_context.user_id))
        fake_context.user_id = fake_context.user_id + 1
    def __enter__(self):
        return self
    
    def __exit__(self,type,value,traceback):
        #this isn't supposed to do anything
        return None
        
    def random_string_maker(self, n = 10):
        string = ""
        code = 97
        i = 0
        while i < n:
            step = random.randint(0,26)
            string = string + chr(code + step)
        return string
        
    def fake(self,n=5,_user="123"):
        VARS = ["time_of_day","time_sending","user","file_size","server_id","url","user_agent","user_agent_os","user_agent_device","customer_id","byte_range","content_type","bytes_sent"]
        customer_to_url = {}
        user = _user
        fake_responses = []
        init_time = int(time.time())
        time_step = 0
        file_size = random.randint(300,1000)
        for i in range(n):
            init_time = init_time + time_step
            time_of_day = str(init_time)
            time_sending = str(random.randint(0,100))
            fraction = float(random.randint(1,8))/50
            bytes_sent = str(int(fraction*file_size))
            byte_range = "0-100/1000"
            user_agent = "Chrome"
            user_agent_os = "Linux"
            user_agent_device = "iPhone"
            server_id = "ams"
            customer_id = str(random.randint(0,2))
            if customer_id in customer_to_url:
                url = customer_to_url[customer_id]
            else:
                #might want to change this later
                url = customer_id
                customer_to_url[customer_id] = url
            content_type = "mp4"
            
            response = {}
            for var in VARS:
                response[var] = str(locals()[var])
            #sleep for a random amount of time
            fake_responses.append(response)
            time_step = random.randint(1,10)
        '''
        print("---------------------")
        print("user_id: {0}, fake_responses: {1}".format(user,fake_responses))
        '''
        return fake_responses