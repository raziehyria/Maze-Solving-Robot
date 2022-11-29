import cv2
import numpy as np
import urllib.request as url

LINE_WIDTH = 30

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
            if x2 - x1 == 0:
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
                        if np.abs(angle - eachAngle) < 10:
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

def has_straight_path(image):
    h, w = image.shape
    #for x in range(int(w / 2))
    pass

def has_right_path(image):
    h, w = image.shape
    for row in range(int(h / 2) - 30, int(h / 2) + 30):
        result = np.all(image[row][int(w / 2): w - 1] != 255)
        if result: 
            return True
    return False
    #return midpoint > mainX + LINE_WIDTH

def has_left_path(image):
    h, w = image.shape
    for row in range(int(h / 2) - 30, int(h / 2) + 30):
        result = np.all(image[row][0: int(w / 2)] != 255)
        if result: 
            return True
    return False
    #return midpoint < mainX - LINE_WIDTH

def has_reached_end():
    pass

def test(image):
    gray = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    thresh, im_bw = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    h, w = im_bw.shape
    #0line = cv2.line(im_bw, (int(w / 2) + 30, 0), (int(w / 2) + 30, h - 1), (0, 0, 255), 2)
    #line = cv2.line(im_bw, (int(w / 2) - 30, 0), (int(w / 2) - 30, h - 1), (0, 0, 255), 2)
    #line = cv2.line(im_bw, (0, int(h / 2) + 30), (w - 1,int(h / 2) + 30), (0, 0, 255), 2)
    #line = cv2.line(im_bw, (0 , int(h / 2) - 30), (w - 1, int(h / 2) - 30), (0, 0, 255), 2)
    #cv2.imshow("result", line)
    #cv2.waitKey(0)
    return im_bw

def process_image(image):
    canny_image = canny(image)
    #cropped_canny_image = regionOfInterest(canny_image)
    lines = cv2.HoughLinesP(canny_image, 2, np.pi/180, 100, np.array([]), minLineLength = 50, maxLineGap = 100) #change canny to cropped to use cropped image
    lineImage, angles, keptLines = displayLines(image, lines)
    final = cv2.addWeighted(image, 0.8, lineImage, 1, 1)
    action = ''
    if len(keptLines) == 1:
        #print("Straight")
        action = 'S'
    else:
        for i, eachLine in enumerate(keptLines):
            x1, y1, x2, y2 = eachLine.reshape(4)
            if (angles[i] > 87 and angles[i] < 93) or (angles[i] > 267 and angles[i] < 273):
                mainX = x1
                mainY = min(y1,y2)
                #print("mainX: ", mainX)
                #print("mainY: ", mainY)
            else:
                midpoint = (x1 + x2) / 2
                #print("midpoint: ", midpoint)
                #print("Y: ", y1)
                #print(angles)
                #print("mainX: ", mainX)
                #print("mainY: ", mainY)
                if midpoint < mainX - LINE_WIDTH:
                    #print("Left Turn")
                    action = 'L'
                elif midpoint > mainX + LINE_WIDTH:
                    #print("Right Turn")
                    action = 'R'
                elif mainY < y1 - LINE_WIDTH:
                    #print("Left, Right, or Straight")
                    action = 'R'
                else:
                    #print("Left or Right Turn")
                    action = 'R'
    cv2.imshow("result", final)
    cv2.waitKey(0)
    #return midpoint, mainX, mainY,
    return action


#image = get_image()
#image = cv2.imread('leftOrRightReal.png') #for testing without camera stream
#angles = []
#keptLines = []
#laneImage = np.copy(image)
#cannyImage = canny()
#result = process_image(cannyImage)
#print(result)
#print(has_right_path())

