import cv2
import numpy as np
import urllib.request as url

def canny():
    # covert to gray, blur, then draw edges based on drastic color changes
    gray = cv2.cvtColor(laneImage, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    canny = cv2.Canny(blur, 50,150)
    #cv2.imshow("canny",canny)
    return canny

def displayLines(image, lines):
    lineImage = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2 = line.reshape(4) #takes two point from line
            #finds angle of each line
            if x2 -x1 == 0:
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

    return lineImage

#this method only used if we need to crop the camera feed to focus on a specific area
def regionOfInterest(image):
    #save height and width of image to make polygon relative to image size
    h = image.shape[0]
    w = image.shape[1]
    polygons = np.array([[(0,h),(int(w/2), h - int(h/1.5)), (w, h - int(h/4)),(w,h)]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask,polygons,255)
    maskedImage = cv2.bitwise_and(canny,mask)
    #cv2.imshow("mask", mask)
    return maskedImage

def get_image(image_url):
    url_response_image = url.urlopen(image_url)
    image_as_np_array = np.array(bytearray(url_response_image.read()), dtype=np.uint8)
    image = cv2.imdecode(image_as_np_array, -1)
    return image

def has_straight_path():
    return "Straight" in result

def has_right_path():
    return "Right" in result

def has_left_path():
    return "Left" in result

def has_reached_end():
    #TODO
    pass

def process_image(image):
    #cropped = regionOfInterest(image)
    lines = cv2.HoughLinesP(image, 2, np.pi/180, 100, np.array([]), minLineLength = 50,maxLineGap = 100) #change canny to cropped to use cropped image
    lineImage = displayLines(laneImage, lines)
    final = cv2.addWeighted(laneImage, 0.8, lineImage, 1, 1)
    LINE_WIDTH = 30
    if len(keptLines) == 1:
        return("Straight")
    else:
        for i, eachLine in enumerate(keptLines):
            x1, y1, x2, y2 = eachLine.reshape(4)
            if angles[i] == 90:
                mainX = x1
                mainY = min(y1,y2)
                print("mainX: ", mainX)
                print("mainY: ", mainY)
            else:
                midpoint = (x1 + x2) / 2
                print("midpoint: ", midpoint)
                print("Y: ", y1)
                if midpoint < mainX - LINE_WIDTH:
                    return("Left Turn")
                elif midpoint > mainX + LINE_WIDTH:
                    return("Right Turn")
                elif mainY < y1 -LINE_WIDTH:
                    return("Left, Right, or Straight")
                else:
                    return("Left or Right Turn")

    print(angles)
    cv2.imshow("result", final)
    cv2.waitKey(0)


#image = get_image()
image = cv2.imread('right.png') #for testing without camera stream
angles = []
keptLines = []
laneImage = np.copy(image)
cannyImage = canny()
result = process_image(cannyImage)
print(has_right_path())

