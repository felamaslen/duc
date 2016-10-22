#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

BTN_TITLE_SCAN = "Scan!"
BTN_TITLE_STOP = "Stop"

class Base:
    def delete_event(self, widget, event, data = None):
        return False
    def destroy(self, widget, data = None):
        gtk.main_quit()

    def startStopScan(self, widget, data = None):
        if (self.scanning):
            # stop scanning
            print "Aborted scan!"
        else:
            # start scanning
            print "Scanning!"

        self.scanning = False if self.scanning else True

        self.setBtnStartStopLabel()

    def setBtnStartStopLabel(self):
        self.btnStartStop.set_label(
            BTN_TITLE_STOP if self.scanning else BTN_TITLE_SCAN
        )

    def __init__(self):
        self.scanning = False

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        # window close
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)

        self.window.set_border_width(10)

        # button to scan directory
        self.btnStartStop = gtk.Button(BTN_TITLE_SCAN)

        self.clickEvtBtnScan = self.btnStartStop.connect(
            "clicked", self.startStopScan, None
        )

        self.window.add(self.btnStartStop)
        self.btnStartStop.show()

        self.window.show()

    def main(self):
        gtk.main()


if __name__ == "__main__":
    base = Base()
    base.main()
