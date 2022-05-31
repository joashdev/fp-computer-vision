
# img = cv2.imread("data/yani1.jpg")

# gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# # gray_img = cv2.threshold(gray_img, 0, 255,
# # 		cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
# custom_config = r'--oem 3 --psm 12 -c tessedit_char_blacklist=!\"#$%&\'()*+,-./0123456789:;<=>?@[\\]^_`{|}~ '
# results = tes.image_to_data(gray_img, config=custom_config, output_type=tes.Output.DICT)

# # h, w, c = img.shape
# # boxes = tes.image_to_boxes(gray_img) 
# # for b in boxes.splitlines():
# #     b = b.split(' ')
# #     gray_img = cv2.rectangle(gray_img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
# # display = cv2.resize(gray_img, (0, 0), fx = 0.3, fy = 0.3)
# # cv2.imshow("input image", display)
# print("result: {}".format(results))
# for i in range(0, len(results["text"])):
# 	# extract the bounding box coordinates of the text region from
# 	# the current result
# 	x = results["left"][i]
# 	y = results["top"][i]
# 	w = results["width"][i]
# 	h = results["height"][i]
# 	# extract the OCR text itself along with the confidence of the
# 	# text localization
# 	text = results["text"][i]
# 	conf = int(results["conf"][i])

# 	if conf > 50:
# 		# display the confidence and text to our terminal
# 		print("Confidence: {}".format(conf))
# 		print("Text: {}".format(text))
# 		print("")
# 		# strip out non-ASCII text so we can draw the text on the image
# 		# using OpenCV, then draw a bounding box around the text along
# 		# with the text itself
# 		text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
# 		cv2.rectangle(gray_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
# 		cv2.putText(gray_img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
# 			1.2, (0, 0, 255), 3)
# 		cv2.putText(gray_img, "Confidence: {}%".format(conf), (x, y - 50), cv2.FONT_HERSHEY_SIMPLEX,
# 			1.2, (0, 0, 255), 3)


# print(text)
