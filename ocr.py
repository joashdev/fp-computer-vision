import cv2
import pytesseract as tes


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
	string_result = compareResult(colored, grayscaled)

	print("colored: {}".format(colored))
	print("grayscaled: {}".format(grayscaled))
	print("Result: {}".format(string_result))


if __name__ == "__main__":

	img = cv2.imread('data/reygel.jpg')
	sampleUsage(img)