import numpy as np
import cv2 as cv
import math
import os
from PIL import Image

#List im_path contains image paths to four corners of QR code
im_path = ['/Users/lukakoll/Downloads/1-cropped.png',
           '/Users/lukakoll/Downloads/2-cropped.png',
           '/Users/lukakoll/Downloads/3-cropped.png',
           '/Users/lukakoll/Downloads/4-cropped.png']

#Corner points of QR code to be flattened; list corner_points contains corner points of four images
#corner points are adjusted to curtail the images with respect to qr overlap in the images;
#this means that flattened image will not represent whole qr segment, but instead only the non-overlapping portions that we need
corner_pts_1 = [[105, 28], [291, 83], [47, 236], [239, 288]]
corner_pts_2 = [[27, 60], [155, 63], [23, 173],[151, 173]]
corner_pts_3 = [[50, 94], [274, 36], [104, 296], [328, 238]]
corner_pts_4 = [[146, 74], [423, 85], [127, 380], [405, 395]]

corner_points = [corner_pts_1, corner_pts_2, corner_pts_3, corner_pts_4]



#Function flatten_img takes in image path and array corner_points with corner points of image segment to be flattened; Returns flattened image
def flatten_img(corner_points, image_path):
    QR_im = cv.imread(image_path)
    #x, y coordinates of corner points presented in list: corner_points = [top_left, top_right, bottom_left, bottom_right]

    top_left, top_right, bottom_left, bottom_right = corner_points[0], corner_points[1], corner_points[2], corner_points[3]


    #Determining new image height and width by finding distance between corner points of original image
    im_width = int(math.sqrt((top_right[0]-top_left[0])**2 +(top_right[1]-top_left[1])**2))
    im_height = int(math.sqrt((top_right[0]-bottom_right[0])**2+(top_right[1]-bottom_right[1])**2))



    #converting to array scalar data type for corner points of original image, and perspective transformed image
    im1_corners = np.float32([top_left, top_right, bottom_left, bottom_right])
    im2_corners = np.float32([[0, 0], [im_width, 0], [0, im_height], [im_width, im_height]])

    #transforming perspective of image(straightening)
    matrix = cv.getPerspectiveTransform(im1_corners, im2_corners)
    new_im = cv.warpPerspective(QR_im, matrix, (im_width, im_height))

    return new_im

#Changing os Directory to save image in
os.chdir('/Users/lukakoll/Downloads')


#looping through images in im_path
for x in range(0, len(im_path)):
    #displaying flattened image at index x
    cv.imshow("New_Image", flatten_img(corner_points[x], im_path[x]))
    cv.waitKey(0)
    #saving flattened image in directory '/Users/lukakoll/Downloads'
    cv.imwrite(f"flattened_im_{x}.jpg", flatten_img(corner_points[x], im_path[x]))
   
    

cv.destroyAllWindows()


#Determined that cropped_im_1 was bottom right quadrant as it lacks an eye/finder pattern
#Determined that cropped_im_3 is the top left quadrant as it is the only quadrant with a
#black and white alternating timing pattern on both sides of the finder pattern
#Determined that cropped_im_4 was the top right quadrant, and that cropped_im_2 was the
#bottom left quadrant by seeing where the finder patterns matched to cropped_im_3


#We will now rotate the top right, bottom left, and bottom right images to be in correct orientation
im_3 = Image.open('/Users/lukakoll/Downloads/flattened_im_3.jpg')
im_3_rotated = im_3.rotate(180, Image.NEAREST, expand = 1)
im_3_rotated.save('flattened_im_3_rotated.jpg')

im_1 = Image.open('/Users/lukakoll/Downloads/flattened_im_1.jpg')
im_1_rotated = im_1.rotate(90, Image.NEAREST, expand = 1)
im_1_rotated.save('flattened_im_1_rotated.jpg')

im_0 = Image.open('/Users/lukakoll/Downloads/flattened_im_0.jpg')
im_0_rotated = im_0.rotate(90, Image.NEAREST, expand = 1)
im_0_rotated.save('flattened_im_0_rotated.jpg')

    

#list flattened_im_paths contains the paths of the flattened images in the order that they appear from: top left, top right, bottom left, bottom right
flattened_im_paths = ['/Users/lukakoll/Downloads/flattened_im_2.jpg',
                      '/Users/lukakoll/Downloads/flattened_im_3_rotated.jpg',
                      '/Users/lukakoll/Downloads/flattened_im_1_rotated.jpg',
                      '/Users/lukakoll/Downloads/flattened_im_0_rotated.jpg']

#list im_dimensions is a list of lists, each of which contains the dimensions([width, height], in qr code squares) of each qr segment;
#This is required as the qr segments are not of equivalent dimensions in qr code squares;
#qr dimensions will appear in the order: [top left, top right, bottom left, bottom right
im_dimensions = [[12, 11],[9, 10], [9, 10], [12, 11]]



#function combine_qr_segments takes in a list with paths to four qr segments, and a list with each segment's respective size([width, height] in qr blocks);
#returns a combined qr code that has been adjusted to solely black(0, 0, 0) and white (255, 255, 255) (r, g, b) values to accentuate QR code.
# The returned qr code is also designed to include buffer margins to accentuate the QR code
def combine_qr_segments(image_paths, dimensions):
    images = []
    for image_path in image_paths:
        images.append(Image.open(image_path))

    #resizing all images in image_paths to 200x200
    resized_images = []
    for img in range(0, len(images)):
        resized_images.append(images[img].resize((20*dimensions[img][0], 20*dimensions[img][1])))
                      
    #Initiating new image of size 400x400
    final_img = Image.new("RGB", ((40 + 20*(dimensions[0][0] + dimensions[1][0]) ,40 + 20*(dimensions[0][1] + dimensions[2][1]))), "white")

    #setting pixels in final_Img for top left quadrant
    for x in range(0 ,0 + 20*dimensions[0][0]):
        for y in range(0, 20*dimensions[0][1]):
            r, g, b = resized_images[0].getpixel((x, y))
            if ((r**2 + b**2 + g**2) < 80000):
                final_img.putpixel((20 + x, 20 + y), (0, 0, 0))
            else:
                final_img.putpixel((20 + x, 20 + y), (255, 255, 255))
        
    #setting pixels in final_Img for top right quadrant
    for x in range(20*dimensions[0][0], 20*dimensions[0][0] + 20*dimensions[1][0]):
        for y in range(0, 20*dimensions[1][1]):
            r, g, b = resized_images[1].getpixel((x - 20*dimensions[0][0], y))
            if ((r**2 + b**2 + g**2) < 100000):
                final_img.putpixel((20 + x, 20 + y), (0, 0, 0))
            else:
                final_img.putpixel((20 + x, 20 + y), (255, 255, 255))

    #setting pixels in final_Img for bottom left quadrant
    for x in range(0, 20*dimensions[2][0]):
        for y in range(20*dimensions[0][1], 20*dimensions[0][1] + 20*dimensions[2][1]):
            r, g, b = resized_images[2].getpixel((x, y - 20*dimensions[0][1]))
            if ((r**2 + b**2 + g**2) < 110000):
                final_img.putpixel((20 + x, 20 + y), (0, 0, 0))
            else:
                final_img.putpixel((20 + x, 20 + y), (255, 255, 255))

    #setting pixels in final_Img for bottom right quadrant
    for x in range(20*dimensions[2][0], 20*dimensions[2][0] + 20*dimensions[3][0]):
        for y in range(20*dimensions[1][1], 20*dimensions[1][1] + 20*dimensions[3][1]):
            r, g, b = resized_images[3].getpixel((x - 20*dimensions[2][0], y - 20*dimensions[1][1]))
            if ((r**2 + b**2 + g**2) < 80000):
                final_img.putpixel((20 + x, 20 + y), (0, 0, 0))
            else:
                final_img.putpixel((20 + x, 20 + y), (255, 255, 255))

    return final_img
            

final_qr = combine_qr_segments(flattened_im_paths, im_dimensions)
final_qr.show()
final_qr.save('final_qr.jpg')


























#I initially attempted to simply put the four segments together into an iamge; This led me to realize that the 4 segments overlap, are not of equivalent size, and are discolored
#Function combine_qr_segments takes in a list of paths to the 4 quarters of an image, and combines them into a single image of size 400x400
##def combine_qr_segments(image_paths):
##    images = []
##    for image_path in image_paths:
##        images.append(Image.open(image_path))
##
##    #resizing all images in image_paths to 200x200
##    resized_images = []
##    for img in images:
##        resized_images.append(img.resize((200,200)))
##                      
##    #Initiating new image of size 400x400
##    final_img = Image.new(mode="RGB", size=(400, 400))
##
##    #setting pixels in final_Img for top left quadrant
##    for x in range(0, 200):
##        for y in range(0, 200):
##            r, g, b = resized_images[0].getpixel((x, y))
##            final_img.putpixel((x, y), (r, g, b))
##    #setting pixels in final_Img for top right quadrant
##    for x in range(200, 400):
##        for y in range(0, 200):
##            r, g, b = resized_images[1].getpixel((x - 200, y))
##            final_img.putpixel((x, y), (r, g, b))
##
##    #setting pixels in final_Img for bottom left quadrant
##    for x in range(0, 200):
##        for y in range(200, 400):
##            r, g, b = resized_images[2].getpixel((x, y - 200))
##            final_img.putpixel((x, y), (r, g, b))
##
##    #setting pixels in final_Img for bottom right quadrant
##    for x in range(200, 400):
##        for y in range(200, 400):
##            r, g, b = resized_images[3].getpixel((x - 200, y - 200))
##            final_img.putpixel((x, y), (r, g, b))
##
##    return final_img






















