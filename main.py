# coding=utf-8
# 18:34 24/09/19 Project starts.
# 16:31 29/09/19 Entire project restructured.
# 23:40 11/10/19 First version (1.0) finished.
# 20:41 14/10/19 Version (1.0) debugged.
# 16:46 26/10/19 Project successfully modularized.
# 23:57 26/10/19 Version (1.1) finished and debugged.

# Generic imports
import os
import sys
import threading
from webbrowser import open as wopen

# Imported files
import egg
import size
import auto

# Tkinter imports
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk


class Main:

    def __init__(self):

        self.raiz = Tk()

        # --------NORMAL VARIABLES--------------

        self.raiz.geometry("660x525")
        self.raiz.title("!bin - Keeping things simple!")
        self.raiz.resizable(False, False)
        self.raiz.iconbitmap(self.resource_path("assets/bin_small_cont.ico"))

        self.hOffset = 115
        self.vOffset = -95

        self.dirEntryVar = StringVar()
        self.manualDir = ""

        self.checkVal = IntVar()
        self.checkVal.set(1)

        self.sizeVar = StringVar()
        self.sizeVar.set("0.0 MB")

        self.videoListLen = 0

        # ----------INTERFACE INSTANCES----------------

        self.frame1 = Frame(
            self.raiz,
            width=660,
            height=620,
        )

        self.container2 = ttk.LabelFrame(
            self.frame1,
            width=600,
            height=300,
            text="Results"
        )

        self.frame2 = Frame(
            self.frame1,
            width=378,
            height=242,
        )

        self.container1 = ttk.LabelFrame(
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

        self.songDirLabel = ttk.Label(
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
            command=lambda: self.check_switch(),

            onvalue=1,
            offvalue=0
        )

        self.dirEntryWidget = ttk.Entry(
            self.frame1,
            width=50,
            textvariable=self.dirEntryVar,
            state="disabled"
        )

        self.browseButton = ttk.Button(
            self.frame1,
            text="Browse...",
            width=13,
            command=lambda: self.browse_window(),
            state="disabled"
        )

        self.progressBar = ttk.Progressbar(
            self.frame1,
            orient="horizontal",
            length=128,
            mode="determinate",
            maximum=100000
        )  #  Here because must be rendered before the findVideosButton

        self.findVideosButton = ttk.Button(
            self.frame1,
            text="Find videos",
            width=20,
            command=lambda: self.find_thread()
        )

        self.videoList = Listbox(
            self.frame2,
            width=72,
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
            command=lambda: self.delete_thread()
        )

        # ---------------ICON SET-UP---------------

        self.aminoBut = Button(self.frame1)
        self.aminoIco = PhotoImage(file=self.resource_path("assets/amino_ico.png"))

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
        self.twitterIco = PhotoImage(file=self.resource_path("assets/twitter_ico.png"))

        self.twitterBut.config(
            image=self.twitterIco,
            border=0,
            cursor="hand2",
            relief="sunken",
            takefocus=False,

            command=lambda: wopen(
                "https://twitter.com/Axyss_"
            )
        )

        self.githubBut = Button(self.frame1)
        self.githubIco = PhotoImage(file=self.resource_path("assets/github_ico.png"))

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
        self.binIco = PhotoImage(file=self.resource_path("assets/bin_ico.png"))

        self.binBut.config(
            image=self.binIco,
            border=0,
            relief="sunken",
            takefocus=False,
            command=lambda: self.egg_run()
        )

    #  ------------------------------MAIN METHODS------------------------------
    def start(self):

        self.reset()  # Removes all info from previous executions

        if (auto.auto_obj.choose_dir(self.checkVal.get(), self.dirEntryVar.get())) == "error":
            return None  # Stops the function in case some part of choose_dir() returns error

        self.findVideosButton.config(state="disabled")  # Disables the find videos button
        self.deleteButton.config(state="disabled")  # Disables the delete button

        auto.auto_obj.check_dirs()
        auto.auto_obj.filter_videos()

        self.gen_listbox(auto.auto_obj.filtered_video_list)  # Generates the listbox with the file names

        self.sizeVar.set(size.size_obj.obtain_size(auto.auto_obj.filtered_video_list))  # Updates the file size label

        self.findVideosButton.config(state="enabled")  # Enables the find videos button
        self.deleteButton.config(state="enabled")  # Enables the Delete videos button

        # Shows the appropriate window

        if len(auto.auto_obj.filtered_video_list) == 0:
            messagebox.showinfo("Information", "Congrats, you have no videos :)")

        else:
            messagebox.showinfo("Information", "Scanning completed!")

    def browse_window(self):
        """Manages the custom window option"""

        self.manualDir = filedialog.askdirectory(initialdir="/")

        if self.manualDir != "":
            os.chdir(self.manualDir)
            print("Entering", self.manualDir)

            self.dirEntryVar.set(self.manualDir)

    def reset(self):
        """Calls all reset methods from any other
        classes and resets the own class variables"""

        size.size_obj.reset()
        self.sizeVar.set("0.0 MB")
        auto.auto_obj.reset()

        self.videoList.delete(0, END)

    def delete(self):
        """Deletes filtered beatmaps"""

        if len(auto.auto_obj.filtered_video_list) == 0:

            messagebox.showerror("Error", "First run a scan.")
            return None

        else:

            decision = messagebox.askquestion(
                "Warn",
                "Are you sure you want to delete?\nThis action cannot be undone.",
                icon='warning'
            )

            if decision == "yes":

                for i in auto.auto_obj.filtered_video_list:
                    os.remove(i)
                # print (f"File {i} removed.")  # Debug

                self.reset()

                messagebox.showinfo(
                    "Information",
                    "All beatmap videos were successfully deleted."
                )

            else:

                return None

    def increase_progress(self, video_list):
        """Increases the progressbar value base on the lenght of the video list"""
        a = 0
        if a == 0:  # Executes this part once
            self.videoListLen = 100000/len(video_list)  # Obtains how much to increase the progressbar each iteration.
            a += 1

        self.progressBar.step(self.videoListLen)

    def gen_listbox(self, video_list):
        """Draw the parameter given in the listbox"""

        for item in video_list:
            pos1 = item.rfind("/")  # Finds the first slash

            sub_item = item[0:pos1]  # Creates a subString from 0 to the first slash

            pos2 = sub_item.rfind("/")  # Finds the second slash using the last subString

            final_item = item[pos2:]  # Creates a subString from second slash to the end

            self.videoList.insert(END, " " + final_item)  # Sets the beatmap name in the listbox
            self.increase_progress(video_list)

    def check_switch(self):
        """Alternates the state of the checkbutton, entry and browse button"""

        if self.checkVal.get() == 0:
            self.dirEntryWidget.config(state="normal")
            self.browseButton.config(state="normal")

        else:
            self.dirEntryWidget.config(state="disabled")
            self.browseButton.config(state="disabled")

    def find_thread(self):
        """Starts the function start() in a different thread."""

        threading.Thread(
            target=lambda: self.start(),
            args=""
        ).start()

    def delete_thread(self):
        """Starts the function delete() in a different thread"""

        threading.Thread(
            target=lambda: self.delete(),
            args=""
        ).start()

    def egg_run(self):

        if egg.egg_obj.egg():
            del self.binIco
            del self.binBut

            Label(self.frame1,
                  text="I'll be back\n -Binny",
                  font=("COMIC SANS MS", 15)
                  ).place(
                x=25,
                y=55
            )

    def resource_path(self, relative_path):
        """Folder getter in case onefile mode is used in Pyinstaller"""

        try:
            base_path = sys._MEIPASS

        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    # -------------------------OSU!BIN GRAPHICAL DESIGN---------------------------

    def render(self):
        """Renders the graphical interface"""

        # Frames
        self.frame1.pack()
        self.frame2.place(x=55, y=300 + self.vOffset)

        # Containers
        self.container1.place(x=45 + self.hOffset, y=120 + self.vOffset)
        self.container2.place(x=30, y=272 + self.vOffset)

        # Labels
        self.sizeLabel.place(x=10, y=595 + self.vOffset)
        self.sizeLabelDyn.place(x=170, y=593 + self.vOffset)
        self.authorLabel.place(x=550, y=594 + self.vOffset)
        self.checkBoxLabel.place(x=110 + self.hOffset, y=148 + self.vOffset)
        self.songDirLabel.place(x=60 + self.hOffset, y=190 + self.vOffset)

        # Buttons
        self.findVideosButton.place(x=368 + self.hOffset, y=148 + self.vOffset)
        self.deleteButton.place(x=515, y=400 + self.vOffset)
        self.browseButton.place(x=410 + self.hOffset, y=218 + self.vOffset)

        # Icon buttons
        self.binBut.place(x=13, y=25)
        self.twitterBut.place(x=590, y=434)
        self.githubBut.place(x=550, y=434)

        # Scrollbars
        self.yscrollVideo.grid(row=0, column=1, sticky="ns")
        self.xscrollVideo.grid(row=1, column=0, sticky="ew")

        # Misc
        self.checkBox1.place(x=80 + self.hOffset, y=150 + self.vOffset)
        self.dirEntryWidget.place(x=80 + self.hOffset, y=220 + self.vOffset)
        self.videoList.grid(row=0, column=0)
        self.progressBar.place(x=484, y=64)

        # Unused
        # self.aminoBut.place(x=508,y=432)

        self.raiz.mainloop()


if __name__ == "__main__":
    windowo = Main()
    if os.name != "nt":  # If the user does not use a Windows system, then the warn down below will be shown up.
        messagebox.showinfo("Warn",
                            "Oh oh, looks like you are not using Windows,\n" +
                            "automatic folder detection may not work for you.\n" +
                            "Use the: 'custom Songs folder' option if this happens.",
                            icon='warning'
                            )
    windowo.render()
