import msvcrt as ms
import time
#hyperparam
cliplength=10


k=False
starttime=time.time()
while(not k):
    nowtime=time.time()
    secs=nowtime-starttime
    if(secs>cliplength):
        ##do something
        print(secs)
        ##
        starttime=nowtime
    k=ms.kbhit()



