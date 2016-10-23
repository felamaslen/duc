#!/usr/bin/env python

import os
import threading

import pygtk
pygtk.require('2.0')
import gtk

from scan import Scanner
import tree

WINDOW_WIDTH = 1250
WINDOW_HEIGHT = 960

BTN_TITLE_SCAN = "Scan!"
BTN_TITLE_STOP = "Stop"
BTN_TITLE_SELECT_DIRECTORY = "Select directory..."

BG_WINDOW = "#eee"

FILE_TREE_NAME = "File tree"

STATUS_IDLE = "Idle"
STATUS_DONE = STATUS_IDLE

DEFAULT_DIRECTORY = os.path.expanduser("~/Desktop")

class Base:
    def getDirToScan(self):
        return self.btnDirSelect.get_filename()

    def delete_event(self, widget, event, data = None):
        return False
    def destroy(self, widget, data = None):
        gtk.main_quit()

    def updateTree(self, data):
        self.treeStore.clear()

        tree.addTreeData(data, self.treeStore)

        self.treeView.set_model(self.treeStore)

    def onScanProgress(self, item):
        self.statusBar.set_text(item)

    def doScan(self):
        scannerThread = Scanner(
                self.getDirToScan(),
                self.onScanProgress,
                self.onScanDone,
                STATUS_DONE)

        scannerThread.run()

    def onScanDone(self, data):
        self.data = data

        # add data to the tree view
        self.updateTree(self.data)

        # finished scanning
        self.scanning = False

        self.setBtnStartStopLabel()

    def startStopScan(self, widget, data = None):
        """
        either start or stop a scan depending on current status
        """
        self.scanning = False if self.scanning else True

        self.setBtnStartStopLabel()

        if (self.scanning):
            # start scanning
            self.doScan()

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

    def addActions(self):
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

        boxActions = gtk.HBox(False, 0)
        boxActions.add(actionBox)
        boxActions.show()
        self.mainBox.pack_start(boxActions, False)


    def addTree(self):
        # tree list view
        self.treeStore = gtk.TreeStore(str, str)

        cols = ['File', 'Size']
        sizing = [
            gtk.TREE_VIEW_COLUMN_FIXED,
            gtk.TREE_VIEW_COLUMN_FIXED
        ]
        sequence = [str] * len(cols)
        tvColumn = [None] * len(cols)

        self.treeView = gtk.TreeView(self.treeStore)
        self.treeView.cell = [None] * len(cols)

        # add columns to the tree view
        for i, col in enumerate(cols):
            self.treeView.cell[i] = gtk.CellRendererText()
            tvColumn[i] = gtk.TreeViewColumn(col, self.treeView.cell[i])
            tvColumn[i].add_attribute(self.treeView.cell[i], "text", i)
            tvColumn[i].set_sizing(sizing[i])
            self.treeView.append_column(tvColumn[i])

        tvColumn[0].set_resizable(True)
        tvColumn[0].set_min_width(500)
        tvColumn[1].set_fixed_width(100)

        scrollTree = gtk.ScrolledWindow()
        scrollTree.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        scrollTree.add(self.treeView)
        scrollTree.show()

        frameTree = gtk.Frame(FILE_TREE_NAME)
        frameTree.add(scrollTree)
        frameTree.show()

        boxTree = gtk.HBox(False, 0)
        boxTree.add(frameTree)
        boxTree.show()
        self.mainBox.pack_start(boxTree, True, True, 10)

        self.treeView.show()

    def addStatusBar(self):
        statusBarTv = gtk.TextView()
        self.statusBar = statusBarTv.get_buffer()

        self.statusBar.set_text(STATUS_IDLE)

        statusBarTv.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse(BG_WINDOW))

        boxStatusBar = gtk.HBox(False, 0)
        boxStatusBar.add(statusBarTv)
        boxStatusBar.show()
        self.mainBox.pack_end(boxStatusBar, False, True, 10)

        statusBarTv.show()

    def __init__(self):
        self.scanning = False

        window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        # window close
        window.connect("delete_event", self.delete_event)
        window.connect("destroy", self.destroy)

        window.set_size_request(WINDOW_WIDTH, WINDOW_HEIGHT)
        window.set_border_width(10)
        window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(BG_WINDOW))

        self.mainBox = gtk.VBox(False, 0)
        window.add(self.mainBox)

        self.addActions()
        self.addTree()
        self.addStatusBar()

        self.mainBox.show()
        window.show()

    def main(self):
        gtk.main()


if __name__ == "__main__":
    base = Base()
    base.main()
