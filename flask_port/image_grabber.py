import sys
import requests
import random
import cv2
import urllib
import numpy as np

#== Parameters =======================================================================
BLUR = 21
CANNY_THRESH_1 = 10
CANNY_THRESH_2 = 200
MASK_DILATE_ITER = 10
MASK_ERODE_ITER = 10
#(0.0,0.0,0.0) # In BGR format


def rem_bg(image, mask_color):
	#== Processing =======================================================================
	MASK_COLOR = mask_color
	#-- Read image -----------------------------------------------------------------------
	img = image#cv2.imread('data/cat.jpg')
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

	#-- Edge detection -------------------------------------------------------------------
	edges = cv2.Canny(gray, CANNY_THRESH_1, CANNY_THRESH_2)
	edges = cv2.dilate(edges, None)
	edges = cv2.erode(edges, None)

	#-- Find contours in edges, sort by area ---------------------------------------------
	contour_info = []
	contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
	# Previously, for a previous version of cv2, this line was:
	#  contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
	# Thanks to notes from commenters, I've updated the code but left this note
	for c in contours:
	    contour_info.append((
	        c,
	        cv2.isContourConvex(c),
	        cv2.contourArea(c),
	    ))
	contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
	max_contour = contour_info[0]

	#-- Create empty mask, draw filled polygon on it corresponding to largest contour ----
	# Mask is black, polygon is white
	mask = np.zeros(edges.shape)
	cv2.fillConvexPoly(mask, max_contour[0], (255))

	#-- Smooth mask, then blur it --------------------------------------------------------
	mask = cv2.dilate(mask, None, iterations=MASK_DILATE_ITER)
	mask = cv2.erode(mask, None, iterations=MASK_ERODE_ITER)
	mask = cv2.GaussianBlur(mask, (BLUR, BLUR), 0)
	mask_stack = np.dstack([mask]*3)    # Create 3-channel alpha mask

	#-- Blend masked img into MASK_COLOR background --------------------------------------
	mask_stack  = mask_stack.astype('float32') / 255.0          # Use float matrices,
	img         = img.astype('float32') / 255.0                 #  for easy blending

	masked = (mask_stack * img) + ((1-mask_stack) * MASK_COLOR) # Blend
	masked = (masked * 255).astype('uint8')                     # Convert back to 8-bit
	return masked

def im_grab(query, DISP):
	r = requests.get("https://api.qwant.com/api/search/images",
	    params={
	        'count': 50,
	        'q': query,
	        't': 'images',
	        'safesearch': 1,
	        'locale': 'en_US',
	        'uiv': 4
	    },
	    headers={
	        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
	    }
	)
	response = r.json().get('data').get('result').get('items')
	urls = [r.get('media') for r in response]

	req = urllib.request.urlopen(urls[3])#random.choice(urls))
	arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
	img = cv2.imdecode(arr, -1) # 'Load it as it is'
	#img.save('my.png')
	if DISP:
		cv2.imshow('Your wonder', img)
	local_path = 'data/{}.jpg'.format(query)
	img_bg = rem_bg(img, (1,1,1))
	cv2.imwrite(local_path, img_bg)
	if cv2.waitKey() & 0xff == 27: quit()
	return local_path
