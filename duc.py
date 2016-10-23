#!/usr/bin/env python

import os

import pygtk
pygtk.require('2.0')
import gtk

from scan import Scanner

BTN_TITLE_SCAN = "Scan!"
BTN_TITLE_STOP = "Stop"

BTN_TITLE_SELECT_DIRECTORY = "Select directory..."

DEFAULT_DIRECTORY = os.path.expanduser("~/Desktop")

class Base:
    def get_dir_to_scan(self):
        return self.btnDirSelect.get_filename()

    def delete_event(self, widget, event, data = None):
        return False
    def destroy(self, widget, data = None):
        gtk.main_quit()

    def startStopScan(self, widget, data = None):
        self.scanning = False if self.scanning else True

        self.setBtnStartStopLabel()

        if (self.scanning):
            # start scanning
            theDir = self.get_dir_to_scan()

            print "Scanning %s" % theDir

            scanner = Scanner(theDir)

            scanner.scan()

            self.scanning = False

            self.setBtnStartStopLabel()
        else:
            # stop scanning
            print "Aborted scan!"

    def setBtnStartStopLabel(self):
        self.btnStartStop.set_label(
            BTN_TITLE_STOP if self.scanning else BTN_TITLE_SCAN
        )

    def selectDirectory(self, widget, data = None):
        print "Selecting directory %s" % data

    def openDirSelect(self, widget, data = None):
        self.dirSelect.show()

    def __init__(self):
        self.scanning = False

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        # window close
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)

        self.window.set_border_width(10)

        actionBox = gtk.HButtonBox()
        actionBox.set_layout(gtk.BUTTONBOX_SPREAD)

        # button to open file selection box
        self.btnDirSelect = gtk.FileChooserButton(BTN_TITLE_SELECT_DIRECTORY)

        self.btnDirSelect.set_filename(DEFAULT_DIRECTORY)
        self.btnDirSelect.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)

        actionBox.add(self.btnDirSelect)
        self.btnDirSelect.show()

        # button to scan directory
        self.btnStartStop = gtk.Button(BTN_TITLE_SCAN)

        self.clickEvtBtnScan = self.btnStartStop.connect(
            "clicked", self.startStopScan, None
        )

        actionBox.add(self.btnStartStop)
        self.btnStartStop.show()

        actionBox.show()
        self.window.add(actionBox)

        self.window.show()

    def main(self):
        gtk.main()


if __name__ == "__main__":
    base = Base()
    base.main()
