# 18:34 24/09/19 Project starts.
# 16:31 29/09/19 Entire project restructured.
# 23:40 11/10/19 First version (1.0) finished.
# 20:41 14/10/19 Version (1.0) debugged.


import os
import threading
import egg
import size

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from webbrowser import open as wopen



class App():

    def __init__(self):

        self.raiz = Tk()

        # --------NORMAL VARIABLES--------------

        self.raiz.geometry("660x525")
        self.raiz.title("!bin - Keeping things simple!")
        self.raiz.resizable(False, False)
        self.raiz.iconbitmap("assets/bin_small_cont.ico")

        self.offset = 115
        self.vOffset = -95

        self.entryDir = StringVar()

        self.checkVal = IntVar()
        self.checkVal.set(1)

        self.sizeVar = StringVar()

        self.letters = ("C", "D", "E", "F")  # Tuple containing main letters non-volatile memories are assigned
        self.currentTry = ""
        self.manualDir = ""

        self.videoFiltered = []
        self.bmFiltered = []
        self.currentID = ""

        self.listaNum = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
        self.door = True

        # ----------INTERFACE INSTANCES----------------

        self.frame1 = Frame(
            self.raiz,
            width=660,
            height=620,
        )

        self.caja2 = ttk.LabelFrame(
            self.frame1,
            width=600,
            height=295,
            text="Results"
        )

        self.frame2 = Frame(
            self.frame1,
            width=378,
            height=242,
        )

        self.caja1 = ttk.LabelFrame(
            self.frame1,
            width=470,
            height=140,
            text="Scan videos"
        )

        self.sizeLabel = ttk.Label(
            self.frame1,
            text="Memory occupied by videos:",
            font=("Calibri", 10)
        )

        self.songDir = ttk.Label(
            self.frame1,
            text="Custom 'Songs' folder:",
            font=("Calibri", 11)
        )

        self.sizeLabelDyn = ttk.Label(
            self.frame1,
            textvariable=self.sizeVar,
            font=("Calibri", 11),
        )

        self.authorLabel = ttk.Label(
            self.frame1,
            text="Axyss - 2019 ©",
            font=("Calibri", 11)
        )

        self.checkBoxLabel = Label(
            self.frame1,
            text="Use default 'Songs' folder",
            font=("Calibri", 11)
        )

        self.checkBox1 = ttk.Checkbutton(
            self.frame1,
            takefocus=False,
            cursor="hand2",
            variable=self.checkVal,
            command=lambda: self.checkSwitch(),

            onvalue=1,
            offvalue=0
        )

        self.dirEntry = ttk.Entry(
            self.frame1,
            width=50,
            textvariable=self.entryDir,
            state="disabled"
        )

        self.browseButton = ttk.Button(
            self.frame1,
            text="Browse...",
            width=13,
            command=lambda: self.browseWindow(),
            state="disabled"
        )

        self.findVideosButton = ttk.Button(
            self.frame1,
            text="Find videos",
            width=20,
            command=lambda: self.findThread()
        )

        self.videoList = Listbox(
            self.frame2,
            width=70,
            height=15,
            borderwidth=0,
            highlightthickness=1,
            relief="solid",
            highlightbackground="#A4A4A4",
        )

        self.yscrollVideo = ttk.Scrollbar(
            self.frame2,
            command=self.videoList.yview
        )

        self.xscrollVideo = ttk.Scrollbar(
            self.frame2,
            command=self.videoList.xview,
            orient="horizontal"
        )

        self.videoList.config(yscrollcommand=self.yscrollVideo.set)

        self.videoList.config(xscrollcommand=self.xscrollVideo.set)

        self.deleteButton = ttk.Button(
            self.frame1,
            text="Delete videos",
            width=15,
            command=lambda: self.deleteThread()
        )

        # ---------------ICON SET-UP---------------

        self.aminoBut = Button(self.frame1)
        self.aminoIco = PhotoImage(file="assets/amino_ico.png")

        self.aminoBut.config(
            image=self.aminoIco,
            border=0,
            cursor="hand2",
            relief="sunken",
            takefocus=False,
            command=lambda: wopen(
                "https://aminoapps.com/c/osu-amino-2/join/"
            )
        )

        self.twitterBut = Button(self.frame1)
        self.twitterIco = PhotoImage(file="assets/twitter_ico.png")

        self.twitterBut.config(
            image=self.twitterIco,
            border=0,
            cursor="hand2",
            relief="sunken",
            takefocus=False,

            command=lambda: wopen(
                "https://github.com/Axyss"
            )
        )

        self.githubBut = Button(self.frame1)
        self.githubIco = PhotoImage(file="assets/github_ico.png")

        self.githubBut.config(
            image=self.githubIco,
            border=0,
            cursor="hand2",
            relief="sunken",
            takefocus=False,

            command=lambda: wopen(
                "https://github.com/Axyss"
            )
        )

        self.binBut = Button(self.frame1)
        self.binIco = PhotoImage(file="assets/bin_ico.png")

        self.binBut.config(
            image=self.binIco,
            border=0,
            relief="sunken",
            takefocus=False,
            command=lambda: self.eggrun()
        )

        self.recycleLabel = Label(self.frame1)
        self.recycleIco = PhotoImage(file="assets/recycle_ico.png")

        self.recycleLabel.config(
            image=self.recycleIco,
            border=0,
            relief="sunken"
        )

    def setDefaultDir(self):  # Unique callable method

        self.reset()

        self.temporary = self.chooseDir()

        if self.temporary == "Error":
            messagebox.showerror("Error", "The selected directory does not exist.")
            return None

        self.findVideosButton.config(state="disabled")  # Disables the find videos button
        self.deleteButton.config(state="disabled")  # Disables the delete button

        for bm in os.listdir():  # Looking for just beatmap folders

            self.door = True

            if bm.count(" ") == 0:  # Skip files/folders in "Songs" without spaces.
                continue

            else:
                self.currentID = bm[0:bm.find(" ")]
                # print(type(self.currentID))

                for char in self.currentID:

                    if char in self.listaNum:
                        continue

                    else:

                        # print(bm,"no es válido")
                        self.door = False
                        break

                if self.door:
                    self.bmFiltered.append(self.currentTry + "/" + bm)

        for directory in self.bmFiltered:  # Looking for videos

            os.chdir(directory)

            for file in os.listdir():

                # FILTERS

                if ".avi" in file:
                    self.videoFiltered.append(directory + "/" + file)

                if ".mp4" in file:
                    self.videoFiltered.append(directory + "/" + file)

                if ".flv" in file:
                    self.videoFiltered.append(directory + "/" + file)

        self.genListBox()  # Generates the listbox with the file names

        self.sizeVar.set(size.size_obj.obtainSize(self.videoFiltered)) # Updates the file size label

        self.findVideosButton.config(state="enabled")  # Enables the find videos button
        self.deleteButton.config(state="enabled")  # Disables the find videos button

        # Shows state window

        if len(self.videoFiltered) == 0:
            messagebox.showinfo("Information", "Congrats, you have no videos :)")

        else:
            # print(self.videoFiltered)
            messagebox.showinfo("Information", "Scanning completed!")

    def browseWindow(self):

        self.manualDir = filedialog.askdirectory(initialdir="/")

        if self.manualDir != "":
            os.chdir(self.manualDir)
            print("Entering", self.manualDir)

            self.entryDir.set(self.manualDir)

    def reset(self):  # Non-constant variables reset

        size.size_obj.sizeVar = "0.0 MB"
        size.size_obj.totalSize = 0

        self.videoList.delete(0, END)

        self.currentTry = ""
        self.manualDir = ""

        self.videoFiltered.clear()
        self.bmFiltered.clear()
        self.currentID = ""

        self.door = True
        self.totalSize = 0

    def delete(self):

        if len(self.videoFiltered) == 0:

            messagebox.showerror("Error", "First run a scan.")
            return None

        else:

            decision = messagebox.askquestion(
                "Warn",
                "Are you sure you want to delete?\nThis action cannot be undone.",
                icon='warning'
            )

            if decision == "yes":

                for i in self.videoFiltered:
                    os.remove(i)
                # print (f"File {i} removed.")# Testing purposes

                self.reset()

                messagebox.showinfo(
                    "Information",
                    "All beatmap videos were succesfully deleted."
                )

            else:

                return None

# todo Hacer que el archivo se pueda utilizar en modo onefile

    def genListBox(self):

        for item in self.videoFiltered:
            pos1 = item.rfind("/")  # Finds the first slash

            subItem = item[0:pos1]  # Creates a subString from 0 to the first slash

            pos2 = subItem.rfind("/")  # Finds the second slash using the last subString

            finalItem = item[pos2:]  # Creates a subString from second slash to the end

            self.videoList.insert(END, " " + finalItem)  # Sets the beatmap name in the listbox

    def checkSwitch(self):

        if self.checkVal.get() == 0:

            self.dirEntry.config(state="normal")
            self.browseButton.config(state="normal")
        else:

            self.dirEntry.config(state="disabled")
            self.browseButton.config(state="disabled")

    def chooseDir(self):

        if self.checkVal.get() == 1:

            for i in self.letters:  # Looking for the Songs directory

                self.currentTry = i + ":/Users/" + os.getlogin() + "/AppData/Local/osu!/Songs"

                if os.path.isdir(self.currentTry):

                    os.chdir(self.currentTry)
                    print("Directory", self.currentTry, "succesfully found!")
                    break

                else:

                    print("Directory not found at", self.currentTry)
                    self.currentTry = ""

            if self.currentTry == "":
                messagebox.showerror('Error', "Default folder couldn't be found" +
                                     "\n use the custom directory option"
                                     )
                return "Error"

        elif self.checkVal.get() == 0 and self.dirEntry.get() != "":

            self.currentTry = self.dirEntry.get()

            if os.path.isdir(self.currentTry):

                os.chdir(self.currentTry)
                print("Directory", self.currentTry, "succesfully found!")

            else:

                print("Directory not found at", self.currentTry)
                self.currentTry = ""
                return "Error"

        else:
            return "Error"

    def findThread(self):

        threading.Thread(
            target=lambda: self.setDefaultDir(),
            args=""
        ).start()

    def deleteThread(self):

        threading.Thread(
            target=lambda: self.delete(),
            args=""
        ).start()

    def eggrun(self):

        if egg.egg_obj.egg():

            del self.binIco
            del self.binBut

            Label(self.frame1,
                text="I'll be back\n -Binny",
                font=("COMIC SANS MS", 15)
                ).place(
                x=30,
                y=50
            )
    # -------------------------OSU!BIN GRAPHICAL DESIGN---------------------------

    def render(self):

        self.frame1.pack()

        self.caja2.place(x=30, y=280 + self.vOffset)

        self.frame2.place(x=55, y=300 + self.vOffset)

        self.caja1.place(x=45 + self.offset, y=120 + self.vOffset)

        self.sizeLabel.place(x=10, y=595 + self.vOffset)

        self.sizeLabelDyn.place(x=170, y=593 + self.vOffset)

        self.songDir.place(x=60 + self.offset, y=190 + self.vOffset)

        self.authorLabel.place(x=550, y=594 + self.vOffset)

        self.checkBoxLabel.place(x=110 + self.offset, y=148 + self.vOffset)

        self.checkBox1.place(x=80 + self.offset, y=150 + self.vOffset)

        self.dirEntry.place(x=80 + self.offset, y=220 + self.vOffset)

        self.browseButton.place(x=410 + self.offset, y=218 + self.vOffset)

        self.findVideosButton.place(x=368 + self.offset, y=148 + self.vOffset)

        self.videoList.grid(row=0, column=0)

        self.yscrollVideo.grid(row=0, column=1, sticky="ns")

        self.xscrollVideo.grid(row=1, column=0, sticky="ew")

        self.deleteButton.place(x=515, y=400 + self.vOffset)

        # ---------------PLACE() ICONS-----------------

        self.binBut.place(x=13, y=25)

        self.twitterBut.place(x=590, y=432)

        self.githubBut.place(x=550, y=432)

        # self.aminoBut.place(x=508,y=432)

        self.recycleLabel.place(x=495, y=307)

        self.raiz.mainloop()

if __name__ == "__main__":
    windowo = App()
    windowo.render()
