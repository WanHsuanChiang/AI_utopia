import sys
import requests
import random
import cv2
import urllib
import numpy as np

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
	cv2.imwrite(local_path, img)
	if cv2.waitKey() & 0xff == 27: quit()
	return local_path
