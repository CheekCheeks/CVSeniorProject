import cv2
import pickle
import cvzone
import numpy as np


# Video Capture
capture = cv2.VideoCapture('resources/parking_lot_1.mp4')

with open('parking_positions', 'rb') as file:
            position_list = pickle.load(file)

width, height = 25, 50

def check_parking_space(img_processed):

    space_counter = 0

    for pos in position_list:
        x, y = pos
        
        img_crop = img_processed[y:y+height, x:x+width]
        count = cv2.countNonZero(img_crop)
        
        if count < 230:
            color = (0, 255, 0)
            thickness = 5
            space_counter += 1
        else:
            color = (0, 0 , 255)
            thickness = 2
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(img, str(count), (x, y+height), scale=1, thickness=1, offset=0, colorR=color)

    
    cvzone.putTextRect(img, f'Free: {space_counter}/{len(position_list)}', (20, 30), scale=2, thickness=3, offset=10, colorR=(0,200,0))



while True:
    if capture.get(cv2.CAP_PROP_POS_FRAMES) == capture.get(cv2.CAP_PROP_FRAME_COUNT):
        capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = capture.read()
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
    img_thresh = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    
    img_median = cv2.medianBlur(img_thresh, 5)
    kernel = np.ones((3,3), np.uint8)
    img_dilate = cv2.dilate(img_median, kernel, iterations=1)

    check_parking_space(img_dilate)

    # for pos in position_list:

    cv2.imshow("image", img)
    # cv2.imshow('imgage_blur', img_blur)
    # cv2.imshow('imgage_thresh', img_median)
    cv2.waitKey(10)

