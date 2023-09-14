import cv2 as cv
import numpy as np

im_paths = ['/Users/lukakoll/Downloads/1.jpg',
            '/Users/lukakoll/Downloads/2.jpg',
            '/Users/lukakoll/Downloads/3.jpg',
            '/Users/lukakoll/Downloads/4.jpg']



def qr_identify(qr_path):
    #qr_highlight will contain the list of images with detected qr codes in it
    qr_highlight = []

    for path in qr_path:
        #reading in qr code image
        qr_im = cv.imread(path)
        #gray-scaling qr-code image to prepare for thresholding
        qr_gray = cv.cvtColor(qr_im, cv.COLOR_BGR2GRAY)

        #blurring image to reduce "noise" in image
        blurred = cv.GaussianBlur(qr_gray, (5, 5), 0)
        #Thresholding image(converting all values to (0,0,0) or (255,255,255) based off of an R,G,B threshold
        threshold, binary_image = cv.threshold(blurred, 150, 255, cv.THRESH_BINARY)
        

        #Detecting edges in image
        edges = cv.Canny(binary_image,20,200)

        
        #identifying contours in image;
        #parameter CHAIN_APPROX_SIMPLE used to optimize countours for space efficiency;
        #parameter RETR_CCOMP organized hierarchy of countours
        contours, hierarchy = cv.findContours(edges, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)

        #copying original image 
        qr_im_copy = np.copy(qr_im)
        #cv.drawContours(qr_im_copy, contours, -1,(0, 0, 255), 7)


        #filter contours to a specific size to eliminate undesired countours, and draw those onto copy of original image
        for i, e in enumerate(contours):
            contour_Area = cv.contourArea(e)
            if(contour_Area < 2200 or 400000 < contour_Area):
                continue
            cv.drawContours(qr_im_copy, contours, i, (0, 0, 255), 7)

        qr_highlight.append(qr_im_copy)

    return qr_highlight


print(len(qr_identify(im_paths)))
for highlight in qr_identify(im_paths):
    cv.imshow("binary img", highlight)
    cv.waitKey(0)
    cv.destroyAllWindows()
