import subprocess
import moviepy.editor
from Katna.video import Video
from Katna.writer import KeyFrameDiskWriter

def extractkeyframes(videopath,num_KF,SavePath="tempKF"):

  vd = Video()
  numberOFKeyFrames = num_KF
  diskwriter = KeyFrameDiskWriter(location=SavePath)
  KeyFrames = vd._extract_keyframes_from_video(numberOFKeyFrames, videopath) 
  diskwriter.write(videopath, KeyFrames)
  
  


if __name__ == "__main__":

  with open("VidPath.txt",'r') as f:
    lines=f.readlines()
    vid=lines[0].split("\n")[0]
    numKF=int(lines[1].split("\n")[0])
    if(numKF==0):
      numKF=5
    SavePath=lines[2].split("\n")[0]

  extractkeyframes(vid,numKF,SavePath)
