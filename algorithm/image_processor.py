import cv2
import numpy as np
import urllib.request as url
from PIL import Image

LINE_WIDTH = 60

def read_image(image_URL): 
    return cv2.imread(image_URL)

def canny(image):
    # covert to gray, blur, then draw edges based on drastic color changes
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    canny = cv2.Canny(blur, 50,150)
    #cv2.imshow("canny",canny)
    return canny

def displayLines(image, lines):
    angles = []
    keptLines = []
    lineImage = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4) #takes two point from line
            #finds angle of each line
            if x2 - x1 == 0: #if line is perfectly verticle; avoids divide by 0 error
                if 90.0 not in angles:
                    angles.append(90)
                    cv2.line(lineImage, (x1, y1), (x2, y2), (0, 0, 255), 10)
                    keptLines.append(line)
            else:
                m = (y2 -y1) / (x2 - x1)
                angle = np.degrees(np.arctan(m))
                if angle < 0:
                    angle += 360
                if len(angles) == 0:
                    angles.append(angle)
                    cv2.line(lineImage, (x1, y1), (x2, y2), (0, 0, 255), 10)
                    keptLines.append(line)
                else:
                    #if line is unique then save it
                    unique = True
                    for eachAngle in angles:
                        if np.abs(angle - eachAngle) < 10 or (np.abs(angle - eachAngle) > 350 and np.abs(angle - eachAngle) < 365) or  (np.abs(angle - eachAngle) > 170 and np.abs(angle - eachAngle) < 190):
                            unique = False
                    if unique:
                        angles.append(angle)
                        cv2.line(lineImage,(x1,y1), (x2,y2), (0,0,255), 10)
                        keptLines.append(line)
    return lineImage, angles, keptLines

#this method only used if we need to crop the camera feed to focus on a specific area
def regionOfInterest(image):
    #save height and width of image to make polygon relative to image size
    h = image.shape[0]
    w = image.shape[1]
    polygons = np.array([[(0,h),(int(w/2), h - int(h/1.5)), (w, h - int(h/4)),(w,h)]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask,polygons,255)
    maskedImage = cv2.bitwise_and(image, mask)
    #cv2.imshow("mask", mask)
    return maskedImage

def get_image(image_url):
    url_response_image = url.urlopen(image_url)
    image_as_np_array = np.array(bytearray(url_response_image.read()), dtype=np.uint8)
    image = cv2.imdecode(image_as_np_array, -1)
    return image

def has_straight_path(state):
    return 'S' in state['J']

def has_right_path(state):
    return 'R' in state['J']

def has_left_path(state):
    return 'L' in state['J']

def has_reached_end(state):
    if state['isEnd']:
        print("End Reached!")
        return True
    return False

def process_image(image):
    canny_image = canny(image)
    h, w = canny_image.shape
    alignment = "C"
    #cropped_canny_image = regionOfInterest(canny_image)
    lines = cv2.HoughLinesP(canny_image, 2, np.pi/180, 100, np.array([]), minLineLength = 50, maxLineGap = 100) #change canny to cropped to use cropped image
    lineImage, angles, keptLines = displayLines(image, lines)
    final = cv2.addWeighted(image, 0.8, lineImage, 1, 1)
    state = {'J': '', 'A': alignment, 'isEnd': False} #J: Junction, A: alignment

    #-------detect red in image. If red seen then goal is reached---------
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0,0,240])  #adjust thresholds for preferred red detection
    upper_red = np.array([25,150,255])
    red_mask = cv2.inRange(hsv,lower_red,upper_red)
    red_color = cv2.bitwise_and(image,image,mask=red_mask)

    #cv2.imshow("redmask", red_color)
    for eachRow in red_color.tolist():  #there is probably a better way to detect this but I honestly cannot figure it out
        for eachPixel in eachRow:
            for eachColor in eachPixel:
                if eachColor != 0:
                    state['isEnd'] = True
   
    #--------------------------------------------------------------------

    #-------find key points-------------------------------------------------
    mainX = int(w/2) #mainX is horizontal position of the main path; intitialized to center of screen
    mainY = 0
    for i, eachLine in enumerate(keptLines):
        x1, y1, x2, y2 = eachLine.reshape(4)
        print(angles[i], "degrees   (",x1, ", ", y1, ") to (",x2, ", ", y2, ")")
        if (angles[i] > 80 and angles[i] < 100) or (angles[i] > 260 and angles[i] < 280):
            mainX = x1
            mainY = min(y1,y2)

    for i, eachLine in enumerate(keptLines):
        x1, y1, x2, y2 = eachLine.reshape(4)
        if not ((angles[i] > 80 and angles[i] < 100) or (angles[i] > 260 and angles[i] < 280)):
            midpoint = (x1 + x2) / 2
            print(midpoint)
            turnX = min(abs(x1 - mainX), abs(x2 - mainX))
            if turnX == x1:
                turnY = y1
            else:
                turnY = y2
     #--------------------------------------------------------------------


     #------find alignment of track for adjustments----------------------------
    section = int(w/5)
    if mainX < section:
        state['A'] = "FL"        #Far Left
    elif mainX < section * 2:
        state['A']  = "L"         #Slight Left
    elif mainX < section * 3:
        state['A']  = "C"         #Centered
    elif mainX < section * 4:
        state['A']  = "R"         #Slight Right
    else:
        state['A']  = "FR"        #Far Right

     #--------------------------------------------------------------------


     #-------define type of junction-----------------------------------------
    if len(keptLines) == 0:
        state['J'] = 'B'
    elif len(keptLines) == 1:
        #print("Straight")
        state['J'] = 'S'
    else:
                
        if midpoint < mainX - LINE_WIDTH and mainY < turnY - 10:
            #print("Straight or Left Turn")
            state['J'] = 'SL'
        elif midpoint < mainX - LINE_WIDTH:
            #print("Left Turn")
            state['J'] = 'L'
        elif midpoint > mainX + LINE_WIDTH and mainY < turnY - 10:
            #print("Straight or Right Turn")
            state['J'] = 'SR'
        elif midpoint > mainX + LINE_WIDTH:
            #print("Right Turn")
            state['J'] = 'R'
        elif mainY < turnY - LINE_WIDTH:
            #print("Left, Right, or Straight")
            state['J'] = 'LRS'
        else:
            #print("Left or Right Turn")
            state['J'] = 'LR'
     #--------------------------------------------------------------------

        #cv2.imshow("result", final)
        #cv2.waitKey(0)

    return state, final # Returning the state and the final image so we can display in a loop
