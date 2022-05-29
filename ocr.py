import cv2
import pytesseract as tes

img = cv2.imread("data/jai.jpg")

gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
custom_config = r'--oem 3 --psm 6'
text = tes.image_to_string(gray_img, config=custom_config)

h, w, c = img.shape
boxes = tes.image_to_boxes(gray_img) 
for b in boxes.splitlines():
    b = b.split(' ')
    gray_img = cv2.rectangle(gray_img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
display = cv2.resize(img, (0, 0), fx = 0.3, fy = 0.3)
# cv2.imshow("input image", display)


print(text)

cv2.waitKey(0)
cv2.destroyAllWindows()


if __name__ == "__main__":
  pass