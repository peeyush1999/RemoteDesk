import socket
import threading
import numpy as np
import cv2
import pickle
import pyautogui
import sys

#HOST = '192.168.1.5'
HOST = socket.gethostbyname(socket.gethostname())
print("Ask Client To put in This in IP :",HOST) #on Same network
PORT =  7777

drag = False

def mouse_click(event, x, y,flags, param): 

    global drag
    curx,cury = pyautogui.position()
    curx = str(curx).encode('utf-8')
    cury = str(cury).encode('utf-8')
    
    if event == cv2.EVENT_LBUTTONDBLCLK:
        param[0].sendall(b'HLO'+b'LBTNDLK:'+curx+b','+cury+b'END')
        print('Double Click')
        
    if event == cv2.EVENT_LBUTTONDOWN:
        param[0].sendall(b'HLO'+b'LBTND:'+curx+b','+cury+b'END')
        drag = True
        print('Left Click')

    if event == cv2.EVENT_MOUSEMOVE:
        if drag:
            param[0].sendall(b'HLO'+b'DMOVE:'+curx+b','+cury+b'END')
        else:
            param[0].sendall(b'HLO'+b'MOVE:'+curx+b','+cury+b'END')

    if event == cv2.EVENT_LBUTTONUP:
        drag = False
        param[0].sendall(b'HLO'+b'LBTNU:'+curx+b','+cury+b'END')
        
    if event == cv2.EVENT_RBUTTONDOWN: 
        param[0].sendall(b'HLO'+b'RBTND:'+curx+b','+cury+b'END')
        print('Right Click')
         
  




            
    
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


cv2.namedWindow("screen")


with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.bind((HOST,PORT))
    s.listen()
    print("Started Lisenting")
    conn,addr = s.accept()
    
    
    with conn:
        print("Connected by :" ,addr)
        cv2.setMouseCallback("screen", mouse_click,param=[conn])
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
                    

    
 
