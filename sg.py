import PySimpleGUI as sg
import io, os
from PIL import Image
import cv2
import pytesseract as tes

#for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#functions for OCR
def performOCR(img=None, grayscale=False):
	"""
		Description:
			performORC() is the function that performs the OCR on the given image

		Args:
				img (cv2.imread(), optional): image to perform OCR on. Defaults to None.
				grayscale (bool, optional): whether to pre-process the image to grayscale or not. Defaults to False.

		Returns:
				list: a list of tuples containing information of all found texts in the image

	"""

	# return if there is no image
	if img is None:
		return
	
	# convert image if grayscale is enabled
	if grayscale is True:
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	# tesseract config 
	# --oem (tesseract scanning engine)
	# --psm (image segmentation method)
	# -c tessedit_char_blacklist= (characters not to scan)
	tes_config = r'--oem 3 --psm 12 -c tessedit_char_blacklist=!\"#$%&\'()*+,-./0123456789:;<=>?@[\\]^_`{|}~ '
	raw_result = tes.image_to_data(img, config=tes_config, output_type=tes.Output.DICT)

	# value to be returned
	result = list()

	# evaluate 
	for i in range(0, len(raw_result["text"])):
		
		text = raw_result["text"][i] # get text
		conf = int(raw_result["conf"][i]) # get confidence

		# assume confidence threshold to 60
		if conf > 60:
			# if confidence level > 60
			# safe to say that it is a positive result 
			to_add = (text, conf)
			result.append(to_add)
			
	return result


def compareResult(coloredScan=None, grayScan=None):
	"""
	compareResult() is the function that compares the result of the colored scan from the grayscale scan

	Args:
			coloredScan (dict, optional): dictionary result from the colored scan of the image. Defaults to None.
			grayScan (dict, optional): dictionary result from the grayscaled scan of the image. Defaults to None.

	Returns:
			string: the concatenated string from the result with higher confidence level
	"""

	# total confidence level, to see which result is more accurate
	coloredTotal = 0
	grayTotal = 0
	coloredString = ""
	grayString = ""

	if coloredScan is not None:
		for text,conf in coloredScan:
			coloredTotal += int(conf)
			coloredString = " ".join([coloredString, text])

	if grayScan is not None:
		for text,conf in grayScan:
			grayTotal += int(conf)
			grayString = " ".join([grayString, text])

	return coloredString if coloredTotal>=grayTotal else grayString
	


	# return None


def sampleUsage(img):
	"""this is a sample usage of the two function above

	Args:
			img (cv2.imread()): image result of the cv2.imread()
	"""

	if img is None:
		return

    # run both colored and grayscaled to check
    # if which image will return more accurate result
	colored = performOCR(img, grayscale=False)
	grayscaled = performOCR(img, grayscale=True)
	return compareResult(colored, grayscaled)

	# print("colored: {}".format(colored))
	# print("grayscaled: {}".format(grayscaled))
	# print("Result: {}".format(string_result))



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

    return bg


#For files
file_type = [    
    ("All files (*.*)", "*.*"),
    #Fix png
    ("PNG (*.png)", "*.png)"),
    ("JPEG (*.jpg)", "*.jpg)")


]

column_output = [
    
    [sg.Text("Converted Image Here", key="-OUTPUTTEXT-")],
    [sg.Image(key="-OUTPUTIMAGE-")],
    [sg.Button("Save Image")]
    
]


column_input = [
    [sg.Text("No Image Converted Yet", key="-INPUTTEXT-")],
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

counter = 0
while True:
    event,values = window.read()
    
    counter += 1
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

            face_result = cv2.cvtColor(face_result, cv2.COLOR_BGR2RGB)


            #-------------------------#
            #     OCR RIGHT HERE      #
            #-------------------------#

            img = cv2.imread(values["-FILE-"])
            ocr_result = sampleUsage(img)


            #-------------------------#
            #       ID CREATION       #
            #-------------------------#
            id_temp = cv2.imread('data/id.png')
            id_temp = cv2.cvtColor(id_temp, cv2.COLOR_BGR2RGB)

            face_result = cv2.resize(face_result, (300,300))
            id_result = generateID(face_result, id_temp, ocr_result)

            pil_image = Image.fromarray(id_result)
            pil_image.thumbnail((400,400))

            # Saves the image to DISPLAY on leftside
            bio2 = io.BytesIO()
            pil_image.save(bio2, format="PNG")

            window["-OUTPUTIMAGE-"].update(data=bio2.getvalue())
            window["-OUTPUTTEXT-"].update("")
            window["-INPUTTEXT-"].update("")
            
            #WHAT TO DO HERE!!!
            #The goal is to send put face_result into the ID
            #Next is to put the OCR text in the ID
            #PUT the resulting ID in -OUTPUTIMAGE-
            #PUT a save button
    elif event == "Save Image":
        try:
            filename = str(ocr_result) + "_id.png"
            output = cv2.cvtColor(id_temp, cv2.COLOR_BGR2RGB)
            cv2.imwrite(filename, output)
        except:
            continue

window.close()


