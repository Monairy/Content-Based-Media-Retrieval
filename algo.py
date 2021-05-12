import cv2 as cv2
import numpy as np
import matplotlib.pyplot as plt

myimg = cv2.imread('HP_train.jpg')

#average glopal 
avg_color_per_row = np.average(myimg, axis=0)
avg_color = np.average(avg_color_per_row, axis=0)




# average local for 
grid = 50

v = cv2.resize(myimg,(500,500))

lo = np.zeros((10,10))
res1 = v.shape[0] // 50
res2 = v.shape[1] //50
for i in range(res1):
  for j in range(res2):
    lo[i,j] = np.mean(myimg[(i*50):(i*50)+grid,(j*50):(j*50) + grid,1])

lo



#key frames

video_path = "dog.mp4"
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
            #print("Got P-Frame")
            i += 1
            if( i % 50 == 0):
              cv2.imwrite('hello2/key'+ str(i) + '.png',curr_frame)
        prev_frame = curr_frame
print(i)
