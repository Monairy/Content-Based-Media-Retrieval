from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt
from PIL import ImageTk, Image
from tkinter import filedialog
import os


####################################
########_USEFUL_FUNCTIONS_##########
####################################
def ShowError(error):
    errorbox = Tk()
    errorbox.withdraw()
    messagebox.showinfo("Error", error)


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
def DrawCBIR():
    DestroyMain()

    global ButtonFindMatches,origx,origy
    global QueryImgPath
    origx=0
    origy=-70
            
    ButtonSelectQueryImg = Button(GUI, text="Select Query Image", font=("Arial", 12), command=lambda: SelectQueryImg())
    ButtonSelectQueryImg.configure(height=2, width=16)
    ButtonSelectQueryImg.place(x=origx+90, y=origy+120)
    
    
    global Type
    Type = IntVar()
    label1 = Label(GUI, text="Choose Algorithm:", bg="LightBlue", fg="white", font=("Times", 16), width=15, relief="ridge")
    label1.place(x=origx+500, y=origy+120)
    
    buttonHistoSim = Radiobutton(GUI, text="Histogram Similarity", variable=Type, value=1, bg="#d2d2d2", font=("Arial", 14))
    buttonHistoSim.place(x=origx+400, y=origy+160)
    buttonBestFit = Radiobutton(GUI, text="ay 7aga", variable=Type, value=2, bg="#d2d2d2", font=("Arial", 14))
    buttonBestFit.place(x=origx+650, y=origy+160)

    ButtonFindMatches = Button(GUI, text="Find Matches",bg="lightgreen", font=("Arial", 12), command=lambda: FindMatches())
    ButtonFindMatches.configure(height=2, width=16)


    QueryImgPath = Text(GUI, height=2, width=40)
    QueryImgPath.place(x=5, y=110)


def SelectQueryImg(): 
    error = 0
    global queryimg
    queryimg = filedialog.askopenfilenames()
    queryimg=queryimg[0]
    
    im = Image.open(queryimg).resize((300, 300))
    ph = ImageTk.PhotoImage(im)
    
    labelimg = Label(GUI,image=ph)
    labelimg.image = ph
    labelimg.place(x=0, y=160)
    ButtonFindMatches.place(x=origx+90, y=origy+600)

    if (error == 0):
        QueryImgPath.insert(END,queryimg )

def FindMatches():
  ImgBrowser()


def ImgBrowser():


        global imgbrowser
        imgbrowser = Toplevel(GUI)
        imgbrowser.geometry("850x600")


        master_frame = Frame(imgbrowser, bg="Light Blue", bd=1, relief=RIDGE)
        master_frame.grid(sticky=NE)
        master_frame.columnconfigure(0, weight=1)
        
     # Create a frame for the canvas and scrollbar(s).
        frame2 = Frame(master_frame,width=1320,height=700)
        frame2.grid(row=3, column=0, sticky=NW)

        

        # Add a canvas in that frame.
        canvas = Canvas(frame2, bg="Yellow")
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
        images=os.listdir('images')

        
        lenn=20
        LABEL_BG = "#ccc"  # Light gray.
        ROWS, COLS = int(lenn/4)+1, 4  # Size of grid.
        ROWS_DISP = 3  # Number of rows to display.
        COLS_DISP = 4  # Number of columns to display
        
        for number in range(lenn):
      
          filename = "images/"+images[number]
  
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

        # Define the scrollable region as entire canvas with only the desired
        # number of rows and columns displayed.
        w, h = bbox[2]-bbox[1], bbox[3]-bbox[1]
        dw, dh = int((w/COLS) * COLS_DISP), int((h/ROWS) * ROWS_DISP)
        canvas.configure(scrollregion=bbox, width=dw, height=dh)
        
        imgbrowser.mainloop()




######################################
def main():
    global GUI, ButtonCBIR,ButtonCBVR

    GUI = Tk()
    #FullScreenApp(GUI)
    GUI.title("Content Based Media Retrieval")
    GUI.configure(bg='#d2d2d2')
    GUI.geometry("1320x700")
    GUI.resizable(True, True)


    labelbanner = Label(GUI, text="Content Based Media Retrieval", font=("Arial", 28), bg='lightblue', relief="ridge", fg="White")
    labelbanner.grid(columnspan=3, padx=400, sticky='ew')


    ButtonCBIR= Button(GUI, text="CBIR", font=("Arial", 14),bg="lightGREEN" ,command=lambda: DrawCBIR())
    ButtonCBIR.configure(height=1, width=12)
    ButtonCBIR.place(x=450, y=350)
    
    ButtonCBVR= Button(GUI, text="CBVR", font=("Arial", 14),bg="lightGREEN" ,command=lambda: DrawCBVR())
    ButtonCBVR.configure(height=1, width=12)
    ButtonCBVR.place(x=750, y=350)    
    #ImgBrowser()
    GUI.mainloop()


##########################
##########################


def DestroyMain():
  
    try:
       ButtonCBIR.destroy()
       ButtonCBVR.destroy()
    except:
        pass





def DestroyAll():  # make sure that area we use is clear before placing objects

    try:
       label1.destroy()
       entry1.destroy()
       label2.destroy()
       label3.destroy()
       entry3.destroy()
       label5.destroy()
       label6.destroy()
       entry6.destroy()
       label7.destroy()
       entry7.destroy()
       label8.destroy()
       entry8.destroy()
       label9.destroy()
       entry9.destroy()
       ButtonAddProcess.destroy()
       ButtonAddSegment.destroy()
       labelimg.destroy()
    except:
        pass
    try:
        HolesContentUI.destroy()
        ProcessContentUI.destroy()
        SegTableUI.destroy()
    except:
        pass

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

