import socket
import threading
import pyperclip
from PIL import ImageGrab
from PIL import Image
import io
import numpy as np
import cv2
from PIL import Image
import pickle
import math
import sys

#HOST = '192.168.1.5'
HOST = socket.gethostbyname(socket.gethostname())
print("Ask Client To put in This in IP :",HOST) #on Same network
PORT =  2514


def show(data):
    print("in show function")
    sz = sys.getsizeof(data)
    print("size od data recv :",sz)
    if(sz>50):
        img = pickle.loads(data)
        cv2.imshow("screen",img)
        cv2.waitKey(1)
            
    
def recvData(conn):
    msize=0
    tmp=0
    rdata = bytes('',encoding='utf-8')
    i=0
    rdata=b''
    while(True):
            
            data = conn.recv(65496)
            rdata += data

            try:
                image = rdata[rdata.index(b'HLO')+3:rdata.index(b'END')]
                rdata = rdata[rdata.index(b'END')+3:]
                img = pickle.loads(image)
                cv2.imshow("screen",img)
                if cv2.waitKey(1) & 0xFF == ord('q'): 
                    break
                
            except Exception as e:
                pass

                
with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.bind((HOST,PORT))
    s.listen()
    print("Started Lisenting")
    conn,addr = s.accept()
    
    
    with conn:
        print("Connected by :" ,addr)
        recvData(conn)
        '''
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(data)
        '''

    print("connection closed") 
    s.close()
                    

    
 
