import numpy as np
import cv2



class CBIR:

 histbins=8

 def __init__(self, HistoBins=8):
        self.histbins = HistoBins
        
 def compareHist(self,queryimg,modelimg):

   hist1= cv2.calcHist([queryimg],[0,1,2],None,[self.histbins,self.histbins,self.histbins],[0, 256, 0, 256, 0, 256])
   hist1 =cv2.normalize(hist1,hist1)

   hist2  = cv2.calcHist([modelimg],[0,1,2],None,[self.histbins,self.histbins,self.histbins],[0, 256, 0, 256, 0, 256])
   hist2  = cv2.normalize(hist2,hist2)

   num = cv2.compareHist(hist1, hist2, cv2.HISTCMP_INTERSECT)
   den=sum(hist2.flatten())

   return(num/den)





imagespath='images/'


queryimg = cv2.imread(imagespath+'090_0010.jpg')
image2 = cv2.imread(imagespath+'nashar.jpg')


a=CBIR(HistoBins=8)


print(a.compareHist(queryimg,image2))





#cv.calcHist(images, channels, mask, histSize, ranges[, hist[, accumulate]])
