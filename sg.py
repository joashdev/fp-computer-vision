import PySimpleGUI as sg
import io, os
from PIL import Image
import cv2

#for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#For files
file_type = [    
    ("All files (*.*)", "*.*"),
    #Fix png
    ("PNG (*.png)", "*.png)"),
    ("JPEG (*.jpg)", "*.jpg)")


]

column_output = [
    
    [sg.Text("Resulting Image")],
    [sg.Image(key="-OUTPUTIMAGE-")]
    
]


column_input = [
    [sg.Image(key="-IMAGE-")],
    [
        sg.Text("Image File"),
        sg.Input(size=(35,1), key="-FILE-"),
        sg.FileBrowse(file_types=file_type),
        sg.Button("Convert Image"),
        # sg.Button("Convert to ID")
    ]
]

#layout here

layout = [
    [
        sg.Column(column_input),
        sg.VSeperator(),
        sg.Column(column_output)
    ]
]


window = sg.Window("ID Converter", layout)

while True:
    event,values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    elif event == "Convert Image":
        filename = values["-FILE-"]
        if os.path.exists(filename):
            image = Image.open(values["-FILE-"])
            image.thumbnail((400,400))

            # Saves the image to DISPLAY on leftside
            bio = io.BytesIO()
            image.save(bio, format="PNG")

            window["-IMAGE-"].update(data=bio.getvalue())

            #-------------------------#
            #   FACE DETECTION HERE   #
            #-------------------------#

            #convert to grayscale
            img = cv2.imread(values["-FILE-"])

            #Initial Resize
            new_size = (0, 0)
            img = cv2.resize(img, new_size, fx=0.25, fy=0.25, interpolation=cv2.INTER_LINEAR)
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

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
            face_result = img[y-50:y+h+10, x-30:x+w+30]

            #change pixel values here, for specific dimension, for now 300,300
            new_size = (100, 100)

            #output is this for face detection
            face_result = cv2.resize(face_result, new_size, fx=0.25, fy=0.25, interpolation=cv2.INTER_LINEAR)

            # window["-OUTPUTIMAGE-"].update(data=face_result)

            #WHAT TO DO HERE!!!
            #The goal is to send put face_result into the ID
            #Next is to put the OCR text in the ID
            #PUT the resulting ID in -OUTPUTIMAGE-
            #PUT a save button



        #Add else statement for improper file
    # elif event == "Convert to ID":
    #     filename = values["-FILE-"]
    #     img = cv2.imread(values["-FILE-"])
    #     cv2.imshow("something", img)
    #     cv2.waitKey(0)
    #     continue
window.close()


