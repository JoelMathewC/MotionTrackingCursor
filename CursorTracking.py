import cv2
import numpy as np
import pyautogui


def nothing(x):
    print(x)

pyautogui.FAILSAFE = False

cv2.namedWindow('Track')
cv2.createTrackbar('Left','Track',0,640,nothing)
cv2.createTrackbar('Right','Track',640,640,nothing)
cv2.createTrackbar('Top','Track',0,480,nothing)
cv2.createTrackbar('Bottom','Track',480,480,nothing)
cv2.createTrackbar('Filter','Track',0,255,nothing)
cv2.createTrackbar('Select','Track',0,1,nothing)


cap = cv2.VideoCapture(0)





valid_state = False
while(cap.isOpened()):
    

    ret, frame = cap.read()
    if ret == False:
        break

    roi = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    roi = cv2.flip(roi,1)
    

    #choosing the region of Intrest
    l = cv2.getTrackbarPos('Left','Track')
    r = cv2.getTrackbarPos('Right','Track')
    t = cv2.getTrackbarPos('Top','Track')
    b = cv2.getTrackbarPos('Bottom','Track')
    roi = roi[t:b,l:r] 

    row,col = roi.shape
   
    
    
    #show = cv2.GaussianBlur(show,(7,7),0)
    


    #Selecting a Threshold for detection of Pupil
    validity = cv2.getTrackbarPos('Select','Track')
    
    if validity == 1:
        valid_state = True

    
    filter = cv2.getTrackbarPos('Filter','Track')
    
    _, thresh = cv2.threshold(roi,filter,255,cv2.THRESH_BINARY)
    
    contours,_ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours,key = lambda x: cv2.contourArea(x),reverse = True)

    
    
    for cnt in contours:
        (x,y,w,h) = cv2.boundingRect(cnt)
        cv2.rectangle(roi,(x,y),(x+w,y+h),(255,0,0),1)
        cv2.line(roi, (x + int(w/2), 0), (x + int(w/2), 350), (0, 255, 0), 1)
        cv2.line(roi, (0, y + int(h/2)), (620, y + int(h/2)), (0, 255, 0), 1)
        x = x + int(w/2)
        y = y + int(h/2)
        print(str(x)+','+str(y)+':'+str(x*5)+','+str(y*2))

        multiX = float(1920/col)
        multiY = float(1080/row)
        if valid_state is True:
            pyautogui.moveTo(x*multiX,y*multiY)
        break


        

    show = cv2.pyrUp(roi)
    show = cv2.pyrUp(show)
    show = cv2.pyrUp(show)
    cv2.imshow('feed',roi)
    cv2.imshow('Mask',thresh)
    
    
    if cv2.waitKey(1) == 27:
        break


cap.release()
cv2.destroyAllWindows()


