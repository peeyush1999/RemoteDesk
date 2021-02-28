import socket
import threading
import sys

import numpy as np 
import cv2 
import pyautogui

import pickle
import time
HOST = '192.168.1.111'
#HOST = '127.0.0.1'
PORT =  2514
dim = (360,360)
    
    

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    print('Connected')
    

    last_image = pyautogui.screenshot()
    last_image = cv2.cvtColor(np.array(last_image), cv2.COLOR_RGB2BGR)
    lastk = pickle.dumps(last_image)   
       
    while(True):
        image = pyautogui.screenshot()
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
        #data = bytes("SIZE:"+str(sys.getsizeof(image)),'utf-8')
        #s.sendall(data)
        #print("SIZE:"+str(sys.getsizeof(image)))
        
        #input()
        k = b'HLO'+pickle.dumps(image)+b'END'
        
        s.sendall(k)
        print("Frame Send")
        

        
        #print(sys.getsizeof(bytes('end',encoding='utf-8')))
        #time.sleep(0.1)
        
        #input('test')
        #print("Image Sent")

