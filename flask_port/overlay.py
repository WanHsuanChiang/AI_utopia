import cv2
#cv2.imwrite(art_path, art)
s_img = cv2.imread("data_art/cat_art.png")
l_img = cv2.imread("data/chin.jpg")
#percent by which the image is resized
scale_percent = 50
#calculate the 50 percent of original dimensions
width = int(s_img.shape[1] * scale_percent / 100)
height = int(s_img.shape[0] * scale_percent / 100)
# dsize
dsize = (width, height)
# resize image
s_img2 = cv2.resize(s_img, dsize)
x_offset=y_offset=50
l_img[y_offset:y_offset+s_img2.shape[0], x_offset:x_offset+s_img2.shape[1]] = s_img2
cv2.imshow('fig', l_img)
cv2.waitKey()
