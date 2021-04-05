import art_grabber
import def_grabber
import image_grabber
import cv2

import png
import numpy as np

from PIL import Image
import os
import time

cwd = os.getcwd()

CHAR_DELAY = 50     # milliseconds between characters

def merge_image(back, front, x,y):
    # convert to rgba
    if back.shape[2] == 3:
        back = cv2.cvtColor(back, cv2.COLOR_BGR2BGRA)
    if front.shape[2] == 3:
        front = cv2.cvtColor(front, cv2.COLOR_BGR2BGRA)

    # crop the overlay from both images
    bh,bw = back.shape[:2]
    fh,fw = front.shape[:2]
    x1, x2 = max(x, 0), min(x+fw, bw)
    y1, y2 = max(y, 0), min(y+fh, bh)
    front_cropped = front[y1-y:y2-y, x1-x:x2-x]
    back_cropped = back[y1:y2, x1:x2]

    alpha_front = front_cropped[:,:,3:4] / 255
    alpha_back = back_cropped[:,:,3:4] / 255

    # replace an area in result with overlay
    result = back.copy()
    print(f'af: {alpha_front.shape}\nab: {alpha_back.shape}\nfront_cropped: {front_cropped.shape}\nback_cropped: {back_cropped.shape}')
    result[y1:y2, x1:x2, :3] = alpha_front * front_cropped[:,:,:3] + (1-alpha_front) * back_cropped[:,:,:3]
    result[y1:y2, x1:x2, 3:4] = (alpha_front + alpha_back) / (1 + alpha_front*alpha_back) * 255

    return result

def art(term):
    #term = input("What's on your mind?")
    defWiki = def_grabber.find_wiki_def(term)
    #print("What is understood is, ", defWiki)
    #print("Wait a few minutes...")

    art = art_grabber.art_grab(term, incomp=1)
    art = np.multiply(art,255)
    art_path = r"server_im/{}_art.png".format(term)
    im = cv2.imencode(".png", art)[1].tobytes()

    cv2.imwrite(art_path, art)
    s_img = cv2.imread(art_path, -1)

    s_img = image_grabber.rem_bg(s_img, (1,1,1))
    cv2.imwrite(art_path, s_img)

    s_img = Image.open(art_path)
    s_img = s_img.convert('RGBA')
    # Transparency
    newImage = []
    for item in s_img.getdata():
        if item[:3] == (255, 255, 255):
            newImage.append((255, 255, 255, 0))
        else:
            newImage.append(item)
    s_img.putdata(newImage)
    s_img.save(art_path)
    #print("done...")
    return
