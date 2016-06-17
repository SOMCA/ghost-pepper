import sys
import os
import math

class ProgressBar:
    """
    Progress bar object
    This object is caracterized by a maximal value, the maximal value of the bar, and the title of the bar
    """
    def __init__ (self, valmax, maxbar, title, pacman_style = False):
        if valmax <= 0:
            valmax = 1
        if maxbar <= 0:
            maxbar = 100
        if maxbar > 200:
            maxbar = 200
        if title == "":
            title = "Progress bar"
        self.valmax = valmax
        self.maxbar = maxbar
        self.title  = title
        if pacman_style:
            self.progress_before_tip = '-'
            self.progress_after_tip = 'o'
            self.pacman_icon_style = True
        else:
            self.progress_before_tip = '#'
            self.progress_after_tip = ' '
            self.progress_tip = '>'
            self.pacman_icon_style = None

    def update(self, val):
        """
        Method to update the ProgressBar object
        """
        if val > self.valmax:
            val = self.valmax
        perc  = round((float(val) / float(self.valmax)) * 100)
        scale = 100.0 / float(self.maxbar)
        bar   = int(perc / scale)

        mul_coef = math.floor((self.maxbar - bar)/len(self.progress_after_tip))

        if self.pacman_icon_style != None:
            if self.pacman_icon_style:
                self.progress_tip = '\033[1;33;40mC\033[0m'
            if not self.pacman_icon_style:
                self.progress_tip = '\033[1;33;40mc\033[0m'
            self.pacman_icon_style = not self.pacman_icon_style

        if (val == self.valmax):
            char_to_return = "\n"
        else:
            char_to_return = "\r"

        print("{0} [{1}{2}{3}] {4}%".format(self.title, self.progress_before_tip * bar, self.progress_tip, self.progress_after_tip * mul_coef, perc), end=char_to_return)
