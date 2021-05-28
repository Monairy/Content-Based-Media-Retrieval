from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt
from PIL import ImageTk, Image
from tkinter import filedialog
import os
import shutil
import cv2 as cv2
import numpy as np
import pickle


class ImgFeaturesDatabase:

  HistoFeaturesDB='HistogramFeatures.db'
  GlobalColorFeaturesDB='GlobalColorFeatures.db'
  ColorLayoutFeaturesDB='ColorLayoutFeatures.db'
  
  def __init__(self, HistoPath='HistogramFeatures.db', GlobalColorPath='GlobalColorFeatures.db',ColorLayoutPath='ColorLayoutFeatures.db'):
        self.HistoFeaturesDB = HistoPath  
        self.GlobalColorFeaturesDB = GlobalColorPath  
        self.ColorLayoutFeaturesDB = ColorLayoutPath  
    
  def LoadHistoDB(self):
    with open(self.HistoFeaturesDB, 'rb') as f:
       HistoDB = pickle.load(f)
    return HistoDB

  def LoadGlobalColorDB(self):
    with open(self.GlobalColorFeaturesDB, 'rb') as f:
       GlobalColorDB = pickle.load(f)
    return GlobalColorDB

  def LoadColorLayoutDB(self):
    with open(self.ColorLayoutFeaturesDB, 'rb') as f:
       ColorLayoutDB = pickle.load(f)
    return ColorLayoutDB       

  def indexDatabaseAll(self,imgpath='images/'):
     self.indexDatabaseHisto(imgpath)
     self.indexDatabaseGlobalColor(imgpath)
     self.indexDatabaseColorLayout(imgpath)
         
  def indexDatabaseHisto(self,imgpath='images/'):
   imagespath=imgpath
   images= os.listdir(imagespath)
   indexHisto={}
   a=CBIR(HistoBins=10)

   for image in images:
     fullimgpath=imagespath+'/'+image
     img=cv2.imread(fullimgpath)
     histogram=a.CalculateHistogram(img)
     indexHisto[fullimgpath]=histogram
     
   with open(self.HistoFeaturesDB, 'wb') as f:
    pickle.dump(indexHisto, f, protocol=pickle.HIGHEST_PROTOCOL)
       
   
  def indexDatabaseGlobalColor(self,imgpath='images/'):
   imagespath=imgpath
   images= os.listdir(imagespath)
   indexGlobal={}

   for image in images:
     fullimgpath=imagespath+'/'+image
     img=cv2.imread(fullimgpath)
     imgglobalColor=CBIR.get_global_color(img)
     indexGlobal[fullimgpath]=imgglobalColor
     
   with open( self.GlobalColorFeaturesDB , 'wb') as f:
    pickle.dump(indexGlobal, f, protocol=pickle.HIGHEST_PROTOCOL)
      
  def indexDatabaseColorLayout(self,imgpath='images/'):
   imagespath=imgpath
   images= os.listdir(imagespath)
   indexColorLayout={}

   for image in images:
     fullimgpath=imagespath+'/'+image
     img=cv2.imread(fullimgpath)
     imgcolorlayout=CBIR.get_color_layout(img)
     indexColorLayout[fullimgpath]=imgcolorlayout
     
   with open(self.ColorLayoutFeaturesDB, 'wb') as f:
    pickle.dump(indexColorLayout, f, protocol=pickle.HIGHEST_PROTOCOL)
    
  
    
class CBIR:

 histbins=8
 def __init__(self, HistoBins=8):
        self.histbins = HistoBins
        
 def CalculateHistogram(self,img):
   hist = cv2.calcHist([img],[0,1,2],None,[self.histbins,self.histbins,self.histbins],[0, 256, 0, 256, 0, 256])
   hist = cv2.normalize(hist,hist)
   return hist
        
 def compareHist(self,queryimghist,modelimghist):
   num = cv2.compareHist(queryimghist, modelimghist, cv2.HISTCMP_INTERSECT)
   den=sum(modelimghist.flatten())
   return(num/den)


 def get_global_color(img):
  # return avgerage color of image
    myimg = img
    avg_color_per_row = np.average(myimg, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    return avg_color


 def get_color_layout(img):
    # resize image to 500x500 then divide it into 50x50 pixels total of 10x10 grids
    myimg = img
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

    
 def FindMatches_Histo():
   cbir=CBIR(HistoBins=10)
   
   queryimg = cv2.imread(queryimgpath)
   queryimgHisto=cbir.CalculateHistogram(queryimg)
  
   DB=ImgFeaturesDatabase()
   HistoDB=DB.LoadHistoDB()
   DBimages=HistoDB.keys()
  
   thres=slider.get()
   MatchingImages={}
  
   for image in DBimages:
     DBimageHisto = HistoDB[image]
     distance=cbir.compareHist(queryimgHisto,DBimageHisto)
    
     if(distance>=(thres/100)):
         MatchingImages[image]=distance
                
   resultimages=dict(sorted(MatchingImages.items(), key=lambda item: item[1]) )    
   ImgBrowser(resultimages)


 def FindMatches_Global():  
   queryimg = cv2.imread(queryimgpath)
   queryimgGlobalColor=CBIR.get_global_color(queryimg)
   
   DB=ImgFeaturesDatabase()
   GlobalColorDB=DB.LoadGlobalColorDB()
   DBimages=GlobalColorDB.keys()
  
   thres=slider.get()
   MatchingImages={}

   for image in DBimages:
       
     DBimageGlobalColor=GlobalColorDB[image]
     
     Bdiff=abs(queryimgGlobalColor[0]-DBimageGlobalColor[0])
     Gdiff=abs(queryimgGlobalColor[1]-DBimageGlobalColor[1])
     Rdiff=abs(queryimgGlobalColor[2]-DBimageGlobalColor[2])
     
     if(Bdiff<=thres and Gdiff<=thres and Rdiff<=thres):
        MatchingImages[image]=1

   resultimages=dict(sorted(MatchingImages.items(), key=lambda item: item[1]) )    
   ImgBrowser(resultimages)



 def FindMatches_Layout():
   queryimg = cv2.imread(queryimgpath)
   bq,gq,rq=CBIR.get_color_layout(queryimg)
   
   DB=ImgFeaturesDatabase()
   ColorLayoutDB=DB.LoadColorLayoutDB()
   DBimages=ColorLayoutDB.keys()  

   thres=slider.get()
   MatchingImages={}
   
   for image in DBimages:
       
       bi,gi,ri=ColorLayoutDB[image]
       
       bdiff=np.abs(bq-bi)
       gdiff=np.abs(gq-gi)
       rdiff=np.abs(rq-ri)
       
       bdiff[bdiff<30]=1
       bdiff[bdiff>=30]=0
       
       gdiff[gdiff<30]=1
       gdiff[gdiff>=30]=0
       
       rdiff[rdiff<30]=1
       rdiff[rdiff>=30]=0
       
       bluehit=np.sum(bdiff)
       greenhit=np.sum(gdiff)
       redhit=np.sum(rdiff)
  
       if(bluehit>=thres and greenhit>=thres and redhit>=thres):
          MatchingImages[image]=bluehit+greenhit+redhit
          
   resultimages=dict(sorted(MatchingImages.items(), key=lambda item: item[1]) )   
   ImgBrowser(resultimages)




######################################
#################GUI##################
######################################
   
def main():
    global GUI 

    GUI = Tk()
    GUI.title("Content Based Media Retrieval")
    GUI.configure(bg='#d2d2d2')
    GUI.geometry("1320x700")
    GUI.resizable(True, True)
    
    labelbanner = Label(GUI, text="Content Based Media Retrieval", font=("Arial", 28), bg='lightblue', relief="ridge", fg="White")
    labelbanner.grid(columnspan=3, padx=400, sticky='ew')
    
    DrawMainScreen()
    
    GUI.mainloop()


def DrawMainScreen():

    global ButtonCBIR,ButtonCBVR
    
    ButtonCBIR= Button(GUI, text="CBIR", font=("Arial", 14),bg="lightGREEN" ,command=lambda: DrawCBIRScreen())
    ButtonCBIR.configure(height=1, width=12)
    ButtonCBIR.place(x=450, y=350)
    
    ButtonCBVR= Button(GUI, text="CBVR", font=("Arial", 14),bg="lightGREEN" ,command=lambda: DrawCBVR())
    ButtonCBVR.configure(height=1, width=12)
    ButtonCBVR.place(x=750, y=350)


def DrawCBIRScreen():
    DestroyMain()
    global ButtonBack,ButtonSelectQueryImg,ButtonIndexDB
    global labelalg,LabelIndexNote
    global buttonHistoSim,buttonGlobalColor,buttonColorLayout
    global ButtonFindMatches
    global labelthres,labelslidernote
    global origx,origy
    global QueryImgPath
    global LabelIndexNote

    origx=0
    origy=-70

    ButtonBack= Button(GUI, text="Back", font=("Arial", 8), command=lambda: DestroyCBIR())
    ButtonBack.configure(height=2, width=8)
    ButtonBack.place(x=origx+0, y=origy+70)
                
    ButtonSelectQueryImg = Button(GUI, text="Select Query Image", font=("Arial", 12), command=lambda: SelectQueryImg())
    ButtonSelectQueryImg.configure(height=2, width=16)
    ButtonSelectQueryImg.place(x=origx+90, y=origy+120)
    
    QueryImgPath = Text(GUI, height=2, width=40)


    ButtonFindMatches = Button(GUI, text="Find Matches",bg="lightgreen", font=("Arial", 12), command=lambda: ChooseCBIR_Algo())
    ButtonFindMatches.configure(height=2, width=16)
    
#########################################################
    global CBIR_alg
    CBIR_alg = IntVar()
    labelalg = Label(GUI, text="Choose Algorithm:", bg="LightBlue", fg="white", font=("Times", 16), width=15, relief="ridge")
    labelalg.place(x=origx+500, y=origy+120)
    
    buttonHistoSim = Radiobutton(GUI, text="Color Histogram", variable=CBIR_alg, value=1, bg="#d2d2d2", font=("Arial", 14),command=lambda:AutoThres())
    buttonHistoSim.place(x=origx+400, y=origy+160)
    
    buttonGlobalColor = Radiobutton(GUI, text="Mean Color", variable=CBIR_alg, value=2, bg="#d2d2d2", font=("Arial", 14),command=lambda:AutoThres())
    buttonGlobalColor.place(x=origx+600, y=origy+160)
    
    buttonColorLayout = Radiobutton(GUI, text="Color Layout", variable=CBIR_alg, value=3, bg="#d2d2d2", font=("Arial", 14),command=lambda:AutoThres())
    buttonColorLayout.place(x=origx+750, y=origy+160)
    
    
    labelthres = Label(GUI, text="Set Threshold:", bg="LightBlue", fg="white", font=("Times", 16), width=15, relief="ridge")

    global slidernote
    slidernote=StringVar()
    
    labelslidernote= Label(GUI,textvariable=slidernote,bg="#d2d2d2",fg="red",font=("Times", 14))
    labelslidernote.place(x=origx+650,y=origy+300)
       
#########################################################
    ButtonIndexDB = Button(GUI, text="Index Database", font=("Arial", 12), command=lambda: SelectImagesPath())
    ButtonIndexDB.configure(height=2, width=16)
    ButtonIndexDB.place(x=origx+1050, y=origy+120)

    global IndexNote
    IndexNote=StringVar()
    
    LabelIndexNote= Label(GUI,textvariable=IndexNote,bg="#d2d2d2",fg="red",font=("Times", 14))
    LabelIndexNote.place(x=origx+1050,y=origy+170)

    IndexNote.set("Select Images Path")


def AutoThres():
   global slider 

   try:
       slider.destroy()
   except:
       pass
    
   if(CBIR_alg.get()==1):
       slider=Scale(GUI,from_=0,to=100,orient=HORIZONTAL)       
       slider.set(22)
       slidernote.set('minimum distance')

   if(CBIR_alg.get()==2):
       slider=Scale(GUI,from_=0,to=255,orient=HORIZONTAL)       
       slider.set(30)
       slidernote.set('mean color difference')
       
   if(CBIR_alg.get()==3):
       slider=Scale(GUI,from_=0,to=100,orient=HORIZONTAL)       
       slider.set(20)
       slidernote.set('number of matching sub blocks')

   labelthres.place(x=origx+500, y=origy+250)
   
   slider.place(x=origx+540, y=origy+290)


    
def SelectQueryImg(): 
    error = 0
    global queryimgpath
    queryimgpath = filedialog.askopenfilenames()
    try:
      queryimgpath=queryimgpath[0]
    except:
        error=1
        
    global labelqueryimg  
        
    if (error == 0  and len(queryimgpath)!=0 ): #Display Query Image in UI
        im = Image.open(queryimgpath).resize((300, 300))
        ph = ImageTk.PhotoImage(im)
        
        labelqueryimg = Label(GUI,image=ph)
        labelqueryimg.image = ph
        labelqueryimg.place(x=0, y=160)
        
        ButtonFindMatches.place(x=origx+90, y=origy+600)
        
        QueryImgPath.delete('1.0', END)
        QueryImgPath.place(x=5, y=110)
        QueryImgPath.insert(END,queryimgpath )

def SelectImagesPath(): 
    error = 0
    try:
       ImagesPath = filedialog.askdirectory()
    except:
        error=1
     
    if (error == 0 and len(ImagesPath)!=0):
        IndexNote.set("Indexing Images,Please Wait...")
        GUI.update()
        DB=ImgFeaturesDatabase()
        DB.indexDatabaseAll(ImagesPath)
        IndexNote.set("Select Images Path")
        ShowError("Image Indexing Done, Features Database Saved!","Done")
                   
        
def ChooseCBIR_Algo():
   if(CBIR_alg.get()==1):
       CBIR.FindMatches_Histo()
   if(CBIR_alg.get()==2):
       CBIR.FindMatches_Global()
   if(CBIR_alg.get()==3):
       CBIR.FindMatches_Layout()
   else:
       ShowError("Please Choose Algorithm!")

    

##########################
##########################


def DestroyMain():
  
    try:
       ButtonCBIR.destroy()
       ButtonCBVR.destroy()
    except:
        pass


    global labelthres,labelnote
    global LabelIndexNote

    
def DestroyCBIR():
    try:
       ButtonBack.destroy()
       ButtonSelectQueryImg.destroy()
       ButtonIndexDB.destroy()
       labelalg.destroy()
       LabelIndexNote.destroy()
       buttonHistoSim.destroy()
       buttonGlobalColor.destroy()
       buttonColorLayout.destroy()             
    except:
        pass
    try:
      QueryImgPath.destroy()
      ButtonFindMatches.destroy()
      labelqueryimg.destroy() 
    except:
        pass
    try:
        labelthres.destroy()
        labelslidernote.destroy()
        slider.destroy()
    except:
        pass
    DrawMainScreen()

   
def ImgBrowser(resultimages):

        global imgbrowser
        imgbrowser = Toplevel(GUI)
        imgbrowser.geometry("850x620")


        master_frame = Frame(imgbrowser, bg="Light Blue", bd=1, relief=RIDGE)
        master_frame.grid(sticky=NE)
        master_frame.columnconfigure(0, weight=1)
        
     # Create a frame for the canvas and scrollbar(s).
        frame2 = Frame(master_frame,width=1320,height=700)
        frame2.grid(row=3, column=0, sticky=NW)
        
        # Add a canvas in that frame.
        canvas = Canvas(frame2, bg="#d2d2d2")
        canvas.grid(row=0, column=0)

        # Create a vertical scrollbar linked to the canvas.
        vsbar = Scrollbar(frame2, orient=VERTICAL, command=canvas.yview)
        vsbar.grid(row=0, column=1, sticky=NS)
        canvas.configure(yscrollcommand=vsbar.set)

        # Create a frame on the canvas to contain the images.
        buttons_frame = Frame(canvas,)
        #buttons_frame.grid_propagate(0)
        
        # Add the images to the frame.
        r=1
        col=0
        images=list(resultimages.keys())

        images.reverse()

        lenn=len(images)
        
        LABEL_BG = "#ccc"  # Light gray.
        ROWS, COLS = int(lenn/4)+1, 4  # Size of grid.
        ROWS_DISP = 3  # Number of rows to display.
        COLS_DISP = 4  # Number of columns to display
        
        for number in range(0,lenn):
      
          filename = images[number]
  
          if((number%4)==0):
            r+=1
            col=0
          
          image = ImageTk.PhotoImage(Image.open(filename).resize((200,200)))
             
          label = Label(buttons_frame,image=image)
          label.photo = image  
        
          label.grid(row=r, column=col)
          col+=1
          
        # Create canvas window to hold the buttons_frame.
        canvas.create_window((0,0), window=buttons_frame, anchor=NW)

        buttons_frame.update_idletasks()  # Needed to make bbox info available.
        bbox = canvas.bbox(ALL)  # Get bounding box of canvas with Buttons.
        #print(bbox)
        # Define the scrollable region as entire canvas with only the desired
        # number of rows and columns displayed.
        w, h = bbox[2]-bbox[1], bbox[3]-bbox[1]
        dw, dh = int((w/COLS) * COLS_DISP), int((h/ROWS) * ROWS_DISP)
        dw,dh=816,612
       
        canvas.configure(scrollregion=bbox, width=dw, height=dh)
        
        imgbrowser.mainloop()


####################################
########_USEFUL_FUNCTIONS_##########
####################################
def ShowError(error,title="Error"):
    errorbox = Tk()
    errorbox.withdraw()
    messagebox.showinfo(title, error)
#####################################
def buttonselected(button, buttons):
    global selectedbutton
    selectedbutton = button
    for i in buttons:
        if (i == button):
            i.configure(bg="lightblue")
        else:
            i.configure(bg='SystemButtonFace')
#####################################
def space(word, numofspaces):
    space = ""
    for i in range(0, numofspaces - len(word)):
        space = space + " "
    return space
#####################################
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False  
########################################

##########################
##########################

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master = master
        pad = 3
        self._geom = '200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth() - pad, master.winfo_screenheight() - pad))
        master.bind('<Escape>', self.toggle_geom)

    def toggle_geom(self, event):
        geom = self.master.winfo_geometry()
        print(geom, self._geom)
        self.master.geometry(self._geom)
        self._geom = geom


try:
   main()
except:
   ShowError("Error Happened, Please Check Your Inputs!")

