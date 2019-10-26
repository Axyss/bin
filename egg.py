# coding=utf-8
from os import getlogin
from tkinter import messagebox


class Webo:

    def __init__(self):
        self.eggVar = 0

    def egg(self):
        """You shouldn't be here, this was supposed to be an easter egg àwá"""
        self.eggVar += 1

        if self.eggVar == 10:
            messagebox.showinfo("?", "Looking for secrets?"
                                )

        elif self.eggVar == 20:
            messagebox.showinfo(
                "?", "There is nothing over here."
                                )

        elif self.eggVar == 30:
            messagebox.showinfo(
                "?", "Don't you have nothing to do " +
                     str(getlogin()) + "?")

        elif self.eggVar == 40:
            messagebox.showinfo("?", "Stop or I'll shutdown your computer àwá")

        elif self.eggVar == 45:
            messagebox.showinfo("?", "Just kidding, I would't do that ewe")

        elif self.eggVar == 50:
            messagebox.showinfo("Binny", "My name's Binny and I'm the !bin logo" +
                                "\nNice to meet ya' :D"
                                )

        elif self.eggVar == 60:
            messagebox.showinfo("Binny", "Do you want to hear a secret?")

        elif self.eggVar == 65:
            messagebox.showinfo("Binny",
                                "Looks like Axyss is working on a new cool osu!" +
                                "\nrelated project, but don't tell him I told you :s"
                                )

        elif self.eggVar == 75:
            messagebox.showinfo("Binny", "Oh s***, NEW FARM MAP," +
                                "\nsorry " + getlogin() + " but I have to go ;)"
                                )
            return True


if __name__ != "__main__":
    egg_obj = Webo()
