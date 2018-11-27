import msvcrt as ms
import os
import subprocess as sp
import threading as th
import time
from os import path
import speech_recognition as sr
import win32con
import win32api

##hyperparam
time_delay=0
exe_name="\\wasapi_capture.exe"
clip_length=2
mode=b'c'
#c:output to cmd
#t:output by typing

#get exe path
current_dir,fn=os.path.split(__file__)
exe_path=current_dir+exe_name
#queue
queue_process_handle=[None,None,None]
queue_wav_name=[-1,-1,-1]
queue_size=3
queue_head=0

#wait to start
k=False;starttime=time.time()
while(not k):
    if((time.time()-starttime)>1):
        starttime=time.time()
        print("ready")
    k=ms.kbhit()    
print("start recording")
#init
mode=ms.getch()#clear key buffer,kbhit init

def rcgnz(num):
    wave_file="\\"+str(num)+".wav"
    AUDIO_FILE=current_dir+wave_file
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file
    try:
        result=r.recognize_sphinx(audio)
        if(mode==b't'):
            type_string(result)
        else:
            print(result)
    except sr.UnknownValueError:
        if(mode==b't'):
            type_string("")
        else:
            print("")
def wk(n,pos):
    global queue_size,queue_process_handle,queue_wav_name
    p=sp.Popen([exe_path,str(n),str(clip_length)]
    ,stdout=sp.PIPE,stdin=sp.PIPE)
    queue_process_handle[pos]=p
    queue_wav_name[pos]=n
def open_sub():
    global wav_num,queue_process_handle,queue_size
    if(queue_process_handle[0]==None):
        for i in range(queue_size):
            ###prepare 3 threads 
            t=th.Thread(target=wk,args=(wav_num,i))
            t.start()
            wav_num+=1
        return    
    for i in range(queue_size):
        if(queue_process_handle[i].poll()==0):
            ###recognize
            t=th.Thread(target=rcgnz,args=(queue_wav_name[i],))
            t.start()
            ###creates a new thread
            t=th.Thread(target=wk,args=(wav_num,i))
            t.start()
            wav_num+=1
            
def type_string(tstring):
    ###only for A-Z a-z 0-9###
    key_shift=16
    key_enter=13
    for ch in tstring:
        key_ch=ord(ch)
        if((key_ch<=ord('z'))and(ord('a')<=key_ch)):
            key_ch=key_ch-ord('a')+ord('A')#convert to upper case
            win32api.keybd_event(key_ch,0,0,0)
            win32api.keybd_event(key_ch,0,win32con.KEYEVENTF_KEYUP,0)
        elif((key_ch<=ord('Z'))and(ord('A')<=key_ch)):
            win32api.keybd_event(key_shift,0,0,0)
            win32api.keybd_event(key_ch,0,0,0)
            win32api.keybd_event(key_ch,0,win32con.KEYEVENTF_KEYUP,0)
            win32api.keybd_event(key_shift,0,win32con.KEYEVENTF_KEYUP,0)
        else:
            win32api.keybd_event(key_ch,0,0,0)
            win32api.keybd_event(key_ch,0,win32con.KEYEVENTF_KEYUP,0)
    win32api.keybd_event(key_enter,0,0,0)
    win32api.keybd_event(key_enter,0,win32con.KEYEVENTF_KEYUP,0)
wav_num=0
#first recording
open_sub()
time.sleep(1)#wait for thread
p=queue_process_handle[0]
p.stdin.write("s".encode("GBK"))
p.stdin.flush()
wav_num=3;queue_head=0

start_time=time.time()
k=False
check=False
while(not k):
    nowtime=time.time()
    secs=nowtime-start_time

    if(secs>(clip_length)):
        #start recording
        p=queue_process_handle[queue_head]
        p.stdin.write("s".encode("GBK"))
        p.stdin.flush()
        queue_head=(queue_head+1)%queue_size
        start_time=nowtime
        check=True
    elif(secs<(clip_length/3)and check):
        #program is waiting
        #prepare thread
        t=th.Thread(target=open_sub,name="t_op_sub")
        t.start()
        check=False
    
    k=ms.kbhit()
