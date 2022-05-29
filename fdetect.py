import cv2

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
image = cv2.imread("img/img6.png")

new_size = (0, 0)
image = cv2.resize(image, new_size, fx=0.25, fy=0.25, interpolation=cv2.INTER_LINEAR)


img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(img_gray, 1.1, 4)
img_x = 0
img_y = 0
img_w = 0
img_h = 0
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)


cv2.imshow("result", image)
cv2.waitKey()