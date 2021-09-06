import socket
import threading
import sys

import numpy as np 
import cv2 
import pyautogui

import pickle
import time
#HOST = '117.201.91.72'
#HOST = '192.168.1.111'

HOST = str(input("Enter Servers IP: "))
PORT =  7777
dim = (720,480)

dim1 = (1080,720)

last_image = pyautogui.screenshot()
disp_x,disp_y = last_image.size
#print(last_image.size)
#print(dim)


def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return int(rightMin + (valueScaled * rightSpan))
    #return value

def moveMouse(s):
    rdata=b''
    while True:
        data = s.recv(1024)
        #rdata = rdata + data
        cmd = data[data.index(b'HLO')+3:data.index(b'END')]
        cmd = cmd.decode('utf-8')
        print(cmd)
        typ,xy = cmd.split(":")

        if(typ=='KEYP'):
            print("keypress:",xy)
            if(int(xy)==13):
                pyautogui.press('enter')
            else:
                pyautogui.write(chr(int(xy)))

        else:

            
            x,y = map(int , xy.split(','))
            x = translate(x,0,dim1[0],0,disp_x)
            y = translate(y,0,dim1[1],0,disp_y)

            if typ == 'MOVE':
                #print("x=",x,"y=",y)
                pyautogui.moveTo(x,y,0.1)
            elif typ == 'LBTND':
                #print("Left Click")
                pyautogui.click(x,y)
            elif typ == 'LBTNDLK':
                
                pyautogui.click(x,y)
                pyautogui.click(x,y)
                #print("Double Click")
            elif typ == 'RBTND':
                #print("Right Click")
                pyautogui.rightClick(x,y)
            '''    
            try:
                cmd = rdata[rdata.index(b'HLO')+3:rdata.index(b'END')]
                print(cmd)
                cmd = cmd.decode('utf-8')
                typ,xy = cmd.split(":")
                x,y = map(int , xy.split(','))
                x = translate(x,0,dim[0],0,disp_x)
                y = translate(y,0,dim[1],0,disp_y)

                if typ == 'MOVE':
                    print("x=",x,"y=",y)
                    pyautogui.moveTo(x,y,0.1)
                
                
            except Exception as e:
                print(e)

            try:
                rdata = rdata[rdata.index(b'END')+3:]
            except:
                pass
            if(sys.getsizeof(rdata)>65536):
                rdata=b''

            '''



with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    print('Connected')
    
    t = threading.Thread(target = moveMouse, args=(s,))
    t.start()
    
    last_image = pyautogui.screenshot()
    last_image = cv2.cvtColor(np.array(last_image), cv2.COLOR_RGB2BGR)
    lastk = b'HLO'+pickle.dumps(last_image)+b'END'          
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
        #if(k!=lastk):
        s.sendall(k)
            #print("Frame Send")
        

        
        #print(sys.getsizeof(bytes('end',encoding='utf-8')))
        #time.sleep(0.1)
        
        #input('test')
        #print("Image Sent")

