import cv2 as cv
from pyzbar.pyzbar import decode


#reading in completed qr code and displaying image
qr = cv.imread(r"C:\Users\Luka\Downloads\final_qr.jpg")
cv.imshow("QR code", qr)
cv.waitKey(0)
cv.destroyAllWindows()


#calling decode function and printing code type and information
decoded_qr = decode(qr)
for code in decoded_qr:
    print(code.type)
    print(code.data.decode('utf-8'))


#code for life video qr code reader
##cap = cv2.VideoCapture(0)
##cap.set(3, 640)
##cap.set(4, 480)
##
##camera = True
##while camera:
##    success, frame = cap.read()
##    for code in decode(frame):
##        print(code.type)
##        print(code.data.decode('utf-8'))
        




