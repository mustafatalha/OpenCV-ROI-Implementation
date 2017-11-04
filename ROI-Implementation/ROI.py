import cv2
import math

def calculateDistance(dot1,dot2):
    return math.sqrt((dot1[0]-dot2[0])**2 + (dot1[1]-dot2[1])**2)

def saveToFile(points):
    name = input ('Enter object name: ')
    with open('roi_file.txt','a') as file:
        file.write('\"%s, (%d,%d), (%d,%d)\"\n'%(name,points[0][0],points[0][1],points[1][0],points[1][1]))

def editAction(points):
    cv2.circle(img, (points[0][0], points[0][1]), 4, (0, 255, 0), -1)
    cv2.circle(img, (points[0][0], points[0][1]), 10, (0, 255, 255), 2)
    cv2.circle(img, (points[1][0], points[1][1]), 4, (0, 255, 0), -1)
    cv2.circle(img, (points[1][0], points[1][1]), 10, (0, 255, 255), 2)
    cv2.rectangle(img,(points[0][0],points[0][1]), (points[1][0],points[1][1]),(0,0,255),2)

def manageClick(event, x, y, flags, param):
    global inEdit, img, isPaintedToMagenta, pt, roi_points, edit_points
    if inEdit:
        if (event == cv2.EVENT_LBUTTONDBLCLK):
            if not isPaintedToMagenta:
                if calculateDistance([x,y],roi_points[0]) < 10: #If 1st point is selected for edit
                    edit_points.append(roi_points[0])
                    pt = 0
                    cv2.circle(img, (roi_points[0][0], roi_points[0][1]), 4, (255, 0, 255), -1)
                    isPaintedToMagenta = True
                elif calculateDistance([x,y],roi_points[1]) < 10: # If 2nd point is selected for edit
                    edit_points.append(roi_points[1])
                    pt = 1
                    cv2.circle(img, (roi_points[1][0], roi_points[1][1]), 4, (255, 0, 255), -1)
                    isPaintedToMagenta = True
            else:
                if (pt == 0):
                    if (calculateDistance([x,y],roi_points[1])<10) or (x > roi_points[1][0]) or (y > roi_points[1][1]):
                        return
                elif (pt == 1):
                    if (calculateDistance([x,y],roi_points[0])<10) or (x < roi_points[0][0]) or (y < roi_points[0][1]):
                        return
                edit_points.append([x,y])
                img = cv2.imread("img2.jpg")
                cv2.imshow('image', img)
                roi_points[pt] = edit_points[1]
                editAction(roi_points)
                edit_points.clear()
                pt = -1
                isPaintedToMagenta = False
                cv2.setMouseCallback('image', manageClick)
    else:
        if len(roi_points) == 1:
            if (calculateDistance([x,y],roi_points[0]) < 10) or (x < roi_points[0][0]) or (y < roi_points[0][1]):
                return #Check if 2nd point is regular
        if (len(roi_points) < 2) and (event == cv2.EVENT_LBUTTONDBLCLK): #Put ROI points
            cv2.circle(img, (x, y), 4, (0, 255, 0), -1)
            cv2.circle(img, (x, y), 10, (0, 255, 255), 2)
            roi_points.append([x,y])
            if len(roi_points) == 2: #Draw rectangle
                cv2.rectangle(img,(roi_points[0][0],roi_points[0][1]),(roi_points[1][0],roi_points[1][1]),(0,0,255),2)
                inEdit = True

#Main Part

img = cv2.imread("img2.jpg")
cv2.namedWindow('image')
cv2.setMouseCallback('image', manageClick)

roi_points = [] #ROI Left-top / Right-bottom points
edit_points = []
pt = -1
inEdit = False #Check if edit in progress
isPaintedToMagenta = False
while True:
    cv2.imshow('image', img)
    if cv2.waitKey(5) & 0xFF == 27:  #Press 'ESC' to exit
        break
    elif cv2.waitKey(5) & 0xFF == 115: #Press 's' to save selection
        saveToFile(roi_points)
        img = cv2.imread("img2.jpg")
        cv2.imshow('image', img)
        roi_points.clear()
        inEdit = False
        cv2.setMouseCallback('image', manageClick)
    elif cv2.waitKey(5) & 0xFF == 99: #Press 'c' to cancel selection
        img = cv2.imread("img2.jpg")
        cv2.imshow('image', img)
        roi_points.clear()
        inEdit = False
        cv2.setMouseCallback('image', manageClick)
cv2.destroyAllWindows()

