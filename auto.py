import os
from tkinter import messagebox


class Automatic:

    def __init__(self):

        self.letters = ("C", "D", "E", "F")  # Units where the program will try to find osu!/songs
        self.templates = (
            ":/Users/" + os.getlogin() + "/AppData/Local/osu!/Songs",
            ":/Program Files/osu!/Songs",
            ":/Program Files (x86)/osu!/Songs"
        )
        self.currentTry = ""
        self.manualDir = ()
        self.posDirs = []

        # ---------------------------

        self.bmFiltered = []
        self.filtered_video_list = []

        self.currentID = ""

        self.listaNum = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
        self.door = True

    def construct_dirs(self):  # Method only called when class instanced
        # type: () -> owo
        """Constructs all possible directories with the given parameters in
        self.templates and self.letters"""

        for letter in self.letters:
            for dir in self.templates:
                self.posDirs.append(letter + dir)

    def choose_dir(self, check_val, entry_dir):
        """Checks which dir from self.posDirs is the correct one"""

        if check_val == 1:  # If checkbox enabled

            for i in self.posDirs:  # Looking for the Songs directory

                self.currentTry = i

                if os.path.isdir(self.currentTry):  # If dir exists the enter

                    os.chdir(self.currentTry)
                    print("Directory", self.currentTry, "successully found!")
                    break

                else:
                    #  print("Directory not found at", self.currentTry)
                    self.currentTry = ""

            if self.currentTry == "":
                messagebox.showerror('Error', "Default folder couldn't be found," +
                                     "\n use the custom directory option."
                                     )
                return "error"

        # This will be executed in case the automatic detection didn't work.

        elif check_val == 0 or entry_dir == "":  # If checkbox not enabled or entry empty

            self.currentTry = entry_dir

            if os.path.isdir(self.currentTry):

                os.chdir(self.currentTry)
                print("Directory", self.currentTry, "successully found!")

            else:

                messagebox.showerror("Error", "The selected directory does not exist.")
                print("Directory not found at", self.currentTry)
                self.currentTry = ""
                return "error"

        else:
            return None

    def check_dirs(self):
        """Detects which folders in Songs are beatmap folders and which not"""

        for bm in os.listdir():  # Looking for just beatmap folders

            self.door = True

            if bm.count(" ") == 0:  # Skip files/folders in "Songs" without spaces
                continue

            else:  # Detects if the folder is a beatmap one using the ID
                self.currentID = bm[0:bm.find(" ")]
                # print(type(self.currentID))

                for char in self.currentID:

                    if char in self.listaNum:
                        continue

                    else:
                        self.door = False
                        break

                if self.door:
                    self.bmFiltered.append(self.currentTry + "/" + bm)

    def filter_videos(self):
        """Creates a new list that contains the video folders"""

        for directory in self.bmFiltered:  # Looking for videos

            os.chdir(directory)

            for file in os.listdir():

                # FILTERS

                if ".avi" in file:
                    self.filtered_video_list.append(directory + "/" + file)

                if ".mp4" in file:
                    self.filtered_video_list.append(directory + "/" + file)

                if ".flv" in file:
                    self.filtered_video_list.append(directory + "/" + file)

    def reset(self):  # Called from main class.
        """Resets some vars of the class"""

        self.currentTry = ""
        self.manualDir = ()
        # ---------------------------
        self.bmFiltered.clear()
        self.filtered_video_list.clear()
        self.currentID = ""
        self.door = True


if __name__ != "__main__":
    auto_obj = Automatic()
    auto_obj.construct_dirs()  # This method is called here because It will just be exec once.
