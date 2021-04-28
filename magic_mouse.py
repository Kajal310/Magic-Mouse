import cv2
import mouse
import numpy as np
import math
 

    
def isPointClose(x1,y1,x2,y2,scale):
    len=math.sqrt((x1-x2)**2+(y1-y2)**2);
    if len<=scale:     
        return True;
    else :
        return False;
    
capture=cv2.VideoCapture(0);
background=cv2.flip(capture.read()[1],1);
width=np.shape(background)[1];
height=np.shape(background)[0];
background=background[1:height-199,250:width].copy();
app=wx.App(False);
(sx,sy)=wx.GetDisplaySize();


mouseOn=0;
while True:
    frame=cv2.flip(capture.read()[1],1);
    
    
    roi=frame[1:height-199,250:width].copy();
    temp_roi=roi.copy();
    
    fmask=cv2.absdiff(background,roi,0);
    fmask=cv2.cvtColor(fmask,cv2.COLOR_BGR2GRAY);
    fmask=cv2.threshold(fmask,10,255,0)[1];
    fmask=cv2.erode(fmask,cv2.getStructuringElement(cv2.MORPH_ERODE,(2,2)),iterations=2);
    mask1=cv2.morphologyEx(fmask,cv2.MORPH_CLOSE,\
                           cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(4,4)));
    mask1=cv2.erode(mask1,cv2.getStructuringElement(cv2.MORPH_ERODE,(2,2)),iterations=2);
    cv2.imshow('mask1',mask1);
    fg_frame=cv2.bitwise_and(roi,roi,mask=mask1);
    cv2.imshow('fg_frame',fg_frame);
    
    gr_frame=cv2.cvtColor(fg_frame,cv2.COLOR_BGR2GRAY);
    gr_frame=cv2.blur(gr_frame,(10,10));
    bw_frame=cv2.threshold(gr_frame,50,255,0)[1];
    
    
    contour=cv2.findContours(bw_frame,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0];
    try:
        my_contour=max(contour,key=cv2.contourArea);
    except:
        my_contour=np.array([[[1,0],[1,2],[2,3]]],dtype=np.int32);
        
    try:
        if cv2.contourArea(my_contour)>90:
            
            hull=cv2.convexHull(my_contour,True);
            
            leftmost = tuple(hull[hull[:,:,0].argmin()][0]) 
            rightmost = tuple(my_contour[my_contour[:,:,0].argmax()][0]) 
            topmost = tuple(hull[hull[:,:,1].argmin()][0]) 
            bottommost = tuple(my_contour[my_contour[:,:,1].argmax()][0])
            
            
            temp=bottommost[0]+30 
            cv2.line(roi,topmost,(topmost[0],height-280),(0,242,225),2);
            cv2.line(roi,leftmost,(topmost[0],bottommost[1]-80),(0,242,225),2);
            
            cv2.circle(roi,topmost,5,(255,0,0),-1);
            cv2.circle(roi,leftmost,5,(0,120,255),-1);
            cv2.circle(roi,(temp,bottommost[1]),5,(230,0,255),-1);

            x1=topmost[0];y1=topmost[1];
            x2=bottommost[0]+20;y2=bottommost[1];
            x3=leftmost[0];y3=leftmost[1];
            m1=(y2-y1)/(x2-x1)
            m2=(y3-y2)/(x3-x2)
            tan8=math.fabs((m2-m1)/(1+m1*m2));
            angle=math.atan(tan8)*180/math.pi;
            
            
            #angle = math.atan2(y2 - y1, x2 - x1) * 180.0 / math.pi;
            length=math.sqrt(math.pow((y2-y1),2)+math.pow((x2-x1),2))
            
            if length<50:
                continue
            
            
            x=sx-((topmost[0]-50)*sx/(width-340));
            y=(topmost[1]*sy/(height-281));
            mouse.move(sx-x,y,absolute=True, duration=.1);
            
            
            
            cv2.putText(roi,str('%d,%d'%(sx-x,y)),topmost, cv2.FONT_HERSHEY_SCRIPT_COMPLEX, .5,(255,255,255),1,cv2.LINE_AA)
            if angle<15:
                mouse.click(button='left');    
                print('You have left clicked your mouse');
                pass
            else:
                pass
            
    except:
        pass;
    frame[1:height-199,250:width]=roi;
    cv2.rectangle(frame,(250,1),(width-1,height-200),(0,255,0),2);
    cv2.rectangle(frame,(300,1),(width-40,height-280),(255,0,0),2);
    cv2.imshow('frame',frame);
    if cv2.waitKey(2)==ord('r'):
        print('Your background is reset')
        background=temp_roi;
    elif cv2.waitKey(2)==10:
        break;
cv2.destroyAllWindows();
capture.release();
