import cv2


def generateID(face, bg, text="Name Surname"):
  bg_width = 600
  bg_height = 900
  fg_height = 300
  fg_width = 300

  textBottomY = 635
  alpha = 1

  # coordinates of id picture
  start_y = 225
  start_x = 150
  end_y = 525
  end_x = 450

  font = cv2.FONT_HERSHEY_DUPLEX
  text = text.upper()

  face_portion = cv2.addWeighted(face, 
                alpha, 
                bg[start_y:end_y, start_x:end_x,:], 
                1-alpha, 
                0, bg)

  bg[start_y:end_y, start_x:end_x,:] = face_portion

  # center the text in bg image
  textsize = cv2.getTextSize(text, font, 1.5, 2)[0]
  textX = int((600 -  textsize[0])/2)
  # put the text
  cv2.putText(bg, text, (textX, textBottomY), font, 1.5, (85, 85, 1), 2)


  # return ID of size 600x900
  return bg

if __name__ == '__main__':

  # get images
  img1 = cv2.imread('data/yani1.jpg')
  id = cv2.imread('data/id.png')

  # resize img1 to simulate id size
  img1 = cv2.resize(img1, (300,300))

  # generate id
  id_result = generateID(img1, id, text="levin seraski")

  id_result = cv2.resize(id_result, (300, 450))
  cv2.imshow('composited image', id_result)

  cv2.waitKey(0)
  cv2.destroyAllWindows()