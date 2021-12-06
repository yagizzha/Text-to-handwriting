import numpy as np
import cv2 
import glob



################ FIND CHESSBOARD CORNERS - OBJECT POINTS AND IMAGE POINTS #############################
def fixshape():
    chessboardSize = (16,14)
    cx=chessboardSize[1]
    cy=chessboardSize[0]

    frameSize = (1200,1360)
    #frameSize=(1345,799)


    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)


    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
    objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)


    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.


    images = glob.glob('*.jpg')

    img = cv2.imread(images[0])
    cv2.imshow("a",img)
    for image in images:

        img = cv2.imread(image)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, chessboardSize, None)

        # If found, add object points, image points (after refining them)
        if ret == True:

            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners)
            cv2.circle(img,((int)(corners[0][0][0]),(int)(corners[0][0][1])),5,(0,0,255),cv2.FILLED)
            cv2.circle(img,((int)(corners[cx*cy-1][0][0]),(int)(corners[cx*cy-1][0][1])),5,(0,255,0),cv2.FILLED)
            cv2.circle(img,((int)(corners[cy-1][0][0]),(int)(corners[cy-1][0][1])),5,(255,0,0),cv2.FILLED)
            cv2.circle(img,((int)(corners[cx*cy-cy][0][0]),(int)(corners[cx*cy-cy][0][1])),5,(255,255,255),cv2.FILLED)
            # Draw and display the corners
            cv2.drawChessboardCorners(img, chessboardSize, corners2, ret)
            cv2.imwrite("processing.jpg",img)
            cv2.imshow('img', img)
            cv2.waitKey(1000)


    cv2.destroyAllWindows()



    ############## CALIBRATION #######################################################

    ret, cameraMatrix, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, frameSize, None, None)


    ############## UNDISTORTION #####################################################

    img = cv2.imread('distest5.jpg') ###PICTURE TO FIX
    h,  w = img.shape[:2]
    newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))



    # Undistort
    dst = cv2.undistort(img, cameraMatrix, dist, None, newCameraMatrix)

    # crop the image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    cv2.imwrite('caliResult1.png', dst)

    imgf = cv2.imread('distest.jpg') ###CHECKBOARD ONLY
    hf,  wf = imgf.shape[:2]
    newCameraMatrix, roif = cv2.getOptimalNewCameraMatrix(cameraMatrix, dist, (wf,hf), 1, (wf,hf))



    # Undistort
    dstf = cv2.undistort(imgf, cameraMatrix, dist, None, newCameraMatrix)

    # crop the image
    xf, yf, wf, hf = roif
    dstf = dstf[y:y+hf, x:x+wf]
    cv2.imwrite('caliResult11.png', dstf)

    ##########################
    gr=cv2.cvtColor(dstf, cv2.COLOR_BGR2GRAY)
    ret, crn = cv2.findChessboardCorners(gr, chessboardSize, None)


    if ret == True:
        print("We in chief")
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gr, crn, (11,11), (-1,-1), criteria)
        imgpoints.append(crn)
        cv2.circle(dst,((int)(crn[cy-1][0][0]),(int)(crn[cy-1][0][1])),15,(255,0,0),cv2.FILLED)
        cv2.circle(dst,((int)(crn[cx*cy-1][0][0]),(int)(crn[cx*cy-1][0][1])),10,(0,255,0),cv2.FILLED)
        cv2.circle(dst,((int)(crn[0][0][0]),(int)(crn[0][0][1])),5,(0,0,255),cv2.FILLED)
        cv2.circle(dst,((int)(crn[cx*cy-cy][0][0]),(int)(crn[cx*cy-cy][0][1])),5,(255,255,255),cv2.FILLED)



        arr=np.float32([
                            [(int)(crn[cx*cy-cy][0][0]),(int)(crn[cx*cy-cy][0][1])],    
                            [(int)(crn[0][0][0]),(int)(crn[0][0][1])],
                            [(int)(crn[cx*cy-1][0][0]),(int)(crn[cx*cy-1][0][1])],
                            [(int)(crn[cy-1][0][0]),(int)(crn[cy-1][0][1])]])
        print(arr)
        width=abs((int)(crn[cx*cy-1][0][0]-crn[cy-1][0][0]))
        height=abs((int)(crn[0][0][1]-crn[cy-1][0][1]))
        transformed=np.float32([[0,0],[width,0],[0,height],[width,height]])
        matrix=cv2.getPerspectiveTransform(arr,transformed)
        output=cv2.warpPerspective(dst,matrix,(width,height))
        cv2.imshow("imga",dst)
        cv2.imshow("imgb",output)
        cv2.imwrite("caliResultFinal1.png",output)
    cv2.imwrite('caliResult4.png', dst)

    """
    for i in range(len(arr)):
        cv2.circle(dst,((int)(arr[i][0]),(int)(arr[i][1])),5,(0,0,i*60),cv2.FILLED)
        print(arr[i][0],arr[i][1])"""

    cv2.imwrite('caliResult7.png', dst)



fixshape()
"""
# Undistort with Remapping+UD
mapx, mapy = cv2.initUndistortRectifyMap(cameraMatrix, dist, None, newCameraMatrix, (w,h), 5)
dst = cv2.remap(dst, mapx, mapy, cv2.INTER_LINEAR)

# crop the image
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
cv2.imwrite('caliResult3.png', dst)



# Undistort with Remapping
mapx, mapy = cv2.initUndistortRectifyMap(cameraMatrix, dist, None, newCameraMatrix, (w,h), 5)
dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)

# crop the image
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
cv2.imwrite('caliResult2.png', dst)




# Reprojection Error
mean_error = 0

for i in range(len(objpoints)):
    continue
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], cameraMatrix, dist)
    error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
    mean_error += error

print( "total error: {}".format(mean_error/len(objpoints)) )"""
