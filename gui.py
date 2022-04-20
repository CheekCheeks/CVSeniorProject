from copy import deepcopy
from tkinter import *
from tkinter import filedialog
import cv2
import pickle
import cvzone
import numpy as np


homeWindow = Tk()
homeWindow.title("Parking Spot Locator")
click_count = 0

def openFileDirectory():
    global directory
    homeWindow.directory = filedialog.askdirectory(title="Select a directory")
    directoryLabel = Label(homeWindow, text=homeWindow.directory, fg="black").grid(row=1, column=2)

# Opens the file dialogue and allows user to select what parking lot file they want to view
def chooseViewFile():
    global viewFilePath
    homeWindow.viewFile = filedialog.askopenfilename(title="Select the viewing file", initialdir=homeWindow.directory, filetypes=(('Image files', '*.img'), ('mp4 files', '*.mp4')))
    viewFilePath = str(homeWindow.viewFile)
    viewFileLabel = Label(homeWindow, text=homeWindow.viewFile, fg="black").grid(row=2, column=2)

# Passes the viewFile to main.py
def getViewFile():
    return viewFilePath

# Opens the file dialogue for choosing a configure file.
def chooseConfigureFile():
    global configureFilePath
    homeWindow.configureFile = filedialog.askopenfilename(title="Select the configuration file", initialdir=homeWindow.directory)
    configureFilePath = str(homeWindow.configureFile)
    configureFileLabel = Label(homeWindow, text=homeWindow.configureFile, fg="black").grid(row=3, column=2)

def getConfigureFile():
    return configureFilePath

# Opens the file dialogue for choosing the parking positions' file.
def chooseParkingPositions():
    global parkingPositionsFilePath
    homeWindow.parkingPositions = filedialog.askopenfilename(title="Select the parking positions", initialdir=homeWindow.directory)
    parkingPositionsFilePath = str(homeWindow.parkingPositions)
    parkingPositionsLabel = Label(homeWindow, text=homeWindow.parkingPositions, fg="black").grid(row=4, column=2)

def getParkingPositions():
    return parkingPositionsFilePath

# Opens the parking spot configure window.
def openConfigureWindow():
    configureWindow = Toplevel()
    configureWindow.title("Configuration Window")
    closeButton = Button(configureWindow, text="Close", fg="black", command=configureWindow.destroy).pack()

# Opens the window that lets you view the available parking spots.
def openViewWindow():
    viewWindow = Toplevel()
    viewWindow.title("View Window")
    closeButton = Button(viewWindow, text="Close", fg="black", command=viewWindow.destroy).pack()

# View lot is what I want to put openViewWindow until
# but if I'm able to figure out how to close the cv2.window
# we could go that route too.
def viewLot():

    capture = cv2.VideoCapture(getViewFile())

    with open(getParkingPositions(), 'rb') as file:
        position_list = pickle.load(file)

    width, height = 45, 20

    position_list_copy = np.array(position_list, dtype=None, copy=True, order='K', subok=False, ndmin=0)

    def check_parking_space(img_processed):

        container = cv2.imread(getConfigureFile())
        space_counter = 0

        for pos in position_list_copy:
            polygon = [[pos[0], pos[1], pos[2], pos[3]]]
            minX = container.shape[1]
            maxX = -1
            minY = container.shape[0]
            maxY = -1

            for point in polygon[0]:
                x = point[0]
                y = point[1]

                if x < minX:
                    minX = x
                if x > maxX:
                    maxX = x
                if y < minY:
                    minY = y
                if y > maxY:
                    maxY = y

            cropedImage = np.zeros_like(container)
            for y in range(0, container.shape[0]):
                for x in range(0, container.shape[1]):

                    if x < minX or x > maxX or y < minY or y > maxY:
                        continue

                    if cv2.pointPolygonTest(np.asarray(polygon), (x, y), False) >= 0:
                        cropedImage[y, x, 0] = container[y, x, 0]
                        cropedImage[y, x, 1] = container[y, x, 1]
                        cropedImage[y, x, 2] = container[y, x, 2]


            img_crop = img_processed[minY:maxY, minX:maxX]
            count = cv2.countNonZero(img_crop)

            if count < 230:
                color = (0, 255, 0)
                thickness = 5
                space_counter += 1
            else:
                color = (0, 0, 255)
                thickness = 2

            #cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
            #cvzone.putTextRect(img, str(count), (x, y + height), scale=1, thickness=1, offset=0, colorR=color)
            cv2.line(img, pos[0], pos[1], color, thickness)
            cv2.line(img, pos[1], pos[2], color, thickness)
            cv2.line(img, pos[2], pos[3], color, thickness)
            cv2.line(img, pos[3], pos[0], color, thickness)
        cvzone.putTextRect(img, f'Free: {space_counter}/{len(position_list)}', (20, 30), scale=2, thickness=3,
                           offset=10, colorR=(0, 200, 0))

    while True:
        if capture.get(cv2.CAP_PROP_POS_FRAMES) == capture.get(cv2.CAP_PROP_FRAME_COUNT):
            capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
        success, img = capture.read()
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
        img_thresh = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)

        img_median = cv2.medianBlur(img_thresh, 5)
        kernel = np.ones((3, 3), np.uint8)
        img_dilate = cv2.dilate(img_median, kernel, iterations=1)

        check_parking_space(img_dilate)

        # for pos in position_list:

        cv2.imshow("image", img)
        # cv2.imshow('imgage_blur', img_blur)
        # cv2.imshow('imgage_thresh', img_median)
        key = cv2.waitKey(10)
        quitKey = ord("q")
        if key == quitKey:
            cv2.destroyWindow("image")
            break


def configureLot():
    width, height = 45, 20
    coords = []

    try:
        with open(getParkingPositions(), 'rb') as file:
            position_list = pickle.load(file)
    except:
        position_list = []

    def position_click(events, x, y, flags, params):
        global click_count
        if events == cv2.EVENT_LBUTTONDOWN:
            coords.append((x, y))
            click_count += 1

            if click_count >= 4:
                position_list.append(deepcopy(coords))
                coords.clear()
                click_count = 0


        if events == cv2.EVENT_RBUTTONDOWN:
            position_list.pop()

        with open(getParkingPositions(), 'wb') as file:
            pickle.dump(position_list, file)


    while True:
        global click_count
        # cv2.rectangle(img,(20,65),(65,90),(255,0,255),2)
        img = cv2.imread(getConfigureFile())
        quitKey = ord("q")
        key = cv2.waitKey(1)
        #print(click_count)

        for pos in position_list:
            cv2.line(img, pos[0], pos[1], 2)
            cv2.line(img, pos[1], pos[2], 2)
            cv2.line(img, pos[2], pos[3], 2)
            cv2.line(img, pos[3], pos[0], 2)

        cv2.imshow("image", img)
        cv2.setMouseCallback("image", position_click)

        if key == quitKey:
            cv2.destroyWindow("image")
            break




# Creating the buttons, and assigning them the their correlated functions that were created up above.
configureButton = Button(homeWindow, text="Configure", fg="black", command=configureLot)
viewButton = Button(homeWindow, text="View", fg="black", command=viewLot)
chooseDirectoryButton = Button(homeWindow, text="Choose Directory", fg="black", command=openFileDirectory)
chooseViewFileButton = Button(homeWindow, text="Choose view file", fg="black", command=chooseViewFile)
chooseConfigureFileButton = Button(homeWindow, text="Choose configure file", fg="black", command=chooseConfigureFile)
chooseParkingPositionsButton = Button(homeWindow, text="Choose parking position file", fg="black", command=chooseParkingPositions)

# Packing the buttons onto the window with their respective column and row.
viewButton.grid(row=6, column=1)
configureButton.grid(row=5, column=1)
chooseDirectoryButton.grid(row=1, column=1)
chooseViewFileButton.grid(row=2, column=1)
chooseConfigureFileButton.grid(row=3, column=1)
chooseParkingPositionsButton.grid(row=4, column=1)

mainloop()