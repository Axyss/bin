# USED JUST FOR TESTING PURPOSES
#-------------------------------------------
# Fills every beatmap folder with trash files with .avi, .flv and .mp4 extensions.
# Warn: If It does not work for you, modify the variable "mydir" below.

import os

mydir="C:/Users/"+os.getlogin()+"/AppData/Local/osu!/Songs/"

os.chdir(mydir)

dirList=os.listdir()

for i in dirList:

	os.chdir(mydir+i)
	
	try:

		open("Trash.flv","+x")
		open("Trash.avi","+x")
		open("Trassssssssssssssssssssssssssssssssssssssssssssssssssssh.mp4","+x")


	except:

		print("Seems this program has already been used, remove the files first.")
		break

else:

	print("Files succesfully generated!")
