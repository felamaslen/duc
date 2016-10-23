#!/usr/bin/env python

import os

import pygtk
pygtk.require('2.0')
import gtk

from scan import Scanner
import tree

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 500

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
        """
        either start or stop a scan depending on current status
        """
        self.scanning = False if self.scanning else True

        self.setBtnStartStopLabel()

        if (self.scanning):
            # start scanning
            theDir = self.get_dir_to_scan()

            print "Scanning %s" % theDir

            scanner = Scanner(theDir)

            scanner.scan()

            # add data to the tree view
            tree.addTreeData(scanner.tree, self.treeStore)

            self.treeView = gtk.TreeView(self.treeStore)

            self.tvColumn = gtk.TreeViewColumn("File name")

            self.treeView.append_column(self.tvColumn)

            # create a CellRenndererText to render the tree data
            self.cell = gtk.CellRendererText()

            # add the cell to the tvColumn and allow it to expand
            self.tvColumn.pack_start(self.cell, True)

            """
            set the cell "text" attribute to column 0 - retrieve text
            from that column in treeStore
            """
            self.tvColumn.add_attribute(self.cell, "text", 0)

            self.treeView.set_search_column(0)

            self.tvColumn.set_sort_column_id(0)

            self.mainBox.pack_start(self.treeView)

            self.treeView.show()

            # finished scanning
            self.scanning = False

            self.setBtnStartStopLabel()
        else:
            # stop scanning
            print "Aborted scan!"

    def setBtnStartStopLabel(self):
        """
        set the title of the scan button depending on
        whether we're scanning
        """
        self.btnStartStop.set_label(
            BTN_TITLE_STOP if self.scanning else BTN_TITLE_SCAN
        )

    def __init__(self):
        self.scanning = False

        window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        # window close
        window.connect("delete_event", self.delete_event)
        window.connect("destroy", self.destroy)

        window.set_size_request(WINDOW_WIDTH, WINDOW_HEIGHT)
        window.set_border_width(10)

        self.mainBox = gtk.VBox(False, 0)
        window.add(self.mainBox)

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

        self.mainBox.pack_start(actionBox)

        self.mainBox.show()

        # tree list view
        self.treeStore = gtk.TreeStore(str)

        self.treeList = gtk.TreeView()

        window.show()

    def main(self):
        gtk.main()


if __name__ == "__main__":
    base = Base()
    base.main()
