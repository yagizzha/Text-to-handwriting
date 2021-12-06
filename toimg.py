import cv2
import numpy as np
import random

width=1200
height=1360

transformed=np.float32([[0,0],[width,0],[0,height],[width,height]])
base="drkdpf/drkdpf-"
for i in range(1,14):
    add=str(i)
    if i<10:
        add="0"+add
    print(add)
    img=cv2.imread(base+add+".png")
    rnd=random.randrange(0,3)
    if rnd==0:
        arr=np.float32([[83,95],[1605,89],[87,2089],[1653,2091]])
    if rnd==1:
        arr=np.float32([[37,51],[1653,37],[49,2129],[1685,2187]])
    if rnd==2:
        arr=np.float32([[47,47],[1625,65],[75,2103],[1609,2119]])
    print(arr)
    #for i in range(len(arr)):
        #cv2.circle(img,((int)(arr[i][0]),(int)(arr[i][1])),5,(0,0,255),cv2.FILLED)

    matrix=cv2.getPerspectiveTransform(arr,transformed)
    output=cv2.warpPerspective(img,matrix,(width,height))

    cv2.imwrite("drkR3/"+add+'.jpg', output)

cv2.destroyAllWindows()
