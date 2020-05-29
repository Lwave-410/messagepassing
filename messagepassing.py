import json 
import os
import multiprocessing as mp
sender=[]
receiver=[]
message=[]
with open('C:/Users/ccps6/Desktop/testdata/testdata.json','r') as load_f:
    load_dict=json.load(load_f)
for i in load_dict:
    sender.append(i) 
    receiver.append(load_dict[i][0])
    message.append(load_dict[i][1])
def send(send,message,a,sendqueue,messagequeue,pidqueue,l):
    l.acquire() 
    for i in range (0,len(load_dict)):
        sendqueue.put(sender[i])
        messagequeue.put(message[i])
    pidqueue.put(os.getpid())
    print(os.getpid()," ",sendqueue.get()," send ",messagequeue.get())
    l.release()

def receive(send,receive,message,a,receivequeue,sendqueue,messagequeue,pidqueue,l2):
    l2.acquire()
    for i in range (0,len(load_dict)):
        receivequeue.put(receiver[i])
    print(os.getpid()," ",receivequeue.get()," get ",messagequeue.get(), " from process ",pidqueue.get()," ",sendqueue.get())
    l2.release()
if __name__ == "__main__":
    sendqueue=mp.Queue()
    receivequeue=mp.Queue()
    messagequeue=mp.Queue()
    pidqueue=mp.Queue()
    l=mp.Lock()
    l2=mp.Lock()
    for i in load_dict:
        p=mp.Process(target=send,args=(send,message,os.getpid(),sendqueue,messagequeue,pidqueue,l))
        p.start()
        p.join(10)
    for i in load_dict:
        p2=mp.Process(target=receive,args=(send,receive,message,os.getpid(),receivequeue,sendqueue,messagequeue,pidqueue,l2))
        p2.start()
        p2.join(10)
        
    
   
    
