import cv2

#required for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#change the input image here
image = cv2.imread("data/jadd.png")

#initial resizing
new_size = (0, 0)
image = cv2.resize(image, new_size, fx=0.25, fy=0.25, interpolation=cv2.INTER_LINEAR)

#convert to grayscale
img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#lets detect
faces = face_cascade.detectMultiScale(img_gray, 1.1, 4)

#variables for resizing
img_x = 0
img_y = 0
img_w = 0
img_h = 0
for (x, y, w, h) in faces:

    # cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
    img_x = x
    img_y = y
    img_w = w 
    img_h = h

# print(img_x, img_y, img_x + w, img_y + h)

#readjust ys and xs by 60 pixels to accomodate whole face + hair
#also add h and w for the extended reach of course
face_result = image[y-50:y+h+10, x-30:x+w+30]

#change pixel values here, for specific dimension, for now 300,300
new_size = (100, 100)

#output is this
face_result = cv2.resize(face_result, new_size, fx=0.25, fy=0.25, interpolation=cv2.INTER_LINEAR)

#not needed for GUI, just to check the result
cv2.imshow("result", face_result)
cv2.waitKey()