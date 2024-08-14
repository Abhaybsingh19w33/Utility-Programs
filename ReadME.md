MoveCursor - Move cursor diagonally across screen

StayAwake -  Press keys in certain interval

TypeKeys - Type provided string in some interval

File System Reader - Tried creating windows file explorer in js
    Extract node folder, outside the parent folder

Update_packages - to update all the package in python

log.py - to print logs in python

ColourLog.py - to print coloured logs in python

TrimVideo - Trim the video in python from provided start pos to end pos

Splitter v0 - it takes video file path (video filename included) also the size limit, it iterates over the video until the size limit is reached, then it created next part

v1 - almost same but no iteration it splits video in count (size of vides / size limit)

old v2 - final it takes only folder path where all the videos are stored, then it splits the all the present video in parts

new v2 - place the script in the same folder as the videos, double click on the script. it will take the video and create parts, now if the video exceeds the size limit it will delete the new file and try to create the part again with short length to fit the size limit