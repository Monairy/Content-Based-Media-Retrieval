from Katna.video import Video
from Katna.writer import KeyFrameDiskWriter
import os
import moviepy.editor
from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt
from PIL import ImageTk, Image

from shutil import copyfile
import subprocess

def openFile(path):
    path2=path.replace("\\","\\\\")
    
    path3=path2.replace(" ","^ ")
    
    os.system(path3)
    
def readyExport():
    if("Exports" not in os.listdir()):
       os.mkdir("Exports")
    try:
     folders=os.listdir("Exports")
     exports=["export 0"]
     maxexport=0
     for folder in folders:
       if(folder.find("export")!=-1):
          exports.append(folder)
          num=int(folder.split()[1])
          if( num > maxexport ):
             maxexport=num
    except Exception as e:
       print(e)
       
    try:
        os.mkdir("Exports\\export "+str(maxexport+1))
        path="Exports\\export "+str(maxexport+1)        
    except Exception as e:
       print(e)
       
    return path
              
def exportFile(dstpath,srcpath):
    print(srcpath)
    
    filename=srcpath.split("/")[-1]
    copyfile(srcpath,os.path.join(dstpath,filename))
    
def exportAll(paths,mode="oneFile"):
   dstpath=readyExport()
     
   paths2=[]
   
   if(isinstance(paths,str)):
     paths2.append(paths)
   else:
     paths2=paths
     
   for srcpath in paths2:
     exportFile(dstpath,srcpath)



def extractkeyframes(videopath,num_KF,SavePath="tempKF"):

  vd = Video()

  numberOFKeyFrames = num_KF

  diskwriter = KeyFrameDiskWriter(location=SavePath)

  KeyFrames = vd._extract_keyframes_from_video(numberOFKeyFrames, videopath)
    
  diskwriter.write(videopath, KeyFrames)

 
  
def main():
    global GUI 

    GUI = Tk()
    GUI.title("Content Based Media Retrieval")
    GUI.configure(bg='#d2d2d2')
    GUI.geometry("1320x700")
    GUI.resizable(True, True)
    
    labelbanner = Label(GUI, text="Content Based Media Retrieval", font=("Arial", 28), bg='lightblue', relief="ridge", fg="White")
    labelbanner.grid(columnspan=3, padx=400, sticky='ew')
    
   # DrawMainScreen()
    
    GUI.mainloop()
    
def generateThumbnail(videoFullPath):
  directory=videoFullPath[:videoFullPath.rfind("\\")]
  thumbdir=os.path.join(directory,"thumbnails")

  thumbName=videoFullPath[videoFullPath.rfind("\\"):]+".png"
  thumbFullPath=thumbdir+thumbName
  if(os.path.exists(thumbFullPath)):
    os.remove(thumbFullPath)
  ret=subprocess.check_output(['ffmpeg', '-i', videoFullPath, '-ss', '00:00:10.000', '-vframes', '1', thumbFullPath])
  
  
def generateThumbnails(vidsPath):
  videos=os.listdir(vidsPath)
  
  for video in videos:
     if(video=="thumbnails"):
       continue
     vidfullpath=os.path.abspath(os.path.join(vidsPath,video))
     generateThumbnail(vidfullpath)
         
    
def openVideo(thumbnailPath): #openVideoFromThumbNail full path
    path2=thumbnailPath.replace("\\","\\\\")   
    path3=path2.replace(" ","^ ")
    path4=path3.replace("thumbnails\\\\","")
    path5=path4.replace(".png","")
    os.system(path5)
  
def ImgBrowser(resultimages):
          
        global imgbrowser
        global exported
        exported=0
        
        imgbrowser = Tk()
        imgbrowser.geometry("850x620")
        
        master_frame = Frame(imgbrowser, bg="Light Blue", bd=1, relief=RIDGE)
        master_frame.grid(sticky=NE)
        master_frame.columnconfigure(0, weight=1)
        
        frame2 = Frame(master_frame,width=1320,height=700)
        frame2.grid(row=3, column=0, sticky=NW)
        
        canvas = Canvas(frame2, bg="#d2d2d2")
        canvas.grid(row=0, column=0)

        vsbar = Scrollbar(frame2, orient=VERTICAL, command=canvas.yview)
        vsbar.grid(row=0, column=1, sticky=NS)
        canvas.configure(yscrollcommand=vsbar.set)

        buttons_frame = Frame(canvas,)
  
        # Add the images to the frame.
        r=1
        col=0
        images=resultimages

        images.reverse()

        lenn=len(images)
        
        LABEL_BG = "#ccc"  # Light gray.
        ROWS, COLS = int(lenn/4)+2, 8  # Size of grid.
        ROWS_DISP = 3  # Number of rows to display.
        COLS_DISP = 8  # Number of columns to display
        
        btnopen=  [[0 for x in range(COLS)] for y in range(ROWS*2)]
        btnexport=  [[0 for x in range(COLS)] for y in range(ROWS*2)]
   
        r+=1
        files=[]
        for number in range(0,lenn):
          
      
          filename =  images[number]
          files.append(filename)
          
          if((number%4)==0 and number!=0):
            r+=2
            col=0
            col2=0    
          
          image = ImageTk.PhotoImage(Image.open(filename).resize((200,200)))

             
          label = Label(buttons_frame,image=image)
          label.photo = image  
          label.grid(row=r, columnspan=2,column=col)
          
          path=os.path.abspath(filename) #full path
          
          btnopen[r][col] = Button(buttons_frame, text="Open", font=("Arial", 10), command=lambda path1=path: openVideo(path1))
          btnopen[r][col].grid(row=r+1, column=col)

          btnexport[r][col] = Button(buttons_frame, text="Export", font=("Arial", 10), command=lambda path2=filename: exportAll(path2,"oneFile"))
          btnexport[r][col].grid(row=r+1, column=col+1)
          
          col+=2
          
        canvas.create_window((0,0), window=buttons_frame, anchor=NW)

        buttons_frame.update_idletasks() 
        bbox = canvas.bbox(ALL)
        
        w, h = bbox[2]-bbox[1], bbox[3]-bbox[1]
        dw, dh = int((w/COLS) * COLS_DISP), int((h/ROWS) * ROWS_DISP)
        dw,dh=816,612
       
        canvas.configure(scrollregion=bbox, width=dw, height=dh)
        
        btnExportAll=Button(buttons_frame, text="Export All", font=("Arial", 15), command=lambda: exportAll(files))
        btnExportAll.grid(row=0,column=0)

        
        imgbrowser.mainloop()


#generateThumbnails("videos")    
      

import subprocess
import os,sys


def compareVideos(pathvid1,VidsPath):
  
  matchedThumbs=[]
  a=1
  vidsNames=os.listdir(VidsPath)
  for vidName in vidsNames:
   if(vidName!="thumbnails"):
     matchedThumbs.append(VidsPath+"\\thumbnails\\"+vidName+".png")
  
  print(matchedThumbs)
  ImgBrowser(matchedThumbs)

  
compareVideos(1,"videos")                          
filename="videos/thumbnails/"+"beach.mp4.png"
path=os.path.abspath(filename)
     
    
#openVideo(path)


#ImgBrowser(os.listdir('videos\\thumbnails'))



#path=os.path.abspath("videos\\beach.mp4")
#print(path)
#openFile(path)
#openFile("E:\_4THCSE\2nd term\multimedia\project\videos\beach.mp4")


#proc=check_output(['E:\\_4THCSE\\2nd^ term\\multimedia\\project\\videos\\beach.mp4'])
#print(proc)
#
#for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
 # print(line.rstrip())

#if __name__ == "__main__":

 # vid=  "videos/Brilliant TimeLapse of Alaskas Northern Lights  Short Film Showcase_v240P.mp4"       
 # video = moviepy.editor.VideoFileClip(vid)
 # video_duration = round(int(video.duration)/60)

 # extractkeyframes(vid,5*video_duration)


