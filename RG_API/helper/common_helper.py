
import os
import datetime as dt
# import constants 


def info(file,message):
    level='info'
    now = dt.date.today()
   
    if os.path.exists("./logs/"+str(now)):
        with open("./logs/"+str(now)+"/"+file,mode="a",encoding="UTF-8") as logf:
            curdt = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            logf.write("["+curdt+"]["+level+"]["+str(message)+"]\n")
            logf.close()
       
    else:    
        os.makedirs("./logs/"+str(now))
        with open("./logs/"+str(now)+"/"+file,mode="a",encoding="UTF-8") as logf:
            curdt = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            logf.write("["+curdt+"]["+level+"]["+str(message)+"]\n")
            logf.close()

def error(file,message):
    level='error'
    now = dt.date.today()
    if os.path.exists("./logs/"+str(now)):
        with open("./logs/"+str(now)+"/"+file,mode="a",encoding="UTF-8") as logf:
            curdt = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            logf.write("["+curdt+"]["+level+"]["+str(message)+"]\n")
            logf.close()
    else:    
        os.makedirs("./logs/"+str(now))
        with open("./logs/"+str(now)+"/"+file,mode="a",encoding="UTF-8") as logf:
            curdt = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            logf.write("["+curdt+"]["+level+"]["+str(message)+"]\n")
            logf.close()

