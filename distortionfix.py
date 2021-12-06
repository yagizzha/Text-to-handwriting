import cv2
import numpy as np


img=cv2.imread("testdrk.jpg")

width=1200
height=1360
arr=np.float32([[48,17],[1157,38],[35,823],[1133,812]])
transformed=np.float32([[0,0],[width,0],[0,height],[width,height]])
print(arr)
for i in range(len(arr)):
    cv2.circle(img,((int)(arr[i][0]),(int)(arr[i][1])),5,(0,0,255),cv2.FILLED)

matrix=cv2.getPerspectiveTransform(arr,transformed)
output=cv2.warpPerspective(img,matrix,(width,height))

cv2.imwrite('outputdrk.jpg', output)
cv2.imshow("original image",img)
cv2.imshow("transformed image",output)

cv2.destroyAllWindows()
