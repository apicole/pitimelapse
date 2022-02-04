#!/usr/bin/python

from picamera import PiCamera
import os
from time import sleep
import time

camera = PiCamera()

##########  VARIABLES ####
#camera.resolution = (1024, 768)
wwwpath = '/var/www/html/timelapse/'
imgname = (time.strftime("%Y%M%d_%H%M"))  #'20224031_1240'
fullrange = 9999
waitperiod = 2
fps = 24
if not os.path.exists(wwwpath): os.makedirs(wwwpath)
########################

def secondsToText(secs):
    days = secs//86400
    hours = (secs - days*86400)//3600
    minutes = (secs - days*86400 - hours*3600)//60
    seconds = secs - days*86400 - hours*3600 - minutes*60
    result = ("{0} J ".format(days) if days else "") + \
    ("{0} H ".format(hours) if hours else "") + \
    ("{0} Min ".format(minutes) if minutes else "") + \
    ("{0} Sec".format(seconds) if seconds else "")
    return result
        

print (' *  ***************************** ')
print (' *  Configuration du Timelapse : ')
print (' *   - Nombre de photos : '+ str(fullrange))
print (' *   - Intervalle       : '+ str(waitperiod))
print (' *   -> Temps total = '+ secondsToText(waitperiod * fullrange))
print (' *  ***************************** ')

try: 
    outBat = open(wwwpath+imgname+ '_ffmpeg.bat', "w")
    outShl = open(wwwpath+imgname+ '_ffmpeg.sh', "w")
    outBat.writelines('ffmpeg -r '+ str(fps) + ' -f image2 -nostats -i  '+ wwwpath + imgname + '%04d.jpg -vcodec libx264 -crf 25 -pix_fmt yuv420p '+ imgname+ '.mp4')
    outShl.writelines('ffmpeg -r '+ str(fps) + ' -f image2 -s 1024x768 -nostats -loglevel 0 -pattern_type glob -i '+ wwwpath + imgname + '/*.jpg -vcodec libx264 -crf 25  -pix_fmt yuv420p '+ imgname+ '.mp4')
    outBat.close()
    outShl.close()

    for i in range(fullrange):
        timeleft = ((fullrange - i ) * waitperiod)
        print (' photo ' + str(i)+ ' / '+ str(fullrange) + ' (' + secondsToText(timeleft)+')') 
        camera.capture(wwwpath + imgname+ '_' +  f'{i:04d}.jpg')
        sleep(waitperiod)
    
except KeyboardInterrupt:
    print (' Arret après ' + str(i)+ ' photos (' + secondsToText(i * waitperiod)+ ')') 
