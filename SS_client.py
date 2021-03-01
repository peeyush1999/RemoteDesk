import socket
import threading
import sys

import numpy as np 
import cv2 
import pyautogui

import pickle
import time
HOST = '192.168.1.5'
#HOST = '127.0.0.1'
PORT =  4152
dim = (1080,720)

last_image = pyautogui.screenshot()
disp_x,disp_y = last_image.size
#print(dim[0])
#input()

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return int(rightMin + (valueScaled * rightSpan))

def moveMouse(s):
    rdata=b''
    while True:
        data = s.recv(1024)
        rdata = rdata + data
        try:
            cmd = rdata[rdata.index(b'HLO')+3:rdata.index(b'END')]
            print(cmd)
            cmd = cmd.decode('utf-8')
            typ,xy = cmd.split(":")
            x,y = map(int , xy.split(','))
            x = translate(x,0,dim[0],0,disp_x)
            y = translate(y,0,dim[1],0,disp_y)

            if typ == 'MOVE':
                pyautogui.move(x,y,0.5)
            
            rdata = rdata[rdata.index(b'END')+3:]
        except:
            pass
        if(sys.getsizeof(rdata)>65536):
            rdata=b''

    



with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    print('Connected')
    
    t = threading.Thread(target = moveMouse, args=(s,))
    t.start()
    
    last_image = pyautogui.screenshot()
    last_image = cv2.cvtColor(np.array(last_image), cv2.COLOR_RGB2BGR)
    lastk = pickle.dumps(last_image)   
       
    while(True):
        curx,cury = pyautogui.position()
        image = pyautogui.screenshot()
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        image = cv2.circle(image, (curx,cury), 4, [0,0,255], 4)
        #cv2.putText(image,"4", (curx,cury), cv2.FONT_HERSHEY_SIMPLEX, 1, 255,10)
        
        
        image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
        #data = bytes("SIZE:"+str(sys.getsizeof(image)),'utf-8')
        #s.sendall(data)
        #print("SIZE:"+str(sys.getsizeof(image)))
        
        #input()
        k = b'HLO'+pickle.dumps(image)+b'END'
        
        s.sendall(k)
        #print("Frame Send")
        

        
        #print(sys.getsizeof(bytes('end',encoding='utf-8')))
        #time.sleep(0.1)
        
        #input('test')
        #print("Image Sent")

