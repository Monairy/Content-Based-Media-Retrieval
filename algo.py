import cv2 as cv2
import numpy as np
import matplotlib.pyplot as plt

myimg = cv2.imread('HP_train.jpg')

def get_glopal_color(path):
  # return avgerage color of image
  myimg = cv2.imread(path)
  avg_color_per_row = np.average(myimg, axis=0)
  avg_color = np.average(avg_color_per_row, axis=0)
  return avg_color

def get_color_layout(path):
    # resize image to 500x500 then divide it into 50x50 grids total of 10x10 grids
    myimg = cv2.imread(path)
    grid = 50

    new_size = cv2.resize(myimg,(500,500))

    blue = np.zeros((10,10))
    green = np.zeros((10,10))
    red = np.zeros((10,10))
    res1 = new_size.shape[0] // 50
    res2 = new_size.shape[1] //50
    for i in range(res1):
        for j in range(res2):
            blue[i,j] = np.mean(new_size[(i*grid):(i*grid)+grid,(j*grid):(j*grid) + grid,0])
            green[i,j] = np.mean(new_size[(i*grid):(i*grid)+grid,(j*grid):(j*grid) + grid,1])
            red[i,j] = np.mean(new_size[(i*grid):(i*grid)+grid,(j*grid):(j*grid) + grid,2])

    return blue,green,red

def extract_key_frames(path):
  video_path = path
  p_frame_thresh = 300000 # You may need to adjust this threshold

  cap = cv2.VideoCapture(video_path)
  # Read the first frame.
  ret, prev_frame = cap.read()
  i = 0
  while ret:
    ret, curr_frame = cap.read()

    if ret:
        diff = cv2.absdiff(curr_frame, prev_frame)
        non_zero_count = np.count_nonzero(diff)
        if non_zero_count > p_frame_thresh:
            i += 1
            if( i % 50 == 0):
              cv2.imwrite('hello2/key'+ str(i) + '.png',curr_frame)
        prev_frame = curr_frame
  return i
